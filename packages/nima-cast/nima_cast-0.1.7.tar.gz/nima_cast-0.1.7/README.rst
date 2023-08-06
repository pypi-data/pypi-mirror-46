|Build Status| |made-with-python| |PyPI version nima-cast| |PyPI
license| |PyPI format| |PyPI pyversions| |PyPI status| |PyPI - License|
|GitHub| |Libraries.io dependency status for latest release| |PyPI -
Downloads| |GitHub issues| |GitHub last commit|

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

-  use ``--no-minio`` for

.. |Build Status| image:: https://travis-ci.com/nimamahmoudi/nima_cast.svg?token=J1fG4B1WmwjMJ3ZExa6D&branch=master
   :target: https://travis-ci.com/nimamahmoudi/nima_cast
.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
.. |PyPI version nima-cast| image:: https://badge.fury.io/py/nima-cast.svg
   :target: https://pypi.python.org/pypi/nima-cast/
.. |PyPI license| image:: https://img.shields.io/pypi/l/nima-cast.svg
   :target: https://pypi.python.org/pypi/nima-cast/
.. |PyPI format| image:: https://img.shields.io/pypi/format/nima-cast.svg
   :target: https://pypi.python.org/pypi/nima-cast/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/nima-cast.svg
   :target: https://pypi.python.org/pypi/nima-cast/
.. |PyPI status| image:: https://img.shields.io/pypi/status/nima-cast.svg
   :target: https://pypi.python.org/pypi/nima-cast/
.. |PyPI - License| image:: https://img.shields.io/pypi/l/nima-cast.svg
.. |GitHub| image:: https://img.shields.io/github/license/nimamahmoudi/nima_cast.svg
.. |Libraries.io dependency status for latest release| image:: https://img.shields.io/librariesio/release/pypi/nima-cast.svg
.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/nima-cast.svg
.. |GitHub issues| image:: https://img.shields.io/github/issues/nimamahmoudi/nima_cast.svg
.. |GitHub last commit| image:: https://img.shields.io/github/last-commit/nimamahmoudi/nima_cast.svg
