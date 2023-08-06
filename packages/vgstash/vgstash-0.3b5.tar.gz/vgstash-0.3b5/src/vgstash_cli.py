import vgstash
import sqlite3
import click
import os
import subprocess
import sys
import tempfile
import yaml
import json

# Click also has this, but it doesn't support a fallback value.
from shutil import get_terminal_size

def get_db():
    """Fetch a vgstash DB object from the default location.

    Change DEFAULT_CONFIG['db_location'] before calling this function
    to alter behavior."""
    return vgstash.DB(vgstash.DEFAULT_CONFIG['db_location'])


@click.group('vgstash')
def cli():
    pass


@cli.command()
def init():
    db = get_db()
    click.echo("Initializing the database...")
    if db.create_schema():
        click.echo("Schema created.")
    else:
        raise sqlite3.OperationalError("Cannot create schema.")


def row_format(row, width, header):
    """
    Prints a row from the result set into a nice table.
    """
    # The magic number comes from:
    #    3 chars per separator (9 chars total)
    #    8 chars for "System" (so there's an additional space on each side)
    #    3 chars for "Own"
    #    9 chars for "Progress" and an additional space
    #    Total is 29 characters
    twidth = int(width) - 29
    if header == True:
        click.echo("{:<{w}s} | {:^8s} | {:^3s} | {}".format(
            "Title",
            "System",
            "Own",
            "Progress",
            w=twidth)
        )
        click.echo("-" * int(width))

    titlestr = "{: <{w}s}".format(row['title'][:twidth], w=twidth)
    systemstr = "{: ^8s}".format(row['system'][:8])
    # unowned, physical, digital, both
    ownltr = [' ', 'P', '  D', 'P D']
    ownstr = "{: <3s}".format(ownltr[row['ownership']])
    progltr = {
        0: '',
        1: 'N',
        2: 'P',
        3: 'B',
        4: 'C'
    }
    progstr = "{}".format((" " * (row['progress'] - 1) * 2) + progltr[row['progress']])
    print(" | ".join((titlestr, systemstr, ownstr, progstr)))


@cli.command('add')
@click.argument('title', type=str)
@click.argument('system', type=str)
@click.argument('ownership', type=str, required=False, default=vgstash.DEFAULT_CONFIG['ownership'])
@click.argument('progress', type=str, required=False, default=vgstash.DEFAULT_CONFIG['progress'])
@click.argument('notes', type=str, required=False, default="")
def add(title, system, ownership, progress, notes):
    db = get_db()
    game = vgstash.Game(title, system, ownership, progress, notes)
    try:
        db.add_game(game, update=False)
        own_clause = (
            "do not own",
            "physically own",
            "digitally own",
            "digitally and physically own",
        )
        progress_clause = (
            "cannot beat",
            "haven't started",
            "are playing",
            "have beaten",
            "have completed",
        )
        note_clause = "" if len(game.notes) == 0 else " It also has notes."
        click.echo("Added {} for {}. You {} it and {} it.{}".format(
            game.title,
            game.system,
            own_clause[game.ownership],
            progress_clause[game.progress],
            note_clause,
        ))
    except sqlite3.IntegrityError as e:
        print(e)
        click.echo("Couldn't add game.")


@cli.command('list')
@click.argument('filter', type=click.Choice(vgstash.FILTERS.keys()), required=False, default="allgames")
@click.option('--raw', '-r', is_flag=True, show_default=True, default=False, help="Output raw, pipe-delimited lines")
@click.option('--width', '-w', type=str, required=False, default=get_terminal_size(fallback=(80,24)).columns, help="The width of the table to output, in characters.")
def list_games(filter, raw, width):
    db = get_db()
    res = db.list_games(filter)
    first_pass = True
    # res can be False if the filter doesn't exist, but Click should catch it
    # and spit out an error before this function even starts.
    for r in res:
        if 'notes' in r.keys() and len(r['notes']) > 0:
            notes = r['notes'].replace('\n', '\\n')
            notes = notes.replace('\r', '\\r')
        else:
            notes = ''
        if raw:
            click.echo("|".join((
                r['title'],
                r['system'],
                str(r['ownership']),
                str(r['progress']),
                notes
            ))
            )
        else:
            row_format(r, width, first_pass)
            first_pass = False


@cli.command('delete')
@click.argument('title', required=True)
@click.argument('system', required=True)
def delete_game(title, system):
    db = get_db()
    target_game = vgstash.Game(title, system)
    if db.delete_game(target_game):
        click.echo("Removed {} for {} from your collection.".format(title, system))
    else:
        click.echo("That game does not exist in your collection. Please try again.")


