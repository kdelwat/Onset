import csv

class Table():
    '''A Table is an object which represents a 2-dimensional CSV file. Both rows
    and columns can be accessed via their key as in a dictionary. This means that
    keys cannot appear as both a row and column label.'''

    def __init__(self, filename):
        self._internal_table = self.load_from_filename(filename)

    def load_from_filename(self, filename):
        '''Load a CSV file into a list of lists. The following CSV:
            ,a,b,c
           d,1,2,3
           e,4,5,6
           f,7,8,9
        would become the list:
           [['', 'a', 'b', 'c'],
            ['d', '1', '2', '3'] ...]'''
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            return [row for row in reader]

    def get_row(self, key):
        '''Gets a list containing all elements of the row specified by key.
        Returns a ValueError if the row doesn't exist.'''
        for row in self._internal_table:
            if row[0] == key:
                return row[1:]
        raise ValueError('Row not found')

    def get_column(self, key):
        '''Gets a list containing all elements of the column specified by key.
        Returns a ValueError if the column doesn't exist.'''
        for i, column in enumerate(self._internal_table[0]):
            if column == key:
                return [row[i] for row in self._internal_table[1:]]
        raise ValueError('Column not found')

    def available_rows(self):
        '''Get a list of row labels in table.'''
        return [row[0] for row in self._internal_table if row[0] != '']

    def available_columns(self):
        '''Get a list of column labels in table.'''
        return [column for column in self._internal_table[0] if column != '']

    def members(self):
        '''Returns a set of all unique members of the table that aren't:
            * a row or column label
            * None
            * an empty string.
        '''
        valid = []

        for row in self._internal_table[1:]:
            for item in row[1:]:
                if item is not None and item != '':
                    valid.append(item)

        return set(valid)

    def voiced(self, item):
        '''Return True if item is voiced.'''

        for column in self.available_columns():
            if column[0] == 'v':
                if item in self[column]: return True

        return False

    def unvoiced(self, item):
        '''Return True if item is unvoiced.'''

        for column in self.available_columns():
            if column[0] == 'u':
                if item in self[column]: return True

        return False

    def __contains__(self, item):
        '''Returns True if the item is present in the table, otherwise false.'''
        for row in self._internal_table:
            for value in row:
                if item == value: return True

        return False

    def __getitem__(self, key):
        '''Returns the row or column linked to the given key, accessed using
        subscript notation.'''
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        try:
            return self.get_row(key)
        except ValueError:
            try:
                return self.get_column(key)
            except ValueError:
                raise ValueError('Key not found in table')
