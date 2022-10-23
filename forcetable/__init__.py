from forcetable._record import record
from forcetable._field import field
from forcetable._field import file_field

from forcetable._table import table
from forcetable._table import records_table
from forcetable._table import primary_table

from forcetable._table import records_to_dicts
from forcetable._table import records_to_fields
from forcetable._table import records_to_table

from forcetable._table import dicts_to_records
from forcetable._table import extract_record_primary_item

from forcetable._table import json_to_table
from forcetable._table import csv_to_table_fp
from forcetable._table import csv_to_table


__all__ = [
    'record', 
    'field', 
    'file_field', 

    'table', 
    'records_table', 
    'primary_table', 

    'records_to_dicts', 
    'records_to_fields', 
    'records_to_table',

    'dicts_to_records', 
    'extract_record_primary_item', 

    'json_to_table', 
    'csv_to_table_fp', 
    'csv_to_table'
]

# # Setups __all__ containing public symbols and non modules symbols.
# # This excludes modules from being imported when importing with 'import *'.
# import types
# __all__ = [
#     name for name, object_ in globals().items()
#     if not (name.startswith("_") or isinstance(object_, types.ModuleType))
# ]
# # 'types' module is no longer needed.
# del types


__name__ = "forcetable"
__version__ = "0.0.5"
