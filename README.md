# forcetable
Forcetable library creates fields which are then used to create table
with records. Table is created from cartesian product of fields but records 
can also be used to create table. Think of this table as table created from
cartesian product not from columns and rows.

Its too common in bruteforce to calculate cartesian product while also 
link the output with existing objects. Forcetable takes away the need to 
calculate cartesian product yourself letting you focus on what matters.

> Table can also be created from json and csv files.


### Installing
Forcetable can be installed pip with in your command-line application.
```bash
pip install forcetable
```

### Usage
It all start with creating field to use with table.  
Field needs a name and items that field should contain like usernames.
```python
import forcetable

usernames = forcetable.field("usernames", ["Ben", "Jackson", "Marry"])
passwords = forcetable.field("passwords", range(3))
```

Items of field do not have to be in iterables but can in callable. Using callable like function allows large items to be used when calculating 
cartesian product without problems.

See [here](https://github.com/sekgobela-kevin/prodius) for more.
```python
import forcetable

usernames = forcetable.field("usernames", ["Ben", "Jackson", "Marry"])
# Passwords are now in function.
passwords = forcetable.field("passwords", lambda: range(10**10))
```


Items of field can written into memory in case they are in iterator which
may be exausated after use.
```python
import forcetable

passwords = forcetable.field("passwords", range(3), read_all=True)
print(passwords.get_items()) # (0, 1, 2)
```

Another great field is file field which reads text files for items. File 
contents wount be written to memory even when calculating cartisian
product of fields.

This library [prodius](https://github.com/sekgobela-kevin/prodius) will 
handle everything to ensure file is never written to memory.
```python
import forcetable

usernames = forcetable.field_field("usernames", "usernames.txt")
passwords = forcetable.field_field("passwords", "passwords.txt")
```


Table can be easily be created from items which will result in table containg
records.
```python
import forcetable

usernames = forcetable.field("usernames", ["Ben", "Jackson", "Marry"])
passwords = forcetable.field("passwords", range(3))
# Fields to use when creating table
fields = [usernames, passwords]

# Now create table from fields
table = forcetable.table(fields)
# Loops through records
for record in table:
    print(record)
# {'passwords': 0, 'usernames': 'Ben'}
# {'passwords': 0, 'usernames': 'Jackson'}
# {'passwords': 0, 'usernames': 'Marry'}
# {'passwords': 1, 'usernames': 'Ben'}
# {'passwords': 1, 'usernames': 'Jackson'}
```
> Fields can have different size of items.

Table can also contain primary field or common record which will be shared 
by all records of table.  
Primary field will only be iterated once and is the main field which 
influence order of records.  
Common record will have its items added to each table record.
```python
# Creating table using existing fields.
table = forcetable.table(fields)
# Sets primary field(also adds the field)
table.set_primary_field(usernames)
# Sets common record
common_record = forcetable.record({"submit": "login"})
table.set_common_record(common_record)
# Loops through records
for record in table:
    print(record)
# {'submit': 'login', 'usernames': 'Ben', 'passwords': 0}
# {'submit': 'login', 'usernames': 'Ben', 'passwords': 1}
# {'submit': 'login', 'usernames': 'Ben', 'passwords': 2}
# {'submit': 'login', 'usernames': 'Jackson', 'passwords': 0}
```

Key names with with each record of table is influced by table field.  
Fields allow to set name to be used within records created from then.
```python
import forcetable

usernames = forcetable.field("usernames", ["Ben", "Jackson", "Marry"])
passwords = forcetable.field("passwords", range(3))
# Corresponding record: {'usernames': 'Ben', 'passwords': 0}

usernames.set_item_name("username")
passwords.set_item_name("password")
# Corresponding record: {'username': 'Ben', 'password': 0}
```

Table can also be created from records, dictionary(dict), json and csv files.
```python
import forcetable

# Table from records
record1 = forcetable.record({'passwords': 0, 'usernames': 'Ben'})
record2 = forcetable.record({'passwords': 1, 'usernames': 'Jackson'})
table = forcetable.records_table([record1, record2])
# Also this one works.
table = forcetable.records_to_table([record1, record2])

# Table from dictionaries(list of dict)
dict1 = {'passwords': 0, 'usernames': 'Ben'}
dict2 = {'passwords': 1, 'usernames': 'Jackson'}
#table = forcetable.dicts_to_table([dict1, dict2])

# Table from csv and json files.
# Json needs to be in table like structure, [{}, {}, {}].
# Field names will be extracted from the files.
table = forcetable.csv_to_table("sample.csv")
table = forcetable.json_to_table("sample.json")
```
> record is valid dict and support all its features.

Here are some useful methods for record.
```python
record = forcetable.record({'name': 'Ben', 'gender': 'Male'})
record.add_item('race', 'Hispanic') # Adds single item to record
record.add_items({'age': 24, 'country': 'Canada'}) # Adds multiple items
record.get_item('race') # Gets item by its name
record.get_items() # Gets items in form of dict.
```

Here are some useful methods for field.
```python
usernames = forcetable.field("usernames", ["Ben", "Jackson", "Marry"])
usernames.get_items() # Gets items of field
usernames.get_name() # Gets name of field
usernames.get_item_name() # Gets name to use within records
usernames.set_item_name("username") # Sets name to use within records

usernames.set_primary() # Sets field as primary field
usernames.unset_primary() # Unset field as primary field
usernames.is_primary() # True if field is primary field
```

Here are some useful methods for table.
```python
table = forcetable.csv_to_table("sample.csv")
table.add_field(usernames) # Adds single field to table
table.add_field(usernames) # Adds multiple fields to table

table.get_records() # Gets records of table
table.get_fields() # Gets fields of table

table.get_other_fields() # gets fields excluding primary field.
table.set_primary_field(usernames) # Sets primary field
table.get_primary_field() # Gets primary field of table(None if not exists)
table.primary_field_exists() # Checks if primary field exists

table.get_field_by_name("usernames") # Gets field with name
table.get_field_by_item_name("username") # Gets field with item name.
```


### Inspired by:
- [perock](https://github.com/sekgobela-kevin/perock)
- [prodius](https://github.com/sekgobela-kevin/prodius)

### License
Forcetable is open source under conditions of 
[MIT license](https://github.com/sekgobela-kevin/forcetable/blob/main/LICENSE).