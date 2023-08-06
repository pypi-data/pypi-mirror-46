import os
import pytest
import vgstash
import sqlite3

def test_config():
    assert vgstash.DEFAULT_CONFIG['db_location']
    assert vgstash.DEFAULT_CONFIG['progress'] in vgstash.PROGRESS.values()
    assert vgstash.DEFAULT_CONFIG['ownership'] in vgstash.OWNERSHIP.values()

@pytest.fixture(scope="module")
def vgstash_db():
    vgstash.DEFAULT_CONFIG['db_location'] = '.vgstash.db'
    yield vgstash.DB(vgstash.DEFAULT_CONFIG['db_location'])
    os.remove(vgstash.DEFAULT_CONFIG['db_location'])

def test_game_min():
    game = vgstash.Game("test_game1", "system3")
    assert isinstance(game, vgstash.Game)
    assert isinstance(game.title, str)
    assert isinstance(game.system, str)
    assert isinstance(game.ownership, int)
    assert isinstance(game.progress, int)
    assert isinstance(game.notes, str)
    assert game.ownership in vgstash.OWNERSHIP.values()
    assert game.progress in vgstash.PROGRESS.values()

def test_game_ownership():
    game = vgstash.Game("test_game2", "system3", 1)
    assert isinstance(game, vgstash.Game)
    assert isinstance(game.title, str)
    assert isinstance(game.system, str)
    assert isinstance(game.ownership, int)
    assert isinstance(game.progress, int)
    assert isinstance(game.notes, str)
    assert game.ownership in vgstash.OWNERSHIP.values()
    assert game.progress in vgstash.PROGRESS.values()

def test_game_ownership_str():
    game = vgstash.Game("test_game2", "system3", 'd')
    assert isinstance(game, vgstash.Game)
    assert isinstance(game.title, str)
    assert isinstance(game.system, str)
    assert isinstance(game.ownership, int)
    assert isinstance(game.progress, int)
    assert isinstance(game.notes, str)
    assert game.ownership in vgstash.OWNERSHIP.values()
    assert game.progress in vgstash.PROGRESS.values()

def test_game_progress():
    game = vgstash.Game("test_game3", "system3", progress=1)
    assert isinstance(game, vgstash.Game)
    assert isinstance(game.title, str)
    assert isinstance(game.system, str)
    assert isinstance(game.ownership, int)
    assert isinstance(game.progress, int)
    assert isinstance(game.notes, str)
    assert game.ownership in vgstash.OWNERSHIP.values()
    assert game.progress in vgstash.PROGRESS.values()

def test_game_progress_str():
    game = vgstash.Game("test_game3", "system3", progress='c')
    assert isinstance(game, vgstash.Game)
    assert isinstance(game.title, str)
    assert isinstance(game.system, str)
    assert isinstance(game.ownership, int)
    assert isinstance(game.progress, int)
    assert isinstance(game.notes, str)
    assert game.ownership in vgstash.OWNERSHIP.values()
    assert game.progress in vgstash.PROGRESS.values()

def test_game_notes_no_own_or_progress():
    game = vgstash.Game("test_game4", "system3", notes="Hello world")
    assert isinstance(game, vgstash.Game)
    assert isinstance(game.title, str)
    assert isinstance(game.system, str)
    assert isinstance(game.ownership, int)
    assert isinstance(game.progress, int)
    assert isinstance(game.notes, str)
    assert game.ownership in vgstash.OWNERSHIP.values()
    assert game.progress in vgstash.PROGRESS.values()

def test_game_full():
    game = vgstash.Game("test_game5", "system3", 'b', 2, "Blah")
    assert isinstance(game, vgstash.Game)
    assert isinstance(game.title, str)
    assert isinstance(game.system, str)
    assert isinstance(game.ownership, int)
    assert isinstance(game.progress, int)
    assert isinstance(game.notes, str)
    assert game.ownership in vgstash.OWNERSHIP.values()
    assert game.progress in vgstash.PROGRESS.values()

def test_db(vgstash_db):
    assert isinstance(vgstash_db.conn, sqlite3.Connection)

def test_db_create_schema(vgstash_db):
    assert vgstash_db.create_schema()

def test_db_add_game(vgstash_db):
    game = vgstash.Game("db_add_game", "system")
    assert vgstash_db.add_game(game)
    assert vgstash_db.has_game(game)

def test_db_add_game_ownership(vgstash_db):
    game = vgstash.Game("db_add_game_ownership", "system2", 'p')
    assert vgstash_db.add_game(game)
    assert vgstash_db.has_game(game)

def test_db_add_game_notes(vgstash_db):
    game = vgstash.Game("db_add_game_notes", "system2", '-', '-', 'my notes')
    assert vgstash_db.add_game(game)
    assert vgstash_db.has_game(game)

def test_db_update_game(vgstash_db):
    oldgame = vgstash.Game("db_add_game", "system")
    newgame = vgstash.Game("db_update_game", "system")
    if vgstash_db.has_game(oldgame):
        assert vgstash_db.update_game(oldgame, newgame)
        assert vgstash_db.has_game(newgame)

def test_db_delete_game(vgstash_db):
    game = vgstash.Game("db_delete_game", "system2")
    vgstash_db.add_game(game)
    assert vgstash_db.delete_game(game)

def test_db_list_games(vgstash_db):
    res = vgstash_db.list_games()
    assert isinstance(res, list)
    assert isinstance(res[0], sqlite3.Row)

def test_db_list_games_not_found(vgstash_db):
    res = vgstash_db.list_games("derp")
    assert res == False

def test_db_add_filter(vgstash_db):
    assert vgstash_db.add_filter("db_add_filter", "SELECT * FROM games WHERE system = 'system2'")
    assert vgstash_db.has_filter("db_add_filter")

def test_db_update_filter(vgstash_db):
    assert vgstash_db.update_filter("db_add_filter", "SELECT * FROM games WHERE system='system'")
    assert vgstash_db.has_filter("db_add_filter")
    assert "'system'" in vgstash.FILTERS["db_add_filter"]

def test_db_delete_filter(vgstash_db):
    assert vgstash_db.delete_filter("db_add_filter")

def test_db_list_filters(vgstash_db):
    assert len(vgstash_db.list_filters()) > 0
