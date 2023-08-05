from concurrent.futures import Executor, Future
import inspect
from functools import wraps, reduce, partial
import types

from sequel.algo import topological_sort
from sequel.compat import now
from sequel.ledger import Outcome, Ledger


class Chronicle(object):
    def __init__(self, executor_class=None, timestamper=None):
        """
        Create work scheduler.

        Args:
            executor_class (:class:`concurrent.futures.Executor`): Optionally
                provide the execution runtime for each independent set of work
                units. By default, independent sets of work will be run in an
                arbitrary and unstable sequence.

                When using the
                :class:`concurrent.futures.ProcessPoolExecutor`, you need to
                make sure all submitted work is :term:`picklable` to avoid
                a `known race condition`_. Also, one can use something else
                such as :mod:`pathos`.
            timestamper: A function that return the next timestamp, usually
                something like ``now()``.

        .. _known race condition: https://bugs.python.org/issue30006
        """
        self._dependencies = {}
        self._jobs = {}
        self._teardown_jobs = {}
        self._outputs = {}
        self._data = {}
        self._recurring = set()
        self._executor_class = executor_class or _SequentialExecutor
        self._timestamper = timestamper or now

    def make_nodes(self, episode, outcomes=None, recur=False):
        """
        Add nodes to the dependency graph based on a function signature.

        Each time this method is called, one or more nodes are added to the
        dependency graph.  If `outputs` is provided, the amount of outputs
        designate the amount of nodes created.

        Parameter names of `function` are dependencies to other nodes.  In
        case multiple outputs are specified, all of them will have all these
        dependencies.

        The number of returned values from `function` must also match the
        amount of outputs or else a :class:`sequel.OutputMismatch` will
        be raised by :meth:`sequel.Chronicle.resolve`.

        Here is simple sum of two other nodes

        .. code-block:: python

                def one():
                    return 1

                def two():
                    return 2

                def add(one, two):
                    return one + two

                graph = Chronicle()
                graph.make_nodes(one)
                graph.make_nodes(two)
                graph.make_nodes(three)

        The resulting graph could be reprensented as followed.

        .. digraph:: simple_sum

            add -> one;
            add -> two;

        .. note:: The arrow direction should be interpreted as
            *depends on*.

        The :paramref:`sequel.Chronicle.make_nodes.output` parameters can
        be used to explicitely specify the nodes names and generate more than
        one node for a given callable:

        .. code-block:: python

            def values():
                return 1,2

            def add(one, two):
                return one + two

            graph = Chronicle()
            graph.make_nodes(values, outputs=('one', 'two'))
            graph.make_nodes(three)

        The resulting graph is the same as above

        .. digraph:: simple_sum

            add -> one;
            add -> two;

        Args:
            episode (:ref:`callable-types`) Any callable object.
            outcomes: Optionally provide the names of outputs of that callable.
            recur (bool): If True, provisioned data will be ignored,
                triggering the callable again even if its outcomes were
                stored and reused.  Defaults to False.  If this callable
                has many outputs, it still be called only once
        """
        outcomes = outcomes if outcomes is not None else [episode.__name__]
        signature = inspect.signature(episode)
        self._outputs[episode] = outcomes

        for node in outcomes:
            self._dependencies[node] = set(signature.parameters)
            self._jobs[node] = episode
            if recur:
                self._recurring.add(node)

    def resolve(self, node):
        """
        Resolve a given node of the graph.

        This method will run any callable attached to a given node if it is
        required.  Since node are equivalent to callable outputs, it will
        only be run if the output was not previously generated.

        Args:
            node: A node (or node identifier) to be resolved.

        Returns:
            dict: A mapping of outcome values by outcome names.
        """
        try:
            result = self._data[node]
            output_names = [node]
        except KeyError:
            function = self._jobs[node]
            result = self._invoke(node)

            output_names = self._outputs[function]

        if not isinstance(result, tuple):
            result = (result,)

        if len(output_names) != len(result):
            # FIXME
            # This should be raised in earlier (in make_nodes)
            # but there is no way to inspect return statements
            # of a function that is not called yet
            raise OutputMismatch()

        result_by_name = dict(zip(output_names, result))
        self._data.update(result_by_name)

        return result_by_name

    def _invoke(self, node):
        function = self._jobs[node]
        arguments = {argument_name: self._data[argument_name]
                     for argument_name in self._dependencies[node]}
        result = function(**arguments)
        if isinstance(result, types.GeneratorType):
            self._teardown_jobs[node] = partial(drain, result)
            result = next(result)
        return result

    def rollback_node(self, node):
        try:
            self._teardown_jobs[node]()
            _ = self._data.pop(node)
            return node
        except KeyError:
            pass

    def import_data(self, input=None):
        if isinstance(input, Ledger):
            input = input.data

        self._data.update(input or {})

    def continued(self, input=None, rollback=True):
        """
        Resolve all the values of nodes of the graph by executing the
        underlying functions.

        The work to do is sequenced with the topological sort provided by
        :func:`sequel.algo.topological_sort`.

        Independent sets are run in pseudo-parallel based on the executor
        provided to :paramref:`sequel.Chronicle.executor_class`.

        Args:
            input (:class:`sequel.Ledger`): Initial values that will
                prevent any non-recurring episode from occuring again.
                A flat dictionary of initial values will also do. Keys
                must match node (outcome) names.

        Returns:
            The last resolved value.
        """
        self.import_data(input)

        for node in self._recurring:
            _ = self._data.pop(node, None)

        ledger = Ledger(set(), self._dependencies.copy())

        try:
            for independent_sets in topological_sort(self._dependencies):
                results = self._run_independent_sets(independent_sets)
                self._results_into_outcomes(ledger.outcomes, results)
        except Exception:
            if rollback:
                return self.rollback(ledger)

        return ledger

    def rollback(self, ledger=None):
        existing_nodes = self._extract_outcome_dict(ledger)

        ordered = topological_sort(self._dependencies)

        for independent_sets in reversed(list(ordered)):
            rollbacked = self._teardown_independent_sets(independent_sets)

            ledger.outcomes = ledger.outcomes - set(
                [existing_nodes[node]
                 for node in rollbacked
                 if node is not None]
            )

        return ledger

    def _extract_outcome_dict(self, ledger=None):
        if ledger:
            existing_nodes = {
                outcome.key: outcome for outcome in ledger.outcomes
            }
        else:
            existing_nodes = {}

        return existing_nodes

    def _results_into_data(self, results):
        for result_dict in results:
            self._data.update(result_dict)

    def _results_into_outcomes(self, outcomes, results):
        for result_dict in results:
            for name, outcome_value in result_dict.items():
                outcomes.add(Outcome(name,
                                     self._timestamper(),
                                     outcome_value))

    def _run_independent_sets(self, independent_sets):
        # FIXME Concurrent run are broken since self._data is not shared
        return [self.resolve(node) for node in independent_sets]

    def _teardown_independent_sets(self, independent_sets):
        # FIXME Concurrent run are broken since self._data is not shared
        return [self.rollback_node(node) for node in independent_sets]

    def episode(self, *decargs, **deckwargs):
        def decorator(f):
            @wraps(self.make_nodes)
            def func_wrapper(f, *args, **kwargs):
                return self.make_nodes(f, *args, **kwargs)
            return func_wrapper(f, *decargs, **deckwargs)
        return decorator

    @property
    def data(self):
        return self._data


class OutputMismatch(ValueError):
    pass


class _SequentialExecutor(Executor):
    def submit(self, fn, *args, **kwargs):
        future = Future()

        result = fn(*args, **kwargs)

        future.set_result(result)

        return future


def drain(iterator):
    reduce(lambda _, __: None, iterator)
