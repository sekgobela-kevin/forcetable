__package__ = "tests.integrated"

import unittest

from .setup_tests import SetUpTable
import forcetable


class TestForceTableFunctions(SetUpTable, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dict_records = [
            {'password': '1234', 'username': 'Marry'}, 
            {'password': '1234', 'username': 'Bella'}, 
            {'password': '1234', 'username': 'Michael'}, 
            {'password': '0000', 'username': 'Marry'}, 
            {'password': '0000', 'username': 'Bella'}, 
            {'password': '0000', 'username': 'Michael'}, 
            {'password': 'th234', 'username': 'Marry'}, 
            {'password': 'th234', 'username': 'Bella'}, 
            {'password': 'th234', 'username': 'Michael'}
        ]

        # Creates table object
        self.setup_table()

        self.records = self.table.get_records()

    def setup_fields(self):
        # Column items
        self.usernames = ["Marry", "Bella", "Michael"]
        self.passwords = ["1234", "0000", "th234"]

        # Creates fields for table
        self.usernames_field = forcetable.field('usernames', self.usernames)
        self.usernames_field.set_primary()
        # Sets key name to use in record key in table
        self.usernames_field.set_item_name("username")
        self.passwords_field = forcetable.field('passwords', self.passwords)
        self.passwords_field.set_item_name("password")


    def setup_table(self):
        # Creates table object
        self.table = forcetable.table()
        # Set common record to be shared by all records
        #self.common_record = forcetable.Record()
        #self.common_record.add_item("submit", "login")
        #self.table.set_common_record(self.common_record)
        # Add fields to table
        self.table.add_field(self.usernames_field)
        self.table.add_field(self.passwords_field)

    def test_json_to_table(self):
        table = forcetable.json_to_table(self.json_file_path)
        self.assertIsInstance(table, forcetable.table)
        self.assertCountEqual(
            table.get_records(), self.table.get_records()
        )

    def test_csv_to_table_fp(self):
        with open(self.csv_file_path) as fp:
            table = forcetable.csv_to_table_fp(fp)
            self.assertIsInstance(table, forcetable.table)
            self.assertCountEqual(
                table.get_records(), self.table.get_records()
            )      

    def test_csv_to_table(self):
        table = forcetable.csv_to_table(self.csv_file_path)
        self.assertIsInstance(table, forcetable.table)
        self.assertCountEqual(
            table.get_records(), self.table.get_records()
        )

    def tearDown(cls):
        # Dont close fields as they dont have .close() method.
        pass


if __name__ == '__main__':
    unittest.main()