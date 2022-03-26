"""All commands to manipulate table 'bookmarks' in database 'bookmarks.db'. Business logic layer."""

from database_manager import DatabaseManager
from datetime import datetime
import sys

db = DatabaseManager(
    'bookmarks.db')  # Simply importing this module won't run this line.

#NOTE: Why not naming all the <execute> method below as <_execute>? They're not going to be called explicitly.


class CreateBookmarksTableCommand:
    def execute(self):
        """Create a table called 'bookmarks' in the database.
        """
        db.create_table(
            'bookmarks', {
                'id': 'integer primary key autoincrement',
                'title': 'text not null',
                'url': 'text not null',
                'notes': 'text',
                'date_added': 'text not null'
            })


class AddBookmarkCommand:
    def execute(self, data):
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmarks added!'


class ListBookmarksCommand:
    def __init__(self, order_by: str = 'date_added') -> None:
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmardCommand:
    def execute(self, id_condition):
        db.delete('bookmarks', {'id': id_condition})
        return 'Bookmark deleted!'


class QuitCommand:
    def execute(self):
        sys.exit()
