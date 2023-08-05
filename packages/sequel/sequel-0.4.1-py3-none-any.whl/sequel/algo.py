from functools import reduce


def topological_sort(graph):
    """
    Make a topological sort of a directed acyclic graph using
    `Kahn's algorithm`_.

    Args:
        graph (dict): A :class:`dict` of :class:`set` objects that maps a
            node to the set of its dependencies.

    Yields:
        :class:`set`: Each yielded item is an independent set.  Elements of
            a given yielded set will only have dependencies on elements of
            previous sets.

    In case you require a flat generator as a result, you could wrap this
    function like the following:

    .. code-block:: python

        def flat_topological_sort(graph):
            for independent_set in topological_sort(graph):
                yield from independent_set
                # For a unique solution, sort the set first:
                # yield from sorted(independent_set)

    .. _Kahn's algorithm: https://en.wikipedia.org/wiki/Topological_sorting
    """
    if not graph:
        return []

    graph = _make_normalized_graph(graph)

    while True:
        nodes_without_deps = _find_nodes_without_deps(graph)

        if not nodes_without_deps:
            break

        yield nodes_without_deps

        graph = _make_graph_excluding_nodes(graph, nodes_without_deps)

    if len(graph):
        raise ValueError('Graph has cycles!')


def _find_nodes_without_deps(graph):
    return set(node
               for node, deps in graph.items()
               if not deps)


def _make_graph_excluding_nodes(graph, excluded_nodes):
    return {node: set(deps - excluded_nodes)
            for node, deps in graph.items()
            if node not in excluded_nodes}


def _make_normalized_graph(graph):
    graph = graph.copy()

    for element, dependencies in graph.items():
        dependencies.discard(element)

    graph.update({
        node_found_only_in_deps: set()
        for node_found_only_in_deps in reduce(
            set.union, graph.values()) - set(graph.keys())
    })

    return graph
