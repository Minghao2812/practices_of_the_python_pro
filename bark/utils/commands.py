"""All commands to manipulate table 'bookmarks' in database 'bookmarks.db'. Business logic layer."""

from database_manager import DatabaseManager
import datetime
import sys

db = DatabaseManager('bookmarks.db')


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
        return db.select('bookmarks', order_by=self.order_by)


class DeleteBookmardCommand:
    def execute(self, id_condition):
        db.delete('bookmarks', {'id': id_condition})
        return 'Bookmark deleted!'


class QuitCommand:
    def execute(self):
        sys.exit()
