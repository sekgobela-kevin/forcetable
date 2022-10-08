from forcetable._record  import record

import unittest


class TestRecordCommon():
    def setUp(self):
        self.items = {
            "Name": "John Doe",
            "Age": 80,
            "Country": "USA",
            "Race": "European"
        }
        self.record = record(self.items)
        self.empty_record = record()

    def test_add_item(self):
        self.record.add_item("Gender", "Male")
        self.assertIn("Gender", self.record)
    
    def test_add_items(self):
        self.record.add_items({"Gender": "Male"})
        self.assertEqual(len(self.record), len(self.items)+1)

    def test_set_items(self):
        self.empty_record.set_items(self.items)
        self.assertEqual(len(self.empty_record), len(self.items))

    def test_get_item(self):
        self.assertEqual(self.record.get_item("Name"), self.items["Name"])

    def test_get_items(self):
        self.assertEqual(self.record.get_items(), self.items)


class TestRecord(TestRecordCommon, unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()