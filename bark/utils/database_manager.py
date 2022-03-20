import sqlite3
from typing import Union


class DatabaseManager:
    def __init__(self, database_filename) -> None:
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, query: str, values: Union[list, tuple] = None):
        with self.connection:  # Using with keyword to roll back when error occurs.
            cursor = self.connection.cursor()
            cursor.execute(query, values or [])
            # When values is None, keep []; otherwise, keep values.
            return cursor  # cursor stores results.

    def create_table(self, table_name: str, columns: dict):
        columns_with_types = [
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items()
        ]
        self._execute(
            f'''CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_with_types)});'''
        )

    def add(self, table_name: str, data: dict):
        column_names = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        self._execute(
            f'''INSERT INTO {table_name} ({column_names}) VALUES({placeholders});''',
            tuple(data.values()))

    def delete(self, table_name: str, criteria: dict):
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(f'''DELETE FROM {table_name} WHERE {delete_criteria};''',
                      tuple(criteria.values()))

    def select(self,
               table_name: str,
               criteria: dict = None,
               order_by: str = None):
        # criteria = criteria or {}
        query = f'SELECT * FROM {table_name}'

        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'

        if order_by:
            query += f' ORDER BY {order_by}'

        return self._execute(query, criteria.values())