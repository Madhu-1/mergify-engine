.. _configuration file format:

====================
 Configuration File
====================

File Used
---------

Mergify uses the configuration file that is:

- The file named ``.mergify.yml``, or, as a fallback, ``.mergify/config.yml``
  from the root directory.

- In the the default repository branch configured on GitHub — usually
  ``master``.

Format
------

Here's what you need to know about the file format:

- The file format is `YAML <http://yaml.org/>`_.

- The file main type is a dictionary whose only key is named
  ``pull_request_rules``.

- The value type of the ``pull_request_rules`` is list.

- Each entry in ``pull_request_rules`` must be a dictionary.

Each dictionary must have the following keys:

.. list-table::
   :header-rows: 1
   :widths: 1 1 2

   * - Key Name
     - Value Type
     - Value Description
   * - ``name``
     - string
     - The name of the rule. This is not used by the engine directly, but is
       used when reporting information about a rule.
   * - ``conditions``
     - array of :ref:`Conditions`
     - A list of :ref:`Conditions` string that must match against the pull
       request for the rule to be applied.
   * - ``actions``
     - dictionary of :ref:`Actions`
     - A dictionary made of :ref:`Actions` that will be executed on the
       matching pull requests.

The rules are evaluated in the order they are defined in ``pull_request_rules``
and, therefore, the actions are executed in that same order.

See :ref:`Examples` for configuration file examples.

Validation
----------

Changes to the configuration file should be done via a pull request in order
for Mergify to validate it via a GitHub check.

However, if you want to validate your configuration file before sending a pull
request, you can use the following command line:

.. code:: bash

    $ curl -F 'data=@.mergify.yml' https://gh.mergify.io/validate


Or by uploading the configuration file with this form:

.. raw:: html

    <form method=post enctype=multipart/form-data action=https://gh.mergify.io/validate target=_blank>
      <input type=file name=data>
      <input type=submit value=Validate>
    </form>
