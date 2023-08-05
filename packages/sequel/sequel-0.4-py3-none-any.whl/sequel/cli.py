import logging
from pathlib import Path

import click

from sequel import (
    __dist__,
    STORAGE_ENTRYPOINT_GROUP,
    LEDGER_ATTRIBUTE,
    ROLLBACK_ATTRIBUTE
)
from sequel import Ledger
from sequel.io import StorageFactory

log = logging.getLogger(__name__)


storage_factory = StorageFactory()
storage_factory.load_plugins(STORAGE_ENTRYPOINT_GROUP)


@click.group(name=__dist__.project_name)
@click.version_option(version=__dist__.version)
@click.option('--debug', default=False, is_flag=True,
              help='Maximize verbosity for debugging.')
def main(debug):
    logging.basicConfig(level=logging.WARNING)
    if debug:  # noqa
        logging.basicConfig(level=logging.DEBUG)


@main.command()
@click.argument('codex')
def rollback(codex):
    """Rewind your Chronicle.  Beware: Time traveling is just too dangerous."""
    codex = load_module(codex)

    storage_url = getattr(codex, LEDGER_ATTRIBUTE, None)

    ledger_store = storage_factory.make_storage(storage_url)

    ledger = Ledger.from_json(ledger_store.read())

    chronicle = find_chronicle()

    ledger = chronicle.rollback(ledger)

    print(ledger.to_json())

    ledger_store.write(ledger.to_json())


@main.command()
@click.argument('codex')
def occur(codex):
    """Read your Codex from a module then resolve its Chronicle and Ledger."""
    codex = load_module(codex)

    storage_url = getattr(codex, LEDGER_ATTRIBUTE, None)
    enable_rollback = getattr(codex, ROLLBACK_ATTRIBUTE, True)

    ledger_store = storage_factory.make_storage(storage_url)

    ledger = Ledger.from_json(ledger_store.read())

    chronicle = find_chronicle()

    ledger = chronicle.continued(ledger, rollback=enable_rollback)

    print(ledger.to_json())

    ledger_store.write(ledger.to_json())


def find_chronicle():
    from sequel import chronicle
    return chronicle


def load_module(path, module_id=None):
    import importlib.util
    import importlib.machinery

    module_id = module_id or Path(path).name

    spec = importlib.util.spec_from_file_location(module_id, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
