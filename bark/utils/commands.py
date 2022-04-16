"""All commands to manipulate table 'bookmarks' in database 'bookmarks.db'. Business logic layer."""

from database_manager import DatabaseManager
from datetime import datetime
import sys
import requests

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
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmarks added!'


class ListBookmarksCommand:
    def __init__(self, order_by: str = 'date_added') -> None:
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class UpdateBookmarksCommand:
    def execute(self, data):
        db.update('bookmarks', {'id': data['id']}, data['update'])
        return 'Bookmarks updated!'


class DeleteBookmardCommand:
    def execute(self, id_condition):
        db.delete('bookmarks', {'id': id_condition})
        return 'Bookmark deleted!'


class ImportGitHubStarsCommand:
    def _extract_bookmark_info(self, repo):
        return {
            'title': repo['name'],
            'url': repo['html_url'],
            'notes': repo['description']
        }

    def execute(self, data):
        bookmarks_imported = 0

        github_username = data['github_username']
        next_page_of_results = f'https://api.github.com/users/{github_username}/starred'

        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={'Accept': 'application/vnd.github.v3.star+json'})
            next_page_of_results = stars_response.links.get('next',
                                                            {}).get('url')

            for repo_info in stars_response.json():
                repo = repo_info['repo']

                if data['preserve_timestamps']:
                    timestamp = datetime.strptime(repo_info['starred_at'],
                                                  '%Y-%m-%dT%H:%M:%SZ')
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(self._extract_bookmark_info(repo),
                                             timestamp=timestamp)

        return f'Imported {bookmarks_imported} bookmarks from starred repos!'


class QuitCommand:
    def execute(self):
        sys.exit()
