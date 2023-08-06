#!/usr/bin/env bash

# system-search.sh: List all games from a specific system

# Accepts either one argument (the system name), or the filter to send
# to vgstash and then the system name.

# Set options for improved robustness
set -o errexit
set -o pipefail
set -o nounset

show_help() {
	cat <<-FOOBAR
	system-search.sh [filter] SYSTEM

	filter:   The filter to pass to vgstash. "all" by default
	SYSTEM:   The value in the System column to search for. Accepts
	          awk-style regex.

	For example, to check which games for the NES that are in progress,
	you would do:

	system-search.sh incomplete NES
FOOBAR
}

case $# in
	1)
		filter="all"
		system="$1"
		;;
	2)
		filter="$1"
		system="$2"
		;;
	*)
		show_help
		exit 0
		;;
esac

vgstash list "${filter}" | awk -F '|' "\$3 ~ \"${system}\""
