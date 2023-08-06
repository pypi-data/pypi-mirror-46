import sys

import pkg_resources

from eth_account import Account  # noqa: E402
from iotexapi.main import Iotex  # noqa: E402

if sys.version_info < (3, 5):
    raise EnvironmentError("Python 3.5 or above is required")


__version__ = pkg_resources.get_distribution("iotexapi").version

__all__ = [
    '__version__',
    'Account',
    'Iotex',
]
