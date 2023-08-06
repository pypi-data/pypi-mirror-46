#!/bin/sh

DEBUG=0
if [ "$1" = "--debug" ]
then
	DEBUG=1
	shift
	echo "WARNING: debug mode is slower and thus timestamps may be less precise." >&2
fi

if [ -z "$1" ]
then
	echo "Usage: $0 [--debug] <command line and args>"
	echo
	echo "This will catch stdout and stderr and send them"
	echo "to walt server as log lines."
	echo
	echo "By default the stdout and stderr of the command line"
	echo "are not echo-ed locally (for performance reasons)."
	echo "Use --debug to enable them."
	exit
fi

if ! which "$1" >/dev/null
then
	echo "Either $1 cannot be found in PATH or its execution is not allowed."
	exit
fi

fifo_prefix="/tmp/$$_fifo."
stream_prefix="$(basename "$1").$$.std"

fifo_stdout="${fifo_prefix}out"
fifo_stderr="${fifo_prefix}err"

on_exit()
{
	rm $fifo_stdout $fifo_stderr
}

# create the FIFOs and setup an EXIT handler
# to delete them at the end
mkfifo $fifo_stdout $fifo_stderr
trap on_exit EXIT

# request walt-node-daemon to monitor these 2 FIFOs
# and pass what's coming in as logs to the server
echo MONITOR ${stream_prefix}out $fifo_stdout > /var/lib/walt/logs.fifo
echo MONITOR ${stream_prefix}err $fifo_stderr > /var/lib/walt/logs.fifo

if [ "$DEBUG" = "0" ]
then
	# start the command with stdout and stderr redirected
	# to the FIFOs
	"$@" >$fifo_stdout 2>$fifo_stderr
else
	# start the command with 
	# - stdout duplicated both on stdout and on the related fifo.
	# - stderr duplicated both on stderr and on the related fifo.
	# note: use of fd 6 allows to avoid merging stderr and stdout
	# before processing stderr.
	{ { "$@" | tee $fifo_stdout 1>&6; } 2>&1 | tee $fifo_stderr 1>&2; } 6>&1
fi

