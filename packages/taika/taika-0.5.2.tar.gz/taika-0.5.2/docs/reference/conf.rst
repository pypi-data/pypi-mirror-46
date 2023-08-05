Configuration file
==================

Taika features configuration using YAML files, since their are readable and flexible. Here
you will find the reference for the configuration file.

.. warning::

   Taika reserves to words in the configuration: **extensions** and **extensions_path**.
   Overriding these two keys in the configuration file can lead to unexpected behaviour.

.. data:: extensions (list)

   A list of extensions to use.

   E.g.::

      extensions:
         - taika.ext.rst
         - taika.ext.permalinks


.. data:: extensions_paths (list)

   A list of paths where extensions live. This paths will be added to the ``sys.path`` in
   order to make the extensions inside it discoverable.

   E.g.::

      extensions_paths:
         - ./extensions
         - ./plugins
         - ./_extensions
         - /.extensions
         - ~/.extensions
