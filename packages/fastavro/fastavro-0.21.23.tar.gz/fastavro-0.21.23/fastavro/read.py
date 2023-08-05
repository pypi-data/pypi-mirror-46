try:
    from . import _read
except ImportError:
    from . import _read_py as _read

from . import _read_common

# Private API
HEADER_SCHEMA = _read_common.HEADER_SCHEMA
SYNC_SIZE = _read_common.SYNC_SIZE
MAGIC = _read_common.MAGIC
BLOCK_READERS = _read.BLOCK_READERS

# Public API
reader = iter_avro = _read.reader
block_reader = _read.block_reader
schemaless_reader = _read.schemaless_reader
is_avro = _read.is_avro
LOGICAL_READERS = _read.LOGICAL_READERS
SchemaResolutionError = _read_common.SchemaResolutionError

__all__ = [
    'reader', 'schemaless_reader', 'is_avro', 'block_reader',
    'SchemaResolutionError', 'LOGICAL_READERS',
]
