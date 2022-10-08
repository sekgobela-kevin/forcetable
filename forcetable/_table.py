'''
source: url - https://github.com/sekgobela-kevin/perock
        commit Hash - de476e23a5447b2eb7af8000637b449aab200f55

Author: Sekgobela Kevin
Date: October 2022
Languages: Python 3
'''
import io
from typing import Any, Callable, Dict, Sequence
from typing import Iterable, Iterator, List, Set

import json
import csv

from forcetable._field import field
from forcetable._record import record
from forcetable import exceptions

import prodius


class table():
    '''Represents table with data for performing attack'''
    def __init__(self, fields=[]) -> None:
        '''
        Creates table with data for performing attack.
        Parameters
        ----------
        fields: Iterator
            Iterator with field objects
        '''
        # Stores fields of table
        self._fields: Set[field] = set(fields)
        # Stores record with items to be shared by all records
        self._common_record = record()
        # Stores records of table
        self._records: Iterator[record] = iter([])

        self._primary_fields: Set[field] = set()
        self._primary_field: field = None

        # Add fields to table
        # 'self._fields: Set[field] = set(fields)' is not enough
        self.add_fields(self._fields)

    def set_primary_field(self, field):
        '''Set the field as primary field'''
        self._primary_field = field
        self._fields.add(field)

    def primary_field_exists(self):
        '''Checks if table ha sprimary field'''
        return self._primary_field != None


    def add_field(self, field):
        '''Adds a coulumn to table'''
        if field.is_primary():
            # adds field to primary fields
            self._primary_fields.add(field)
            self.set_primary_field(field)
        self._fields.add(field)
        # Updates records to use the new field

    def add_fields(self, fields):
        '''Adds multiple field to table'''
        for field in fields:
            self.add_field(field)

    def add_primary_field(self, field):
        '''Add the field and make it one of primary fields'''
        self._primary_fields.add(field)
        self.set_primary_field(field)
        self._fields.add(field)

    def get_primary_fields(self):
        '''Returns primary field'''
        return self._primary_fields

    def get_primary_field(self):
        '''Returns primary field'''
        return self._primary_field

    def get_fields(self):
        '''Gets fields of table'''
        return self._fields

    def get_other_fields(self):
        '''Gets fields of table excluding primary field'''
        return self._fields.difference([self._primary_field])

    def get_field_by_name(self, name):
        '''Gets field by its name(raises exception if not found)'''
        # It was better if map(dict) was used instead of set
        for field in self._fields:
            if field.get_name() == name:
                return field
        err_msg = "field with name '{}' not found"
        raise exceptions.fieldNotFound(err_msg.format(name))

    def get_field_by_item_name(self, name, force=False):
        '''Gets field by its item name(raises exception if not found)'''
        # It was better if map(dict) was used instead of set
        for field in self._fields:
            if field.get_item_name() == name:
                return field
        err_msg = "field with item name '{}' not found"
        raise exceptions.fieldNotFound(err_msg.format(name))

    def get_records(self):
        '''Returns records of the table'''
        # Update records before returning them
        self.update()
        return self._records


    def get_field_names(self):
        '''Returns names of fields in table'''
        return {field.get_name() for field in self._fields}

    def get_item_names(self):
        '''Returns item names from table fields'''
        return {field.get_item_name() for field in self._fields}

    def get_fields_items(self):
        '''Returns items of fields in table'''
        return [field.get_items() for field in self._fields]

    def get_primary_items(self):
        '''Returns items of primary field'''
        if self.primary_field_exists():
            return self._primary_field.get_items()
        else:
            return None


    @staticmethod
    def dicts_to_records(dicts):
        '''Returns iterable of records from iterable of dictionaries'''
        # Using map has advantage of using [record(dict_) for dict_ in dicts]
        # Map will save memory(uses iterators than just list)
        # 'dicts' can sometimes be large in Millions or Billions
        def dict_to_record(__dict):
            if not isinstance(__dict, dict):
                err_msg = "Instance of type 'dict' expected, not " +\
                     str(type(__dict))
                raise TypeError(err_msg)
            return record(__dict)
        return map(dict_to_record, dicts)

    @staticmethod
    def records_to_dicts(records):
        '''Returns iterable of dictionaries from iterable of records'''
        # This is not worth it as record is instance of 'dict'
        def record_to_dict(__dict):
            if not isinstance(__dict, dict):
                err_msg = "Instance of type 'dict' or 'record' expected, " +\
                     "not " + str(type(__dict))
                raise TypeError(err_msg)
            return record(__dict)
        return map(record_to_dict, records)


    @classmethod
    def fields_to_records(cls, 
    fields, 
    primary_field=None,
    common_record=record()):
        '''Returns records from fields'''
        if primary_field:
            if not isinstance(primary_field, field):
                type_name = primary_field.__class__.__name__
                err_msg = "Primary field should of type 'field' not '{}'."
                raise TypeError(err_msg.format(type_name))
            # Let primary field be the first one.
            # Important when calculating cartisian product.
            fields = sorted(fields, key=lambda f: f != primary_field)
        # Get fields item names(will act as keys)
        # 'item_name' is more suitable than 'name'(name of coulumn)
        field_names = [field.get_item_name() for field in fields]
        # Gets items of field into 2D list.
        fields_items = [field.get_items(True) for field in fields]
        # Uses prodius.product() to calculate cartesian product.
        for product_item in prodius.product(*fields_items):
            # product_item contain atleat item from each field.
            if not product_item:
                break
            # Creates empty record object
            record_ = record()
            # Adds common record items to record.
            record_.add_items(common_record)
            # Link back field items to their field names
            # and then add results to record
            for index, field_item in enumerate(product_item):
                # Adds field name and field item to record
                record_.add_item(field_names[index], field_item)
            # prodius.product() output can be larger.
            # Appending 'record' to collection is waste of memory.
            yield record_

    @classmethod
    def fields_to_records_primary_grouped(
        cls, 
        fields: Set[field], 
        primary_field: field, 
        common_record=record()):
        '''Returns records grouped by primary field items'''
        primary_items = primary_field.get_items()
        # other_fields needs to exclude primary field
        other_fields = fields.copy()
        other_fields.discard(primary_field)
        if primary_field not in fields:
            err_msg = "primary_field not in fields"
            raise exceptions.FieldNotFound(err_msg)
        if len(fields) == 1:
            records = cls.fields_to_records(
                fields, primary_field, common_record
            )
            # All items of primary record are treated as group
            yield records
        else:
            # Loop each of primary field items
            for primary_item in primary_items:
                # Creates field for primary field
                # Name of field is taken from primary field
                field = field(primary_field.get_name(), [primary_item])
                field.set_item_name(primary_field.get_item_name())
                # Merge the field with other fields
                fields = other_fields.union([field])
                # Creates records the fields
                records =  cls.fields_to_records(
                    fields, primary_field, common_record
                )
                yield records

    def records_primary_grouped(self):
        '''Returns records of table grouped by primary field items'''
        if self.primary_field_exists():
            return self.fields_to_records_primary_grouped(
                self._fields,
                self._primary_field,
                self._common_record
            )
        else:
            err_msg = "Primary field is required, but not found"
            raise exceptions.PrimaryfieldNotFound(err_msg)

    def set_common_record(self, record):
        '''Sets record with items to be shared by all records'''
        self._common_record = record
        

    def get_common_record(self):
        '''Gets record to be merged with each record'''
        return self._common_record

    def update_records(self):
        '''Updates table records to keep-up with fields'''
        self._records = self.fields_to_records(
            self._fields, 
            self._primary_field,
            self._common_record
        )

    def update(self):
        '''Updates table including its records'''
        # Theres nothing to be updated than just the records
        self.update_records()

    def __iter__(self) -> Iterator[record]:
        return iter(self.get_records())


