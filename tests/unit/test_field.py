from forcetable._field import field

import unittest



class TestFieldCommon():
    def setUp(self):
        self.items = ["Marry", "Bella", "Paul", "Michael"]
        self.field = field("names", self.items)

    def test_set_name(self):
        self.field.set_name("peoples_names")
        self.assertEqual(self.field.get_name(), "peoples_names")

    def test_set_item_name(self):
        self.field.set_item_name("name")
        self.assertEqual(self.field.get_item_name(), "name")

    def test_read_items(self):
        self.assertEqual(self.field.read_items(), self.items)

    def test_get_items(self):
        self.assertEqual(self.field.get_items(), self.items)
    
    def test_get_name(self):
        self.assertEqual(self.field.get_name(), "names")

    def test_get_item_name(self):
        field_name = self.field.get_name()
        # Field item name is same as field name if not set.
        self.assertEqual(self.field.get_item_name(), field_name)
        # field name should be returned when field item name not set
        # and force is True.
        self.field.set_item_name("item-name")
        self.assertEqual(self.field.get_item_name(), "item-name")

    def test_set_primary(self):
        self.field.set_primary()
        self.assertTrue(self.field.is_primary())

    def test_unset_primary(self):
        self.field.set_primary()
        self.field.unset_primary()
        self.assertFalse(self.field.is_primary())

    def test_is_primary(self):
        self.field.set_primary()
        self.assertTrue(self.field.is_primary())
        self.field.unset_primary()
        self.assertFalse(self.field.is_primary())


class TestField(TestFieldCommon, unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()