'''
source: url - https://github.com/sekgobela-kevin/perock
        commit Hash - de476e23a5447b2eb7af8000637b449aab200f55

Author: Sekgobela Kevin
Date: October 2022
Languages: Python 3
'''


class field():
    '''Class for operating with field data. Column data  
    may include things like 'passwords', 'usernames', etc.'''
    def __init__(self, name: str, items, read_all=False):
        '''
        Creates field object
        
        --------------------
        name: str
            Name of field
        items: Iterator
            Iterator or callable returning items of field
        read_all: bool
            True if should read all items to memory at once.
        '''
        # Stores items of field, e.g 'passwords'
        self._items = items
        # Name of field
        self._name = name
        # Decides if items should be read to memory at once
        self._read_all = read_all
        # Name of each item of field
        # Name to use with each record, default: field name.
        self._item_name = name

        # If true then this field is primary field.
        self._primary = False

        if self._read_all:
            # Reads all items into list(read all)
            self._items = list(self._read_items())

    def set_name(self, name):
        '''Sets name of field, e.g 'usernames\''''
        self._name = name

    def set_item_name(self, name):
        '''Sets name/string to use within each item, default: field name'''
        self._item_name = name

    def _read_items(self):
        # Reads and returns items of field object
        # Realise that items may be exausated if in iterator.
        # This method may be called within __init__().
        if callable(self._items):
            return self._items()
        else:
            return self._items     

    def read_items(self):
        '''Reads and returns items of field object, items maybe exausted
        if they are from iterator.'''
        return self._read_items()


    def get_items(self):
        '''Returns items of field'''
        if (not callable(self._items)) or self._read_all:
            # Return items if items is not callable or 
            # self._read_all is True.
            return self._items
        else:
            return self.read_items()

    
    def get_name(self):
        '''Returns name of field, e.g 'usernames\''''
        return self._name

    def get_item_name(self):
        '''Returns name for item of field e.g username'''
        return self._item_name

    def set_primary(self):
        '''Sets the field as primary field'''
        self._primary = True

    def unset_primary(self):
        '''Unset field as primary field'''
        self._primary = False

    def is_primary(self):
        '''Returns True if field is primary field'''
        return self._primary

    def __iter__(self):
        return iter(self.get_items())


class file_field(field):
    '''Creates field from file path''' 
    def __init__(self, name:str, path, read_all=False):
        '''
        Creates file_field object
        
        ----------
        name: str
            Name of field
        path: str | bytes
            File path pointing to file with field items.
        read_all: bool
            True if should read all items to memory at once.
        '''
        self._path = path
        self._file = open(path)
        super().__init__(name, self._read_file_items, read_all)
        if read_all:
            # Close file handle as its content will be read at once.
            # It will never be used again.
            self._file.close()

    def _read_file_items(self):
        # Reads lines from file in path, returns generator.
        # This method may be called within __init__().
        for line in self._file:
            line_ = line.rstrip("\n")
            if line_:
                yield line_

    def _read_items(self):
        # Seeking may cause problems if file is used in multiple places.
        # This method may be called within __init__().
        self._file.seek(0)
        return super()._read_items()

    def close(self):
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()




if __name__ == "__main__":

    field_ = field("name", [1,2,3,4,5])
    print(field_.get_items())
    print(field_.get_items())