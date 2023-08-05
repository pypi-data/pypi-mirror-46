from pkg_resources import DistributionNotFound


"""
Attributes:
    __project__ (str): Runtime value for the package name and command
        line entrypoint.

    __version__ (str): Runtime value for the current version.

    __dist__ (:class:`pkg_resources.Distribution`): Runtime guess about
        its installation.  This may be a tissue of lies since it
        **will** be created, whether an installed distribution can be
        found or not.  This will happen if the package is not
        installed.

        .. warning:: Development (editable) installations may break
            other packages from the same implicit namespace. See
            https://github.com/pypa/packaging-problems/issues/12

        See :doc:`pkg_resources` for details.

    _PACKAGE (str): The advertised name of **this** package. We
        introspect the current installation for convenience.
"""


_PACKAGE = 'sequel'


try:
    from pkg_resources import get_distribution
    __dist__ = get_distribution(_PACKAGE)  # type: Distribution
    __project__ = __dist__.project_name
    __version__ = __dist__.version
except DistributionNotFound:
    from pkg_resources import Distribution
    __dist__ = Distribution(project_name=_PACKAGE,
                            version='(local)')
    __project__ = __dist__.project_name
    __version__ = __dist__.version
except ImportError:
    __project__ = _PACKAGE
    __version__ = '(local)'
else:
    pass


from sequel.dag import Chronicle
from sequel.ledger import Ledger
from sequel.dag import OutputMismatch


chronicle = Chronicle()


STORAGE_ENTRYPOINT_GROUP = '{!s}_storage'.format(__project__)
LEDGER_ATTRIBUTE = 'LEDGER'
ROLLBACK_ATTRIBUTE = 'ROLLBACK'


__all__ = ['Chronicle',
           'Ledger',
           'OutputMismatch',
           'STORAGE_ENTRYPOINT_GROUP']
