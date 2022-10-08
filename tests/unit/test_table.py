import unittest

from forcetable._table import (
    table, 
    primary_table, 
    records_table
)

from forcetable._record import record
from forcetable._field import field


from forcetable import _table


class TestTableSetUp():
    def setUp(self):
        # Column items
        self.usernames = ["Marry", "Bella", "Michael"]
        self.passwords = ["1234", "0000", "th234"]

        # Creates fields for table
        self.usernames_field = field('usernames', self.usernames)
        self.usernames_field.set_primary()
        # Sets key name to use in record key in table
        self.usernames_field.set_item_name("username")
        self.passwords_field = field('passwords', self.passwords)
        self.passwords_field.set_item_name("password")

        # Creates table object
        self.create_table_objects()

        self.dict_records = [
            {'password': '1234', 'submit': 'login', 'username': 'Marry'}, 
            {'password': '1234', 'submit': 'login', 'username': 'Bella'}, 
            {'password': '1234', 'submit': 'login', 'username': 'Michael'}, 
            {'password': '0000', 'submit': 'login', 'username': 'Marry'}, 
            {'password': '0000', 'submit': 'login', 'username': 'Bella'}, 
            {'password': '0000', 'submit': 'login', 'username': 'Michael'}, 
            {'password': 'th234', 'submit': 'login', 'username': 'Marry'}, 
            {'password': 'th234', 'submit': 'login', 'username': 'Bella'}, 
            {'password': 'th234', 'submit': 'login', 'username': 'Michael'}
        ]

    def create_table_objects(self):
        # Creates table object
        self.table = table()
        # Set common record to be shared by all records
        self.common_record = record()
        self.common_record.add_item("submit", "login")
        self.table.set_common_record(self.common_record)
        # Add fields to table
        self.table.add_field(self.usernames_field)
        self.table.add_field(self.passwords_field)

        # table object without Fields
        self.empty_table = table()


class TestTableCommon(TestTableSetUp):
    def setUp(self):
        super().setUp()

    def test_set_primary_field(self):
        self.empty_table.set_primary_field(self.usernames_field)
        self.assertIn(self.usernames_field, self.empty_table.get_fields())

    def test_primary_field_exists(self):
        self.assertTrue(self.table.primary_field_exists())
        self.assertFalse(self.empty_table.primary_field_exists())
        self.empty_table.add_field(self.passwords_field)
        # passwords_field is not primary field
        self.assertFalse(self.empty_table.primary_field_exists())


    def test_add_field(self):
        self.empty_table.add_field(self.passwords_field)
        self.assertIn(self.passwords_field, self.empty_table.get_fields())
        self.empty_table.add_field(self.usernames_field)
        # Primary field exists as self.usernames_field is primary field
        self.assertTrue(self.empty_table.primary_field_exists())

        

    def test_add_primary_field(self):
        self.empty_table.add_primary_field(self.passwords_field)
        self.assertIn(self.passwords_field, self.empty_table.get_fields())
        self.assertTrue(self.empty_table.primary_field_exists())


    def test_get_primary_fields(self):
        self.assertCountEqual(self.table.get_primary_fields(), 
        [self.usernames_field])
        self.assertCountEqual(self.empty_table.get_primary_fields(), [])

    def test_get_primary_field(self):
        self.assertEqual(self.table.get_primary_field(), self.usernames_field)
        self.assertEqual(self.table.get_primary_field(), self.usernames_field)

    def test_get_fields(self):
        self.assertCountEqual(self.table.get_fields(), [self.usernames_field, 
        self.passwords_field])
        self.assertCountEqual(self.empty_table.get_fields(), [])

    def test_get_other_fields(self):
        primary_field = self.table.get_primary_field()
        other_fields = self.table.get_fields().difference([primary_field])
        self.assertCountEqual(self.table.get_other_fields(), other_fields)
        self.assertCountEqual(self.empty_table.get_other_fields(), [])

    def test_get_field_by_name(self):
        self.assertEqual(
            self.table.get_field_by_name("usernames"),
            self.usernames_field
        )
        with self.assertRaises(Exception):
            # Theres no field with name 'username'
            self.table.get_field_by_name("username")

    def test_get_field_by_item_name(self):
        self.assertEqual(
            self.table.get_field_by_item_name("username"),
            self.usernames_field
        )
        with self.assertRaises(Exception):
            # Theres no field with item name 'usernames'
            self.table.get_field_by_item_name("usernames")

    def test_get_records(self):
        self.assertCountEqual(self.table.get_records(), self.dict_records)
        self.assertCountEqual(self.empty_table.get_records(), [])


    def test_get_field_names(self):
        self.assertCountEqual(self.table.get_field_names(), ["passwords", 
        "usernames"])
        self.assertCountEqual(self.empty_table.get_field_names(), [])

    def test_get_item_names(self):
        self.assertCountEqual(self.table.get_item_names(), ["password", 
        "username"])
        self.assertCountEqual(self.empty_table.get_item_names(), [])

    def test_get_fields_items(self):
        self.assertCountEqual(self.table.get_fields_items(), [self.passwords, 
        self.usernames])
        self.assertCountEqual(self.empty_table.get_fields_items(), [])

    def test_get_primary_items(self):
        self.assertEqual(self.table.get_primary_items(), self.usernames)
        self.assertEqual(self.empty_table.get_primary_items(), None)


    def test_dicts_to_records(self):
        records = list(self.table.dicts_to_records(self.dict_records))
        self.assertIsInstance(records[0], record)
        self.assertEqual(len(records), len(self.dict_records))

    def test_records_to_dicts(self):
        records = list(self.table.dicts_to_records(self.dict_records))
        dicts = list(self.table.records_to_dicts(records))
        self.assertIsInstance(records[0], dict)
        self.assertEqual(len(records), len(dicts))


    def test_fields_to_records(self):
        records = self.table.dicts_to_records(self.dict_records)
        fields = [self.usernames_field, self.passwords_field]
        fields_records = self.table.fields_to_records(
            fields, common_record=self.common_record,
        )
        self.assertCountEqual(fields_records, records)
        self.assertCountEqual([], [])

    def test_set_common_record(self):
        self.empty_table.set_common_record(self.common_record)
        self.assertEqual(self.empty_table.get_common_record(), 
        self.common_record)

    def test_get_common_record(self):
        self.assertEqual(self.empty_table.get_common_record(), record())
        self.assertEqual(self.table.get_common_record(), self.common_record)

    def test_update_records(self):
        # Hard to test(shouldnt be public method)
        pass

    def test_update(self):
        # Hard to test(shouldnt be public method)
        pass



