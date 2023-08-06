#!/usr/bin/env bash

# This is a set of helper bash functions that are too small for their own file,
# but useful enough to be worth `source`ing in your bashrc.

# Faster general searching
function vgsrc() {
	case $# in
		1)
			vgstash list | grep -iE "$1"
			;;
		2)
			vgstash list "$1" | grep -iE "$2"
			;;
		*)
			echo "usage: vgsrc [game name]"
			echo " or    vgsrc [view name] [game name]"
			echo
			echo "Ex: vgsrc physical Borderlands"
			;;
	esac
}

# Faster adding
function vgadd() {
	vgstash add "$@"
}
