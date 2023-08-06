# vgstash - a place to stash your game collection

If you love video games, you've probably amassed a collection of them, across
many different systems; physical, digital, and everything in-between. At some
point, a player may want to know a few key pieces of information that may steer
their gaming. These questions are great for quelling boredom and keeping a
gaming backlog manageable:

* Which games do I own?
* Which games have I beaten or completed?
* Which games do I need to beat?
* What was the note I left for X game?

vgstash seeks to answer these type of questions in a simple and extensible way.

# Installation

vgstash is available via `pip`:

~~~
pip install [--user] vgstash
~~~

Please note that vgstash is under heavy development at present. Do not install
unless you are interested in helping its development.

# Concept

The core concept of vgstash is the game itself. Every game in a player's
collection has a few important attributes, all of which are obvious to the
player:

* Title
* System
* Ownership
    * unowned
    * physical
    * digital
    * both
* Progress
    * unbeatable
    * new
    * playing
    * beaten
    * complete
* Notes

Think of any game that you have a history with. Let's say it was a game you
bought as part of a Humble Bundle, but haven't started playing yet. Internally,
vgstash tracks it somewhat like this:

```
.--------------------------------------------------------.
| Title                  | System | Ownership | Progress |
|------------------------+--------+-----------+----------|
| FTL: Faster Than Light | Steam  | digital   | new      |
'--------------------------------------------------------'
```

This is the bare minimum information you need to meaningfully track a video 
game in your collection.

# Command Line Usage

vgstash comes with a command line client of the same name, which gives you
high level commands to manipulate the database with. It's the reference
implementation for a vgstash client.

If you wanted to add the above game to your collection, you'd do it like this:

```bash
$ vgstash add 'FTL: Faster Than Light' Steam d n
Added FTL: Faster Than Light for Steam. You digitally own it and you have not started it.
```

Pretty easy, huh? Each game and system added to vgstash is free-form and can be
tuned to match the user's preferences.

## Quoting Game Titles

A note on characters: some shells treat certain characters differently. The most 
common ones you'll run into are punctuation, like single quotes ('), double 
quotes (") and exclamation points (!). You'll need to search your shell's manual 
for "character escaping" to get the details.

Let's take a few game titles that might be problematic for a shell, and add them 
to vgstash. These examples assume you're using bash (the Bourne Again SHell) or 
something comparable.

First: a title with single quotes and exclamation points:

```bash
$ vgstash add "Eek! It's a Bomb!" Android d n
```

Double quotes are useful for quoting just about any game title.

Next is a little more insidious: a title with two (or more) exclamation points:

```bash
$ vgstash add 'Mario Kart: Double Dash!!' GCN p n
```

Note that we're using single quotes; if we used double quotes, then the `!!` 
would expand to the last command entered into the shell, creating
`Mario Kart: Double Dash<your last command here>`. Quite different from what
you'd expect!

But what if we, somehow, had both single quotes *and* sequential exclamation 
points? Single-quoted strings cannot escape a single quote character. Double 
quotes won't stop the `!!` expansion. Escaping the exclamation points retains 
the backslash; what is one to do? There are a few ways to tackle this one:

```bash
# The easy way
$ vgstash add $'Some title\'s crazy!!' PC d n

# The hard way
$ vgstash add Some\ title\'s\ crazy\!\! PC d n

# The exotic way
$ vgstash add "Some title"\''s crazy!!' PC d n
```

The `$'text'` form is handy when you need to use double and/or single quotes 
alongside exclamation points, or you can just escape every special character 
(including space) as needed.

The "exotic" one takes advantage of the shell's built-in string concatenation 
and the ability to mix quoting styles. First we have `Some title` in double 
quotes; then an escaped single quote for literal output; then `s crazy!!` in 
single quotes to avoid the `!!` expansion.

The last option is to disable the feature (history expansion) altogether, though 
you'll miss out on nice stuff like `sudo !!`. In bash, it's disabled with `set
+H` or `set +o histexpand`. Change `+` to `-` to turn it back on when you're 
done.

These tips may not work in all shells, so try using `echo` to print the title
you want before trying to add it in vgstash! If you accidentally add a game this
way, copy the title that's output in the success message and paste it into your
delete command:

```bash
# Let's say I used 'ls' last
$ vgstash add "my game!!" PC d n
Added my gamels for PC. You own it digitally and it's new.
$ vgstash delete "my gamels" PC
Removed my gamels for PC from your collection.
```

That's it! This is something that the shell does before vgstash begins 
processing its arguments, so please don't report any bugs dealing with quoting.

# Commands

vgstash has a fairly small set of commands:

* add
* delete
* export
* import
* list
* notes
* update

The power is in the `list` command. vgstash comes with a set of default filters 
that allow you to reason about your game collection. For example, this command 
will show you every game marked "playing" that you also own in some way:

```bash
$ vgstash list -w 40 playlog
Title       |  System  | Own | Progress
----------------------------------------
Crashmo     |   3DS    |   D |   P
Ever Oasis  |   3DS    | P   |   P
Fire Emblem |   3DS    | P   |   P
Monster Hun |   3DS    |   D |   P
Box Pusher  |   DSi    |   D |   P
Glow Artisa |   DSi    |   D |   P
Dark Souls  |   PS3    | P   |   P
```

Consult `vgstash --help` for further usage information.

# Roadmap

These are planned for the full 0.3 release:

* command line interface finished
* Match feature-set with `master`
* Iron out any initial bugs on Windows and Mac (testers welcome!)

Goals planned for the 0.4 release:

* import and export with JSON

Goals planned for the 0.5 release:

* some sort of GUI (Tk and Qt are current candidates)

Goals planned for the 1.0 release:

* Kivy-based interface (to release on Android via F-Droid)

If this interests you, please [e-mail me](mailto:zlg+vgstash@zlg.space).
