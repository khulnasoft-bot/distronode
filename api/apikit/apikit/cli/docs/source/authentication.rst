.. _authentication:

Authentication
==============

To authenticate to API, include your username and password in each command invocation as shown in the following examples:

.. code:: bash

    CONTROLLER_USERNAME=alice CONTROLLER_PASSWORD=secret api jobs list
    api --conf.username alice --conf.password secret jobs list