class primary_table(table):
    '''Dynamically records based on primary field items'''
    def __init__(self, fields=[], fields_callback=lambda: []) -> None:
        super().__init__(fields)
        self._fields_callback = fields_callback

    # def primary_item_to_records(self, primary_item):
    #     '''Creates records from primary item'''
    #     if self._records_callable != None:
    #         # Create records from provided callable
    #         records =  self._records_callable(primary_item)
    #     else:
    #         # Creates field for primary field
    #         # Name of field is taken from primary field
    #         field = field(self._primary_field.get_name(), [primary_item])
    #         field.set_item_name(self._primary_field.get_item_name())
    #         # Get all other field excluding primary fileld
    #         other_fields = self._fields.difference([self._primary_field])
    #         # Merge the field with other fields
    #         fields = other_fields.union([field])
    #         # Creates records the fields
    #         records =  self.fields_to_records(
    #             fields, self.primary_field, self._common_record
    #         )
    #     return records

    # def primary_item_to_records(self, primary_item) -> Iterator[record]:
    #     if self._records_callable != None:
    #         # Call the prvided callable to get records from primary item
    #         return self._records_callable(primary_item, self._common_record)
    #     else:
    #         # Return empty iterator if callable not provided
    #         return iter([])

    def primary_item_to_fields(self, primary_item) -> Iterator[record]:
        return self._fields_callback(primary_item)

    def records_primary_grouped(self):
        if self.primary_field_exists():
            primary_field_name = self._primary_field.get_name()
            primary_field_item_name = self._primary_field.get_item_name()
            for primary_item in self._primary_field.get_items():
                # Get the fields to create records from
                fields = set(self.primary_item_to_fields(primary_item))
                # Primary field shouldnt be included(removed it)
                fields.discard(self._primary_field)
                # Uses table to convert the fields to records
                table_ = table(fields)
                # Create field for representing item
                item_field = field(primary_field_name, [primary_item])
                item_field.set_item_name(primary_field_item_name)
                # Now add the field to the table
                table_.add_field(item_field)
                # Provides table with common record
                table_.set_common_record(self._common_record)
                # Return records from table created from the fields
                yield table_.get_records()
        else:
            err_msg = "Primary field is required, but not found"
            raise exceptions.PrimaryfieldNotFound(err_msg)

    def update_records(self):
        '''Updates table records to keep-up with fields'''
        # Update records only if there are fields in table
        def records_callable():
            # Flattens primary grouped records
            for records in self.records_primary_grouped():
                for record in records:
                    yield record
        # Updates update records with with generator function
        self._records = records_callable()



