This script is a simple python framework to verify that each board for the
workshop is functioning correctly. It talks to the board over a USB serial
adapter, and does useful things like ensuring the kernel boots and that the
MAC address of the wired interface on the board is recorded.

Run the script like this:

# python3 burnin.py /dev/ttyUSB0 --verbose --username mikal --password lca2019 --board 1

This will populate an entry in boards.json with the relevant information for
the new board.
