dmon - A Super Simple Network Monitor
=====================================

About
-----

The title pretty much says it all. Set up dmon, and you'll have a simple
network status page showing your current ping to google (or another site
of your choosing), packet loss stats, and an up/down indicator for any
additional services (on your local network?) that you want to monitor.

The name dmon is a combination pun/acronym in that it can be pronounced
like daemon, but is also an acronym for "dungeon monitor" (where dungeon
is the name of the network that it was initially built for).

Setup
-----

Dependencies
  - Python 2.7
  - bottle.py
  - A running mongodb server
  - pymongo

After all dependencies are installed, copy all of the .sample files and rename
them without the .sample extension, and edit the files to match your setup.
A sample adapter.wsgi has been included, and should work with apache or nginx.