@cli.command('update')
@click.argument('title', required=True)
@click.argument('system', required=True)
@click.argument('attr', type=click.Choice(['title', 'system', 'ownership', 'progress']), required=True)
@click.argument('val', required=True)
def update_game(title, system, attr, val):
    # TODO: Consider namedtuple as a solution
    db = get_db()
    target_game = db.get_game(title, system)
    if attr == 'ownership':
        val = vgstash.vtok(val, vgstash.OWNERSHIP)
    if attr == 'progress':
        val = vgstash.vtok(val, vgstash.PROGRESS)
    updated_game = vgstash.Game(
        val if attr == 'title' else target_game.title,
        val if attr == 'system' else target_game.system,
        val if attr == 'ownership' else target_game.ownership,
        val if attr == 'progress' else target_game.progress,
        target_game.notes
    )
    if db.update_game(target_game, updated_game):
        click.echo("Updated {} for {}. Its {} is now {}.".format(title, system, attr, val))
    pass


@cli.command('notes')
@click.argument('title', required=True)
@click.argument('system', required=True)
@click.option('--edit', '-e', is_flag=True, default=False)
def notes(title, system, edit):
    db = get_db()
    target_game = db.get_game(title, system)
    if edit:
        with tempfile.NamedTemporaryFile() as tmpfile:
            tmpfile.write(target_game.notes.encode("UTF-8"))
            tmpfile.flush()
            process = subprocess.run([os.getenv("EDITOR", "vim"), tmpfile.name])
            tmpfile.flush()
            tmpfile.seek(0)
            note_arr = []
            for line in tmpfile:
                note_arr.append(line.decode("UTF-8").rstrip("\r\n"))
            target_game.notes = "\n".join(note_arr)
            db.update_game(target_game, target_game)
        if process.returncode == 0:
            click.echo("Notes for {} on {} have been updated!".format(target_game.title, target_game.system))
        else:
            click.echo("Couldn't find an editor for notes. Check the EDITOR environment variable and try again.")
    else:
        if len(target_game.notes) > 0:
            click.echo("Notes for {} on {}:".format(target_game.title, target_game.system))
            click.echo()
            click.echo(target_game.notes)
        else:
            click.echo("No notes for {} on {}.".format(target_game.title, target_game.system))


@cli.command("import")
@click.option("--format", "-f", type=click.Choice(["yaml", "json"]), required=False, default="yaml")
@click.option("--update", "-u", is_flag=True, default=False, help="Overwrite existing games with the file's data")
@click.argument("filepath",
                type=click.Path(
                    readable=True,
                    resolve_path=True,
                    dir_okay=False,
                    file_okay=True),
                default=sys.stdin,
                required=False,
                )
def import_file(format, filepath, update):
    """
    Import game data from an external file matching the chosen format.

    The default format is YAML.

    Available formats:

    * JSON
    * YAML
    """
    with open(filepath) as fp:
        if format == "yaml":
            data = yaml.safe_load(fp)
        if format == "json":
            data = json.load(fp)
    db = get_db()
    count = len(data)
    for game in data:
        try:
            db.add_game(
                vgstash.Game(
                    game["title"],
                    game["system"],
                    game["ownership"],
                    game["progress"],
                    game["notes"]
                ),
                update=update
            )
        except sqlite3.IntegrityError as e:
            # skip games that already exist
            count -= 1
    if count > 0:
        click.echo("Successfully imported {} games from {}.".format(count, filepath))
    else:
        click.echo("Couldn't import any games. Is the file formatted correctly?")


@cli.command("export")
@click.option("--format", "-f", type=click.Choice(["yaml", "json"]), required=False, default="yaml")
@click.argument("filepath",
                type=click.Path(
                    exists=False,
                    readable=True,
                    writable=True,
                    resolve_path=True,
                    dir_okay=False,
                    file_okay=True),
                default=sys.stdout,
                required=False,
                )
def export_file(format, filepath):
    """
    Export the game database to a file written in the chosen format.

    The default format is YAML.

    Available formats:

    * JSON
    * YAML
    """
    db = get_db()
    data = db.list_games()
    game_set = []
    # Time to re-read the master branch's code
    for game in data:
        g = {}
        for field in game.keys():
            g.update({field: game[field]})
        game_set.append(g)
    with open(filepath, "w") as fp:
        if format == "yaml":
            yaml.dump(game_set, fp, default_flow_style=False,
                             indent=4, allow_unicode=True)
        if format == "json":
            json.dump(game_set, fp, allow_nan=False, indent=1, skipkeys=True, sort_keys=True)
    if len(game_set) > 0:
        click.echo("Successfully exported {} games to {}.".format(len(game_set), filepath))
    else:
        click.echo("Could not export any games; have you made sure your collection has games in it?")

