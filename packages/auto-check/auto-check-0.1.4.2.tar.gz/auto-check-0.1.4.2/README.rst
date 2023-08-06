==========================
Automatic Check In And Out
==========================
|PyPI version|

`auto-check` is a tool used to check in & out in the remote server automaticly. Set a crontab task that run this script in the remote linux system.The check in & out system was a little bit funny, because this api(url)'s network package was captured while using my iPhone App to perform check in & out actions, and I check in & out successfully via these api with cookies, etc.

Installation
------------
`pip3 install auto-check`

Usage
-----
The following setting will perform an action that `cio.py` was executed at 8:30 and 19:30 on every workday.

.. code-block:: console

    30 8,19 * * * auto-check

FAQ
---
- Why performs login aciton before check in & out?

  In order to avoid the cookies being out of date, though that case didn't appear. But when I open the iPhone App, the lonin action was performed, and the latest cookie was received by the App.

.. |PyPI version| image:: https://badge.fury.io/py/auto-check.svg
    :target: https://badge.fury.io/py/auto-check