class TestPrimaryTableCommon(TestTableCommon):
    @classmethod
    def primary_item_to_records(
            cls,
            primary_item, 
            primary_field, 
            fields, 
            common_record):
        fields = set(fields)
        field = field(primary_field.get_name(), [primary_item])
        field.set_item_name(primary_field.get_item_name(True))
        # Get all other field excluding primary fileld
        other_fields = fields.difference([primary_field])
        # Merge the field with other fields
        fields = other_fields.union([field])
        # Create also table with records
        table = table(fields)
        table.set_common_record(common_record)
        return table
    
    def create_table_objects(self):
        def fields_callable(primary_item):
            # This is just for demostation
            # It doesnt matter if primary column is included.
            # primary column will be removed on after function call
            return [self.passwords_field]
        # Creates table object
        self.table = primary_table(fields_callback=fields_callable)
        # Set common record to be shared by all records
        self.common_record = record()
        self.common_record.add_item("submit", "login")
        self.table.set_common_record(self.common_record)
        # Add fields to table
        self.table.add_field(self.usernames_field)
        self.table.add_field(self.passwords_field)

        # table object without Fields
        self.empty_table = primary_table()

    def test_get_records(self):
        self.assertEqual(
            len(list(self.table.get_records())), len(self.dict_records)
        )
        with self.assertRaises(Exception):
            # Primary field is missing
            self.assertCountEqual(self.empty_table.get_records(), [])


class TestRecordsTableCommon(TestTableCommon):
    def create_table_objects(self):
        super().create_table_objects()
        # Get records from previous table
        records = self.table.get_records()

        # Creates table object
        self.table = records_table()
        # Set records from the other table into this table
        self.table.set_records(records)
        # Set common record to be shared by all records
        self.common_record = record()
        self.common_record.add_item("submit", "login")
        self.table.set_common_record(self.common_record)
        # Add fields to table
        self.table.add_field(self.usernames_field)
        self.table.add_field(self.passwords_field)

        # table object without Fields
        self.empty_table = table()


class TestFunctions(TestTableSetUp, unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.fields = [self.usernames_field, self.passwords_field]
        self.records = list(self.table.get_records())

        self.record = record({'password': '1234', 'submit': 'login', 
        'username': 'Bella'})
        self.record2 = record({'password': 'th234', 'submit': 'login', 
        'username': 'Marry'})


    def test_extract_record_primary_item(self):
        record_item = _table.extract_record_primary_item(self.record, 
        self.usernames_field)
        self.assertEqual(record_item, 'Bella')
        record_item = _table.extract_record_primary_item(self.record2, 
        self.usernames_field)
        self.assertEqual(record_item, 'Marry')


    def test_record_primary_included(self):
        is_included = _table.record_primary_included(self.record, 
        self.usernames_field, self.usernames_field.get_items())
        self.assertTrue(is_included)

        is_included = _table.record_primary_included(self.record, 
        self.usernames_field, self.passwords_field.get_items())
        self.assertFalse(is_included)

    def test_records_to_item_names_map(self):
        item_names_map = _table.records_to_item_names_map(self.records)
        self.assertCountEqual(
            set(item_names_map["username"]), set(self.usernames)
        )
        self.assertCountEqual(
            set(item_names_map["password"]), set(self.passwords)
        )

    def test_records_to_fields(self):
        fields = _table.records_to_fields(self.records, self.common_record)
        self.assertEqual(len(list(fields)), 2)
        fields = _table.records_to_fields(self.records)
        self.assertEqual(len(list(fields)), 3)

    def test_records_to_table(self):
        records = _table.records_to_table(self.records)
        self.assertCountEqual(records, self.records)
        records =  _table.records_to_table(
            self.records,
            "usernames", 
            fields_names_map = {
                "username": "usernames", 
                "passwords": "passwords"
            }
        )
        self.assertCountEqual(records, self.records)



class TestTable(TestTableCommon, unittest.TestCase):
    pass

class TestPrimaryTable(TestPrimaryTableCommon, unittest.TestCase):
    pass

class TestRecordsTable(TestRecordsTableCommon, unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()