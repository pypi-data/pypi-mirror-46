===========================================================
filestat
===========================================================

.. :_filestat https://github.com/zxalif/filestat/
.. _MIT: https://choosealicense.com/licenses/mit/

filestat_ A command line library for file monitoring.

    :Authors: Alif Jahan
    :Version: 0.2 of 05/05/2019

installation
-----------------------------------------------------------

Using ``pip``

.. code-block:: bash

    $ pip install filestat

To install using ``git`` just clone the repo

.. code-block:: bash

    $ git clone https://github.com/zxalif/filestat.git
    $ cd filestat
    $ python3 setup.py install

Usages
***********************************************************

There is two way to access filestat_ with command line or with python ``interpreter``.

1. using ``bash``

.. code-block:: bash

    $ python3 -m filestat -f filename.py
    Name:	filename.py
    Owner:	alif
    Group:	alif
    Size:	1045 bytes
    Update Time: 	Sunday, May 05, 2019 10:50:11.640795 PM
    Last Access:	Sunday, May 05, 2019 10:50:15.200863 PM
    Permissions:	644

2. Using ``interpreter``

.. code-block:: python

    >>> # to get file size
    >>> from filestat import utils
    >>> utils.get_size('path/to/file.py') # it returns the file size in byte
    123121
    >>>

License
--------------------------------------------------------

The program under Licensed MIT_.

**Documentations are under develop**