class records_table(table):
    '''table class that allows setting of records'''
    def __init__(self, records=[]) -> None:
        '''Creates records_table instance'''
        super().__init__([])
        self.set_records(records)

    def update_records(self):
        # No need to update records as fields are not to be used.
        # But its worth it to add common record to each record.
        def callback(record: record):
            # Its better to modify copy of record
            record = record.copy()
            record.update(self._common_record)
            return record
        self._records = map(callback, self._records)

    def set_records(self, records: Iterator[record]):
        self._records = records
        # Its better to update records when setting records
        # than when getting records.
        self.update_records()

    def get_records(self):
        return self._records



def extract_record_primary_item(record, primary_field):
    '''Returns primary item from record'''
    field_name = primary_field.get_item_name()
    # Rember that record is instance of dict
    primary_item = record[field_name]
    return primary_item


def record_primary_included(record, primary_field, primary_field_items):
    '''Returns True if primary item of record is in primary_field_items'''
    primary_item = extract_record_primary_item(record, primary_field)
    return primary_item in primary_field_items


def records_to_item_names_map(
    records: Iterator[record], 
    unique=False):
    # Returns dictionary with item names and iterators
    item_names_map: Dict[str, List] = {}
    for record in records:
        for name, value in record.items():
            item_names_map[name] = item_names_map.get(name, [])
            if unique and value in item_names_map[name]:
                continue
            item_names_map[name].append(value)
    # Dict["item names": "Iterator"]
    return item_names_map


def records_to_fields(
    records: Iterator[record], 
    common_record=record(),
    fields_names_map: Dict[str, Any]={}, 
    unique=False):
    # Returns fields from records
    # fields_names_map: Dict["item_name", "field_name"]
    fields: List[field] = []
    item_names_map = records_to_item_names_map(records, unique=unique)
    for item_name, items in item_names_map.items():
        if item_name not in common_record:
            field_name = fields_names_map.get(item_name, item_name)
            field_ = field(field_name, items)
            field_.set_item_name(item_name)
            fields.append(field_)
    return fields

             



