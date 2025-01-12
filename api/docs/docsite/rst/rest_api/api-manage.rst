.. _ag_manage_utility:

The *api-manage* Utility
-------------------------------

.. index:: 
   single: api-manage

The ``api-manage`` utility is used to access detailed internal information of API. Commands for ``api-manage`` should run as the ``api`` user only.

.. warning:: 
         Running api-manage commands via playbook is not recommended or supported.

Inventory Import
~~~~~~~~~~~~~~~~

.. index:: 
   single: api-manage; inventory import

``api-manage`` is a mechanism by which an API administrator can import inventory directly into API, for those who cannot use Custom Inventory Scripts.

To use ``api-manage`` properly, you must first create an inventory in API to use as the destination for the import.

For help with ``api-manage``, run the following command: ``api-manage inventory_import [--help]``

The ``inventory_import`` command synchronizes an API inventory object with a text-based inventory file, dynamic inventory script, or a directory of one or more of the above as supported by core Distronode.

When running this command, specify either an ``--inventory-id`` or ``--inventory-name``, and the path to the Distronode inventory source (``--source``).

::

    api-manage inventory_import --source=/distronode/inventory/ --inventory-id=1 

By default, inventory data already stored in API blends with data from the external source. To use only the external data, specify ``--overwrite``. To specify that any existing hosts get variable data exclusively from the ``--source``, specify ``--overwrite_vars``. The default behavior adds any new variables from the external source, overwriting keys that already exist, but preserves any variables that were not sourced from the external data source.

::

    api-manage inventory_import --source=/distronode/inventory/ --inventory-id=1 --overwrite


.. note::

    Edits and additions to Inventory host variables persist beyond an inventory sync as long as ``--overwrite_vars`` is **not** set. 


Cleanup of old data
~~~~~~~~~~~~~~~~~~~

.. index:: 
   single: api-manage, data cleanup

``api-manage`` has a variety of commands used to clean old data from API. The API administrators can use the Management Jobs interface for access or use the command line. 

-  ``api-manage cleanup_jobs [--help]``

This permanently deletes the job details and job output for jobs older than a specified number of days.

-  ``api-manage cleanup_activitystream [--help]``


Cluster management
~~~~~~~~~~~~~~~~~~~~

.. index:: 
   single: api-manage; cluster management

.. note::
    Do not run other ``api-manage`` commands unless instructed by Red Hat Distronode personnel.


.. _ag_token_utility:

Session management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
   single: api-manage; session management

``expire_sessions``
^^^^^^^^^^^^^^^^^^^^^^^^

Use this command to terminate all sessions or all sessions for a specific user. Consider using this command when a user changes role in an organization, is removed from assorted groups in AD, or the administrator wants to ensure the user can no longer execute jobs due to membership in these groups.

::

	$ api-manage expire_sessions


This command terminates all sessions by default. The users associated with those sessions will be consequently logged out. To only expire the sessions of a specific user, you can pass their username using the ``--user`` flag (specify actual username for ``example_user`` below):

::

	$ api-manage expire_sessions --user example_user



``clearsessions``
^^^^^^^^^^^^^^^^^^^^^^^^

Use this command to delete all sessions that have expired. Refer to `Django's documentation on clearsessions`_ for more detail.

	.. _`Django's documentation on clearsessions`: https://docs.djangoproject.com/en/2.1/topics/http/sessions/#clearing-the-session-store



Analytics gathering
~~~~~~~~~~~~~~~~~~~~~

.. index:: 
   single: api-manage; data collection
   single: api-manage; analytics gathering


Use this command to gather analytics on-demand outside of the predefined window (default is 4 hours):

::

	$ api-manage gather_analytics --ship


For customers with disconnected environments who want to collect usage information about unique hosts automated across a time period, use this command: 

::

  api-manage host_metric --since YYYY-MM-DD --until YYYY-MM-DD --json


The parameters ``--since`` and ``--until`` specify date ranges and are optional, but one of them has to be present. The ``--json`` flag specifies the output format and is optional.
