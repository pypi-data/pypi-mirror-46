import os
import sys
import sqlite3

# Remixed vgstash. This time I chose an individual file on purpose:
#
# * Only need a single module to interface with a game DB. That's awesome.
# * Keeps the backend separate from the UI, as intended.
# * SQLA and pandas are both too large and unwieldy for my intent, and deps
#   will need to be kept low if I want to be cross-platform. sqlite3's part of
#   the standard library, can't beat that.
# * GUI will be implemented in tkinter, Qt, and/or Kivy.

PROGRESS = {
    'unbeatable': 0,
    'new': 1,
    'playing': 2,
    'beaten': 3,
    'complete': 4,
}

OWNERSHIP = {
    'unowned': 0,
    'physical': 1,
    'digital': 2,
    'both': 3
}

DEFAULT_CONFIG = {
    'db_location': os.getenv('VGSTASH_DB_LOCATION', os.path.join(os.getenv('HOME', os.curdir), '.vgstash.db')),
    'progress': os.getenv('VGSTASH_DEFAULT_PROGRESS', PROGRESS['playing']),
    'ownership': os.getenv('VGSTASH_DEFAULT_OWNERSHIP', OWNERSHIP['physical'])
}

FILTERS = {
    'allgames': "SELECT * FROM games ORDER BY system, title ASC",
    'backlog':  "SELECT * FROM games WHERE ownership > 0 AND progress > 0 AND progress < 3 ORDER BY system, title ASC",
    'borrowing': "SELECT * FROM games WHERE ownership = 0 AND progress = 2 ORDER BY system, title ASC",
    'complete': "SELECT * FROM games WHERE progress = 4 ORDER BY system, title ASC",
    'digital': "SELECT * FROM games WHERE ownership = 2 ORDER BY system, title ASC",
    'done': "SELECT * FROM games WHERE progress > 2 ORDER BY system, title ASC",
    'incomplete': "SELECT * FROM games WHERE progress = 3 AND ownership > 0 ORDER BY system, title ASC",
    'new': "SELECT * FROM games WHERE progress = 1 ORDER BY system, title ASC",
    'notes': "SELECT * FROM games WHERE notes NOT LIKE '' ORDER BY system, title ASC",
    'owned': "SELECT * FROM games WHERE ownership > 0 ORDER BY system, title ASC",
    'physical': "SELECT * FROM games WHERE ownership = 1 ORDER BY system, title ASC",
    'playlog': "SELECT * FROM games WHERE ownership > 0 AND progress = 2 ORDER BY system, title ASC",
    'unowned': "SELECT * FROM games WHERE ownership = 0 ORDER BY system, title ASC",
}

def kvmatch(arg, dict_map, fallback):
    """
    Match arg against keys or values in dict_map, returning fallback if no match.

    This function performs a prefix-match against the keys in dict_map. Doing
    such iteration partially defeats the purpose of using a dictionary, but
    it offers considerable ease-of-use for the CLI and acts as a validation
    function that will always return a valid value ready for committing to the
    database.

    It is generalized to support any value that needs to be mapped to an
    integer, via the dict_map.
    """
    try:
        ret = int(arg)
    except TypeError:
        ret = fallback
    except ValueError:
        found = False
        for k in dict_map.keys():
            if k.startswith(arg):
                ret = dict_map[k]
                found = True
                break
        if not found:
            ret = fallback
    finally:
        if ret not in dict_map.values():
            ret = fallback
    return ret


def vtok(arg, dict_map):
    """
    Match an integer value to a key name in the mapping dictionary. Returns a
    string (the key name) if found, False if not found.
    """
    if isinstance(arg, int):
        for k, v in dict_map.items():
            if arg == v:
                return k
    elif isinstance(arg, str):
        for k, v in dict_map.items():
            if k.startswith(arg):
                return k
        return False