def records_to_table( 
    records: Iterator[record], 
    primary_field_name=None,
    common_record=record(),
    fields_names_map: Dict[str, Any]={}):
    '''Returns table object from iterator of records'''
    #fields_names_map: Dict["item_name", "field_name"]
    if primary_field_name == None:
        return records_table(records)
    else:
        fields = records_to_fields(
            records, 
            fields_names_map=fields_names_map,
            common_record=common_record,
            unique=True
        )
        table_ = table(fields)
        primary_field = table_.get_field_by_name(primary_field_name)
        table_.set_primary_field(primary_field)
        return table_

def dicts_to_records(dicts: Iterator[Dict]):
    '''Returns corresponding records objects from dictionaries(dict)'''
    return table.dicts_to_records(dicts)

def records_to_dicts(records: Iterator[record]):
    '''Returns corresponding 'dict' objects from records objects'''
    return table.records_to_dicts(records)

def dicts_to_table(
    dicts: Iterator[Dict], 
    primary_field_name=None,
    common_dict = dict(),
    fields_names_map: Dict[str, Any]={}):
    '''Returns table object from iterator of dictionaries(dict)'''
    records = dicts_to_records(dicts)
    common_record = record(common_dict)
    return records_to_table(
        records,
        primary_field_name=primary_field_name,
        common_record=common_record,
        fields_names_map=fields_names_map
    )


def json_to_table(
    file_path,
    primary_field_name=None,
    fields_names_map: Dict[str, Any]={}):
    '''Returns table object from json file'''
    with open(file_path, mode='r') as f:
        dicts = json.load(f)
        return dicts_to_table(
            dicts,
            primary_field_name=primary_field_name,
            fields_names_map=fields_names_map
        )

def csv_to_table_fp(
    fp: io.FileIO,
    primary_field_name=None,
    fields_names_map: Dict[str, Any]={},
    fieldnames: Sequence = None,
    restkey=None, 
    restval=None,
    dialect=...,
    delimiter: str = ",", 
    quotechar: str = None, 
    escapechar: str = None, 
    doublequote: bool = ...,
    lineterminator: str = "\n"
    ):
    '''Returns table object from csv file like object'''
    reader = csv.DictReader(
        fp,
        fieldnames=fieldnames,
        restkey=restkey,
        restval=restval,
        dialect=dialect,
        delimiter=delimiter,
        quotechar=quotechar,
        escapechar=escapechar,
        doublequote=doublequote,
        lineterminator=lineterminator,
    )
    return dicts_to_table(
        reader,
        primary_field_name=primary_field_name,
        fields_names_map=fields_names_map
    )


def csv_to_table(
    path, 
    primary_field_name=None,
    fields_names_map: Dict[str, Any]={},
    fieldnames: Sequence = None,
    restkey=None, 
    restval=None,
    dialect=...,
    delimiter: str = ",", 
    quotechar: str = None, 
    escapechar: str = None, 
    doublequote: bool = ...,
    lineterminator: str = "\n"):
    '''Returns table object from csv file in path'''
    # This function would read the whole csv into memory
    # Use csv_to_table_fp() if you dont want read whole csv to memory.
    with open(path) as fp:
        reader = csv.DictReader(
            fp,
            fieldnames=fieldnames,
            restkey=restkey,
            restval=restval,
            dialect=dialect,
            delimiter=delimiter,
            quotechar=quotechar,
            escapechar=escapechar,
            doublequote=doublequote,
            lineterminator=lineterminator,
        )
        # list(reader) reads the whole csv into memory
        return dicts_to_table(
            list(reader),
            primary_field_name=primary_field_name,
            fields_names_map=fields_names_map
        )



if __name__ == "__main__":
    usernames = ["david", "marry", "pearl"]*1
    passwords = ["1234", "0000", "th234"]

    # Creates fields for table
    usernames_col = field('usenames', usernames)
    # Sets key name to use in record key in table
    usernames_col.set_item_name("username")
    passwords_col = field('passwords', passwords)
    passwords_col.set_item_name("password")

    table = table()
    # Set common record to be shared by all records
    common_record = record()
    common_record.add_item("submit", "login")
    table.set_common_record(common_record)
    # Add fields to table
    table.add_field(usernames_col)
    table.add_field(passwords_col)
    # print the records with common record
    # Realise that the keys match ones set by set_item_name()
    print(list(table))
