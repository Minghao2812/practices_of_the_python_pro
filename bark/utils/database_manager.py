import sqlite3
from typing import Union


class DatabaseManager:
    def __init__(self, database_filename: str) -> None:
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, query: str, values: Union[list, tuple] = None):
        with self.connection:  # Using with keyword to roll back when error occurs. (sqlite3's feature)
            cursor = self.connection.cursor()
            cursor.execute(query, values or [])
            # When values is None, keep []; otherwise, keep values.
            return cursor  # cursor stores results.

    def create_table(self, table_name: str, columns: dict):
        """
        Parameters
        ----------
        :table_name: table name should not have .db suffix.

        :columns: column name as dictionary key, data type as dictionary value.
        """
        columns_with_types = [
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items()
        ]
        self._execute(
            f'''CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_with_types)});'''
        )

    def add(self, table_name: str, data: dict):
        """
        Original SQL parameter statement
        ------------
        INSERT INTO <table_name>
        (<column1>, <column2>, ...)
        VALUES (?, ?, ...);
        """
        column_names = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        self._execute(
            f'''INSERT INTO {table_name} ({column_names}) VALUES({placeholders});''',
            tuple(data.values()))

    def delete(self, table_name: str, criteria: dict):
        """
        Original SQL parameter statement
        ------------
        DELETE FROM <table_name>
        WHERE column1 = ? AND column2 = ?;

        Example
        -------
        delete('a_table', criteria={'column1': condition1, 'column2': condition2})
        """
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        # placeholders is a list like ['column1 = ?', 'column2 = ?']
        delete_criteria = ' AND '.join(placeholders)
        # delete_criteria is a string like 'column1 = ? AND column2 = ?'
        self._execute(f'''DELETE FROM {table_name} WHERE {delete_criteria};''',
                      tuple(criteria.values()))

    def select(
        self,
        table_name: str,
        order_by: str = None,
        criteria: dict = None,
    ):
        # criteria = criteria or {}
        query = f'SELECT * FROM {table_name}'

        if order_by:
            query += f' ORDER BY {order_by}'

        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'
            return self._execute(query, tuple(criteria.values()))

        return self._execute(query)

    def update(self, table_name: str, criteria: dict, data: dict):
        """
        Original SQL parameter statement
        ------------
        UPDATE <table_name>
        SET column0 = ?
        WHERE column1 = ? AND column2 = ?;
        """

        update_placeholders = [f'{column} = ?' for column in criteria.keys()]
        update_criteria = ' AND '.join(update_placeholders)

        data_placeholders = ', '.join(f'{key} = ?' for key in data.keys())

        values = tuple(data.values()) + tuple(criteria.values())
        #NOTE: this combination of criteria and data is amazing!

        self._execute(
            f'''UPDATE {table_name} SET {data_placeholders} WHERE {update_criteria};''',
            values)


if __name__ == '__main__':
    # Test DatabaseManager.update()
    db = DatabaseManager('bookmarks.db')
    print(db.select('bookmarks').fetchall())
    db.update('bookmarks', {'id': 1}, {'notes': 'TECH'})
    print(db.select('bookmarks').fetchall())
