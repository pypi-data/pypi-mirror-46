#!/bin/bash

# WARNING: This script is a proof-of-concept and prone to errors. I don't want to hear any bitching if you use this and it blows up your game db. Back it up using `vgstash export -i foo.yaml` first.

# TODO: Refactor into multiple functions to improve error-handling.

# Set options for improved robustness
set -o errexit
set -o pipefail
set -o nounset

# Color escapes we'll use
norm="[0m"
BG="[1;32m" # Green
BC="[1;36m" # Cyan
BY="[1;33m" # Yellow

again=0
gamesrc=""

gid_check() {
	if [[ $# == 1 ]]; then
		case $game_id in
			''|*[!0-9]*)
				echo "ID is not a number."
				exit 1
				;;
			*)
				# Check for its existence
				result=$(vgstash list -r | grep "^${game_id}|")
				if [[ -n $result ]]; then
					echo "Found game ID '${game_id}'!"
				else
					echo "ID not found in vgstash database."
					exit 1
				fi
				;;
		esac
	fi
}

field_update() {
	echo -ne "${BG}Which field are you updating?\n[t]itle, [s]ystem, [o]wnership, [p]rogress: ${norm}"
	read game_field
	case $game_field in
		t|s)
			clause="string"
			;;
		o)
			clause="y/n"
			;;
		p)
			clause="[f]resh, [i]n-progress, [b]eaten, [c]omplete"
			;;
		*)
			echo "Invalid"
			exit 1
			;;
	esac
	echo -ne "${BG}What to?\n${clause}: ${norm}"
	read game_value
	# TODO: Put this into a loop/function
	echo "Running '${BC}vgstash update ${game_id} ${game_field} "${game_value}"${norm}'..."
	echo -ne "${BY}"
	vgstash update ${game_id} ${game_field} "${game_value}"
	echo -ne "${norm}"
	run_again
}

run_again() {
	echo -ne "${BG}Do you want to edit another game?${norm} "
	read again
	case $again in
		y|yes)
			main
			;;
		n|no)
			exit
			;;
		*)
			echo "Invalid. Try [y]es or [n]o."
			run_again
			;;
	esac
}

game_search() {
	if [[ $# == 0 ]]; then
		echo -ne "${BG}Game title to search for:${norm} "
		read gamesrc
	else
		gamesrc="$1"
	fi
	# Print the header first
	vgstash list | head -n 2
	vgstash list | grep -i "$gamesrc"
	# -ne omits the newline and accepts color escapes; handy!
	echo -ne "${BG}Which ID do you want to update?${norm} "
	read game_id
	echo "${game_id} selected."
	# Check to make sure $game_id is a number
	gid_check $game_id
	field_update $game_id
}

main() {
	case $# in
		0)
			game_search
			;;
		1)
			game_search "$1"
			;;
		*)
			echo "This script accepts zero or one arguments."
			exit
			;;
	esac
}

main "$*"
