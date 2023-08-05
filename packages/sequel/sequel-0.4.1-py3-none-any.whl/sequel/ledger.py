import json

from sequel.compat import json_dumps
from sequel.algo import topological_sort


class Ledger(object):
    def __init__(self, outcomes, dependencies):
        """
        Records of a resolved :class:`sequel.Chronicle`.

        Annals are a concise historical record in which events are
        arranged chronologically.  This class makes the outcomes of
        a resolved chronicle serializable for later use.

        Args:
            outcomes (set): All current :class:`sequel.ledger.Outcome`
                of the chronicle.
            dependencies (dict): A dependencies graph of Outcome names.

        Raises:
            ValueError: In case the dependency graph contains cycles.
        """
        _ = list(topological_sort(dependencies))
        self.outcomes = outcomes
        self._depencencies = dependencies

    @property
    def data(self):
        return {
            outcome.key: outcome.value
            for outcome in self.outcomes
        }

    def to_json(self, **kwargs):
        data = {
            'events': [
                dict(name=outcome.key,
                     outcome=outcome.value,
                     time=outcome.timestamp)
                for outcome in self.outcomes
            ],
            'dependencies': self._depencencies
        }

        return json_dumps(data, **kwargs)

    @classmethod
    def from_json(cls, json_str):
        if not json_str:
            return cls(set(), dict())

        ledger_dict = json.loads(json_str)

        return cls(
            set(Outcome(outcome['name'], outcome['time'], outcome['outcome'])
                for outcome in ledger_dict['events']),
            dict((name, set(dependencies))
                 for name, dependencies in ledger_dict['dependencies'].items())
        )


class Outcome(object):
    def __init__(self, key, timestamp, value):
        self.key = key
        self.timestamp = timestamp
        self.value = value

    def __hash__(self):
        return hash((self.key, self.timestamp))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.key == other.key and self.timestamp == other.timestamp
