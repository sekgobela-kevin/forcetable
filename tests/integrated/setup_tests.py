import os
import forcetable


folder_path = os.path.split(os.path.abspath(__file__))[0]

class SetUpFixtures():
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures_path = os.path.join(folder_path, "fixtures")
        cls.passwords_file_path = os.path.join(
            cls.fixtures_path, 
            "passwords.txt"
        )
        cls.usernames_file_path = os.path.join(
            cls.fixtures_path, 
            "usernames.txt"
        )

        cls.json_file_path = os.path.join(cls.fixtures_path, "table.json")
        cls.csv_file_path = os.path.join(cls.fixtures_path, "table.csv")

        assert os.path.isfile(cls.passwords_file_path), cls.passwords_file_path
        assert os.path.isfile(cls.usernames_file_path), cls.usernames_file_path

        assert os.path.isfile(cls.json_file_path), cls.json_file_path
        assert os.path.isfile(cls.csv_file_path), cls.csv_file_path


        with open(cls.usernames_file_path) as usernames_file:
            with open(cls.passwords_file_path) as passwords_file:
                cls.usernames = [line.rstrip("\n") for line in usernames_file]
                cls.passwords = [line.rstrip("\n") for line in passwords_file]


    @classmethod
    def _get_files(cls, folder):
        file_paths = []
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                file_paths.append(file_path)
        return file_paths



class SetUpTable(SetUpFixtures):
    def setUp(self):
        self.setup_fields()
        self.setup_table()

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

    def setup_table(self):
        # enable_callable_product=False
        # Enables use of itertools.product() for cartesian product
        # It should be True if max_parallel_primary_tasks > 1
        self.table = forcetable.table()
        self.table.add_primary_field(self.usernames_field)
        self.table.add_field(self.passwords_field)


    def tearDown(cls):
        cls.usernames_field.close()
        cls.passwords_field.close()
