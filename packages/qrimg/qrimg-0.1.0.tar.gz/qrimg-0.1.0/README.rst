qrimg
=====

Generate QRCode Image


Install
-------

::

    pip install qrimg


Usage
-----

::

    C:\Code\qrimg>qrimg --help
    Usage: qrimg.py [OPTIONS] MESSAGE

    Options:
    -o, --output TEXT  Output file name.  [required]
    --help             Show this message and exit.

Example
-------

Use qrimg command generate an image contain information "Hello world".

::

    C:\Code\qrimg>qrimg -o hello.png "Hello world"

    C:\Code\qrimg>dir hello.png
    驱动器 C 中的卷是 Windows
    卷的序列号是 D012-B866

    C:\Code\qrimg 的目录

    2019/05/25  22:16               430 hello.png
                1 个文件            430 字节
                0 个目录 112,028,286,976 可用字节

The image preview:

.. image:: https://raw.githubusercontent.com/appstore-zencore/qrimg/master/hello.png
