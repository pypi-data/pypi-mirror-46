from pathlib import Path

from sequel import (
    STORAGE_ENTRYPOINT_GROUP,
    LEDGER_ATTRIBUTE,
    ROLLBACK_ATTRIBUTE
)
from sequel import Ledger
from sequel.io import StorageFactory


class Codex(object):
    def __init__(self, codex_path):
        self._codex = load_module(codex_path)
        storage_url = getattr(self._codex, LEDGER_ATTRIBUTE, None)
        self._rollback = getattr(self._codex, ROLLBACK_ATTRIBUTE, True)
        storage_factory = StorageFactory()
        storage_factory.load_plugins(STORAGE_ENTRYPOINT_GROUP)

        self._ledger_store = storage_factory.make_storage(storage_url)
        self.ledger = Ledger.from_json(self._ledger_store.read())

        from sequel import chronicle
        self.chronicle = chronicle

    def record(self):
        self._ledger_store.write(self.ledger.to_json())

    def continued(self):
        self.ledger = self.chronicle.continued(
            self.ledger,
            rollback=self._rollback
        )
        return self.ledger

    def rollback(self):
        self.ledger = self.chronicle.rollback(self.ledger)
        return self.ledger


def load_module(path, module_id=None):
    import importlib.util
    import importlib.machinery

    module_id = module_id or Path(path).name

    spec = importlib.util.spec_from_file_location(module_id, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
