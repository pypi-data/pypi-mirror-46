import logging

import click

from sequel import __dist__
from sequel.codex import Codex

log = logging.getLogger(__name__)


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
    codex = Codex(codex)

    codex.rollback()

    print(codex.ledger.to_json())

    codex.record()


@main.command()
@click.argument('codex')
def occur(codex):
    """Read your Codex from a module then resolve its Chronicle and Ledger."""
    codex = Codex(codex)

    codex.continued()

    print(codex.ledger.to_json())

    codex.record()
