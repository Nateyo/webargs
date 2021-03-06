from distutils.version import LooseVersion
from marshmallow.utils import missing

# Make marshmallow's validation functions importable from webargs
from marshmallow import validate

from webargs.core import ValidationError
from webargs.dict2schema import dict2schema
from webargs import fields

__version__ = "6.0.0b2"
__version_info__ = tuple(LooseVersion(__version__).version)
__all__ = ("dict2schema", "ValidationError", "fields", "missing", "validate")
