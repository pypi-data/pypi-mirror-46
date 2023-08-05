firefox-shm
===========

Use tmpfs on /dev/shm to store firefox profile. No need root user rights. User can create, delete, and sync by his own.

Depencies: rsync


Installation
------------

- `installing <https://bitbucket.org/igraltist/firefox-shm/src/tip/INSTALL.rst>`_ 


Usage
-----

usage::
 
   usage: firefox-shm [-h] [-v] [-b] [-c] [-s] [-r]

-h      show this help message and exit
-v      make script noisily
-b      backup, created a copy in ~/.mozilla/firefox/ from current selected profile with suffix .archive
-c      create, move the current profile, and created the shm directory, and copy current selected profile, and symlink it
-s      sync, syncing the temporary profile the local profile
-r      restore, deleting the temporary profile and move archive profile to current profile


initialize it::
  
  firefox-shm --create

To do this automatic on login, here an example for Mate-desktop.

~/.config/autostart/firefox-shm.desktop::

  [Desktop Entry]
  Type=Application
  Exec=firefox-shm --create
  Hidden=false
  X-MATE-Autostart-enabled=true
  Name=firefox-shm


Do syncing the temporary profile back to local use crontab.

crontab -e::

  # do every 5 minutes a sync 
  */5 * * * * /usr/bin/firefox-shm --sync


Enough go back to default::

   firefox-shm --restore
