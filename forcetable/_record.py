'''
source: url - https://github.com/sekgobela-kevin/perock
        commit Hash - de476e23a5447b2eb7af8000637b449aab200f55

Author: Sekgobela Kevin
Date: October 2022
Languages: Python 3
'''


class record(dict):
    '''Class for operating with record data. Row data represents
    records to be sent to target, e.g 'password' and 'username'.'''
    def __init__(self, items={}) -> None:
        '''
        Creates record object from dictionary
        Parameters
        ----------
        items: Dict
            (optional) Dictionary/map with record items
        '''
        super().__init__(items)

    def add_item(self, name, value):
        '''Adds item to record'''
        self[name] = value
    
    def add_items(self, items):
        '''Adds items to record'''
        self.update(items)

    def set_items(self, items):
        '''Sets/overides record items with specified items'''
        self.clear()
        self.update(items)

    def get_item(self, name):
        '''Gets value of item with provided name'''
        return self.get(name)

    def get_items(self):
        '''Gets items of record in form of dict'''
        return dict(self)