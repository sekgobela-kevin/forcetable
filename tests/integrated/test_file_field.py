__package__ = "tests.integrated"

import unittest
import itertools

from .setup_tests import SetUpTable
import forcetable


class TestFileFieldCommon(SetUpTable, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.usernames_file = open(self.usernames_file_path)
        self.passwords_file = open(self.passwords_file_path)

    def setup_fields(self):
        # Create passwords and usernames fields
        self.usernames_field = forcetable.file_field(
            "usernames", self.usernames_file_path
        )
        self.passwords_field = forcetable.file_field(
            "passwords", self.passwords_file_path
        )
        # Set items name 
        self.usernames_field.set_item_name("username")
        self.passwords_field.set_item_name("password")

    def tearDown(self):
        self.usernames_field.close()
        self.passwords_field.close()

        self.usernames_file.close()
        self.passwords_file.close()


    def test_get_items(self):
        self.assertListEqual(
            list(self.passwords_field.get_items()), self.passwords
        )

    def test_for_exaustion(self):
        # Test if username field does not get exausted after being looped
        first_usernames = list(self.usernames_field.get_items())
        second_usernames = list(self.usernames_field.get_items())
        self.assertGreater(len(first_usernames), 0)
        self.assertListEqual(first_usernames, second_usernames)

    def test_with_itertools_product(self):
        #_product = itertools.product(
        #    self.usernames_file,
        #    self.usernames_file
        #)
        _product = itertools.product(
           self.usernames_field.get_items(),
           self.usernames_field.get_items()
        )

        _expected_product = itertools.product(
            self.usernames,
            self.usernames
        )
        # Its expected for product of file_field with itself to be small.
        # That has todo with file position being changed while
        # calculating cartesian product.
        # Thats similar to trying to calculate cartesian product file object
        # with itself.
        # There will be problems with file positions.

        # Setting read_all=True on field solves the problem.
        # That causes whole file lines to be read to list.
        # Which avoid having to direcly read from file object. 

        # This assert tests for restriction.
        self.assertLess(len(list(_product)), len(list(_expected_product)))

    def test_with_itertools_product_second(self):
        _product = itertools.product(
            self.usernames_field.get_items(),
            self.passwords_field.get_items()
        )

        _expected_product = itertools.product(
            self.usernames,
            self.passwords
        )
        # The two products are expected to be equal.
        # usernames_field and passwords_field have opened different
        # file objects.
        # There wont be problems with file positions being changed
        # in unwanted way.
        self.assertListEqual(list(_product), list(_expected_product))


if __name__ == '__main__':
    unittest.main()