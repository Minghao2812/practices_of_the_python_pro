import os
from collections import OrderedDict

import commands


class Option:
    def __init__(self, name, command, prep_call=None) -> None:
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        # Print the prompt message after executing.
        message = self.command.execute(data) if data else self.command.execute(
        )  # In some commands, execute method requires arguments; others don't.
        print(message)

    def __str__(self) -> str:
        return self.name


def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    choice = input('Choose an option: ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice')
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data():
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False)
    }


def get_bookmark_data_for_update():
    bookmark_id = get_user_input('Enter a bookmark ID to update')
    field = get_user_input(
        'Enter the column to update (title, url, notes)').lower()
    new_value = get_user_input('Enter the update value')
    return {'id': bookmark_id, 'update': {field: new_value}}


def get_bookmark_id_for_deletion():
    return get_user_input('Enter a bookmark ID to delete')


def get_github_import_options():
    return {
        'github_username':
        get_user_input('GitHub username'),
        'preserve_timestamps':
        get_user_input('Preserve timestamps [Y/n]', required=False)
    }


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def loop():
    # Use OrderedDict to avoid misorder.
    options = OrderedDict()
    options['A'] = Option('Add a bookmark',
                          commands.AddBookmarkCommand(),
                          prep_call=get_new_bookmark_data)
    options['B'] = Option('List bookmarks by date',
                          commands.ListBookmarksCommand())
    options['T'] = Option('List bookmarks by title',
                          commands.ListBookmarksCommand(order_by='title'))
    options['U'] = Option('Update a bookmark',
                          commands.UpdateBookmarksCommand(),
                          prep_call=get_bookmark_data_for_update)
    options['D'] = Option('Delete a bookmark',
                          commands.DeleteBookmardCommand(),
                          prep_call=get_bookmark_id_for_deletion)
    options['G'] = Option('Import GitHub stars',
                          commands.ImportGitHubStarsCommand(),
                          prep_call=get_github_import_options)
    options['Q'] = Option('Quit', commands.QuitCommand())
    clear_screen()
    print_options(options)
    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()

    _ = input('Press ENTER to return to menu')


if __name__ == '__main__':
    print('Welcome to Bark!')
    commands.CreateBookmarksTableCommand().execute()
    while True:
        loop()