class DB(object):
    """
    The central class of vgstash. It handles everything relating to storing the
    game collection.
    """
    def __init__(self, path=DEFAULT_CONFIG['db_location']):
        """
        Initiates the DB object with a 'conn' attribute, which holds the SQLite
        connection. Additionally, the connection's 'row_factory' attribute is
        set to sqlite3.Row to allow for string *and* integer indexes. This value
        may be changed by the caller after the object is returned.
        """
        try:
            self.conn = sqlite3.connect(path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.OperationalError as e:
            print("{}: {}".format(e, path))
            exit()

    def add_filter(self, filter_name, stmt):
        """
        Adds a new filter keyword to the database. Note that values are passed
        directly in, with no escaping. Use with caution.

        'filter_name' is the name of your filter, and will be the 'name' key
        when viewed with list_filters(). usable via `vgscli list [filter name]`.
        'stmt' is a plain SELECT statement representing the SQLite VIEW.
        """
        if filter_name.startswith("sqlite_"):
            raise ValueError("Cannot create a filter with the 'sqlite_' prefix.")

        # The call to format() is needed because sqlite doesn't allow
        # parameterized view or table names. This may affect database
        # integrity, and may disappear in a later release.
        res = self.conn.execute("CREATE VIEW\
            IF NOT EXISTS \
            '{}'\
            AS\
            {}".format(filter_name, stmt))
        FILTERS[str(filter_name)] = str(stmt)
        return self.has_filter(filter_name)

    def add_game(self, game, update=True):
        """
        Adds a Game to the database. Returns True on success and False on
        failure.
        """
        if self.has_game(game) and update:
            return self.update_game(game, game)
        else:
            c = self.conn.execute("INSERT INTO games\
                    (title, system, ownership, progress, notes)\
                    VALUES\
                    (?, ?, ?, ?, ?)",
                    (game.title, game.system, game.ownership, game.progress, game.notes))
            self.conn.commit()
            return (c.rowcount > 0)

    def create_schema(self):
        """
        Initializes the database with this basic schema:

        games:
            title (TEXT)
            system (TEXT)
            ownership (INTEGER)
            progress (INTEGER)
            notes (TEXT)

        The schema is configured to use the 'title' and 'system' columns as
        primary keys, meaning it is impossible for two games with the same name
        and system to be present in the database.

        Additionally, create_schema will add the default set of filters, which
        are considered important for an ordinary vgstash DB.
        """
        # The UNIQUE clause ensures that no two games with the same title and
        # system are added to the database. An sqlite3.IntegrityError will be
        # raised when a match occurs; clients can decide how to handle it.
        #
        # The 'rowid' field is automatically generated by sqlite, and is thus
        # omitted. External modifications to the database should be done
        # through additional tables, and should reference the 'rowid' field to
        # get more exact data manipulation. Alternatively, use the *_filter
        # methods of this class to create custom reporting filters.
        try:
            self.conn.execute("CREATE TABLE\
                IF NOT EXISTS\
                games (\
                    title TEXT NOT NULL,\
                    system TEXT NOT NULL,\
                    ownership INTEGER NOT NULL DEFAULT 1,\
                    progress INTEGER NOT NULL DEFAULT 1,\
                    notes TEXT DEFAULT '',\
                    UNIQUE (title, system) ON CONFLICT ROLLBACK\
                )")
            # setup default filters while we're here
            for name, sql in sorted(FILTERS.items()):
                self.add_filter(name, sql)
            return True
        except sqlite3.OperationalError:
            print("Table already exists, skipping.")
            return False

    def delete_filter(self, filter_name):
        with self.conn:
            # try:
            self.conn.execute("DROP VIEW IF EXISTS '{}'".format(filter_name))
            return True
            # except:
            #     sys.exc_info()
            #     print("Could not remove filter '{}'.".format((filter_name))
        return False

    def delete_game(self, game):
        """
        Deletes a game from the database. Returns True on success and False
        on failure.
        """
        if self.has_game(game):
            c = self.conn.cursor()
            c.execute("DELETE FROM games\
                    WHERE title=? AND system=?",
                    (game.title, game.system))
            self.conn.commit()
            return True
        else:
            return False

    def get_game(self, title, system):
        """
        Fetches a game's information from the database. Returns a Game object.
        """
        stmt = "SELECT * FROM games WHERE title=? AND system=?"
        res = self.conn.execute(stmt, (title, system)).fetchone()
        if bool(res):
            return Game(res['title'], res['system'], res['ownership'], res['progress'], res['notes'])

    def has_game(self, game, fuzzy=False):
        """
        Returns whether or not the game is in the database.

        game  - The Game object to search for.
        fuzzy - Fuzzy search, using internal 'LIKE' and replacing the game
                title's spaces with '%' characters. Defaults to False.
        """
        if fuzzy:
            game.title = "%".join(['', game.title.replace(" ", "%"), ''])
            stmt = "SELECT * FROM games WHERE title LIKE ? AND system=?"
        else:
            stmt = "SELECT * FROM games WHERE title=? AND system=?"

        res = self.conn.execute(stmt, (game.title, game.system)).fetchone()
        # res is None if there isn't a match, which evaluates to False
        return bool(res)

    def has_filter(self, filter_name):
        return filter_name in self.list_filters().keys() \
                and filter_name in FILTERS

    def list_filters(self):
        """
        Provides an iterable of filter names and their associated SELECT
        statements.
        """
        # The 'sqlite_master' table is a built-in.
        # This returns an iterable of sqlite3.Row, which can be accessed
        # similarly to a dictionary.
        res = self.conn.execute(\
                "SELECT name,sql\
                FROM sqlite_master\
                WHERE\
                type='view'\
                ORDER BY name ASC").fetchall()
        ret = {}
        for row in res:
            ret[row['name']] = row['sql']
        # Be sure to sync with internal representation
        FILTERS = ret
        return ret

    def list_games(self, filter='allgames'):
        """
        Return a list of games that meet the filter criteria.

        If the filter exists, it returns a list of sqlite3.Row objects. If the
        filter does not exist, it returns False. If no filter is specified, it
        will return a list of all games in the database.
        """
        if filter not in FILTERS.keys():
            return False
        else:
            return self.conn.execute(FILTERS[filter]).fetchall()

    def update_filter(self, filter_name, stmt):
        """
        Updates a filter's definition within the database.

        SQLite does not have a way to update VIEWs directly, so this is a
        convenience function to make updating possible.
        """
        try:
            self.delete_filter(filter_name)
            self.add_filter(filter_name, stmt)
            return True
        except:
            return False

    def update_game(self, target, source):
        """
        Look for target in the database and (if found) update it with source's
        information. Returns True on success and False on failure.

        The same Game object may be passed as both target and source to update
        a given game's values within the database.
        """
        # don't update unless it exists
        if self.has_game(target):
            c = self.conn.cursor()
            # TODO: do this better
            c.execute("UPDATE games\
                    SET title=?, system=?, ownership=?, progress=?, notes=?\
                    WHERE title=? AND system=?",
                    (source.title, source.system, source.ownership, source.progress, source.notes, target.title, target.system))
            self.conn.commit()
            return (c.rowcount > 0)
        else:
            return False


class Game(object):
    """The core data structure of vgstash."""
    def __init__(self, title, system,
                 ownership=DEFAULT_CONFIG['ownership'],
                 progress=DEFAULT_CONFIG['progress'],
                 notes=""):

        self.title = title
        self.system = system
        self.ownership = kvmatch(ownership, OWNERSHIP, DEFAULT_CONFIG['ownership'])
        self.progress = kvmatch(progress, PROGRESS, DEFAULT_CONFIG['progress'])
        self.notes = notes
