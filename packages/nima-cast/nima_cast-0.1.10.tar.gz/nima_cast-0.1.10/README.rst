nima_cast CLI
=============

Usage
=====

.. code:: bash

   $ nima_cast
   Welcome! Type ? to list commands. options: --no-minio and --show-debug

   (nima.cast) select
   INFO:pychromecast:Querying device status
   INFO:pychromecast:Querying device status
   [0] - Bedroom speaker
   [1] - Living Room TV
   Please choose an index: 1

   (nima.cast) list
   [ 0]-   example_video.mp4

   (nima.cast) play 0
   INFO:pychromecast.controllers:Receiver:Launching app CC1AD845

   (nima.cast) pause

   (nima.cast) goto 0:10:0

   (nima.cast) pause

   (nima.cast) stop

   (nima.cast) quit
   INFO:pychromecast:Quiting current app
   INFO:pychromecast.controllers:Receiver:Stopping current app 'CC1AD845'

   (nima.cast) exit

Commands
========

You can get a list of commands by enterring ``?``:

.. code:: bash

   (nima.cast) ?

   Documented commands (type help <topic>):
   ========================================
   EOF     exit  help  play  search  select  stream
   device  goto  list  quit  seek    stop

   Undocumented commands:
   ======================
   pause  resume

Look at the documentation for each of them by entering ``help CMD``:

.. code:: bash

   (nima.cast) help play
   play [num] starts playing the file specified by the number in results of list

Installation
============

Install using pip:

.. code:: bash

   $ pip install nima_cast

Upgrading:

.. code:: bash

   pip install nima_cast --upgrade

Minio Configuration
===================

On windows:

.. code:: bash

   set ACCESS_KEY=XXXXXXXXXXXXXXXXX
   set SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   set MINIO_SERVER=YOUR_MINIO_SERVER:9000

On ubuntu:

.. code:: bash

   export ACCESS_KEY=XXXXXXXXXXXXXXXXX
   export SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   export MINIO_SERVER=YOUR_MINIO_SERVER:9000

Running the app
===============

.. code:: bash

   $ nima_cast

Options
=======

-  use ``--no-minio`` for streaming purposes (no need to connect to
   minio).
-  use ``--show-debug`` to see debug messages from the cast.
