Create your own extension
=========================

If you want to create yourself an extension, this is the place. You can take a look at the source
of builtin extensions such as :doc:`layouts </extensions/layouts>` or :doc:`rst </extensions/rst>`.


Available events to register to
-------------------------------

The following are the different events which you can register your extension to.

.. note::

   The arguments that are listed are given as *arguments*, not *keyword_arguments*.


.. data:: doc-post-read

   Arguments: ``site, document``

   Called after each document read.

.. data:: site-post-read

   Arguments: ``site``

   Called after all the documents have been read.


Empty extension
---------------

This will be the backbone of your extension, one that does nothing:

.. code-block:: python

   def do_nothing(site, document):
      pass

   def setup(site):
      pass

Taika will use the  :code:`setup()` as entry point, so you should do your loading there.

Save it  as a Python file and place it in the :data:`extensions` and put it's path into
:data:`extensions_path`, so we can find it and load it:

.. code-block:: yaml

   # taika.yml
   ...
   extensions_path: /path/to/my_extensions
   extensions:
      ...
      - my_extension  # <--
      ...
   ...

.. If you run Taika with ``-l DEBUG``, you see that the extension is listed as loaded.

Adding functionality
--------------------

Here, we use as example an extension that will print certain documents. First we print
all the documents::

   def print_document(site, document):
       print(document)

   def setup(site):
       site.events.register("doc-post-read", print_document)


Note that we are registering our function using ``site.events.register``.


Making the extension configurable
---------------------------------

Now we want to print only certain documents, based on the frontmatter keys. But we want to
configure which key is needed to print the documents, so we make our extension to read
``site.config``.::

   def print_document(site, document):
       on_key = site.config.get("print_document_on_key", DEFAULT_KEY)
       if on_key in document:
           print(document)

   def setup(site):
       site.events.register("doc-post-read", print_document)

We used the ``get`` method on the configuration and we passed our key name and a default
value. Later, we decide that we want to pass a list of keys which will trigger the print.
We modify our extensions as follows::

   def print_document(site, document):
       on_keys = site.config.get("print_document_on_keys", DEFAULT_KEYS)
       match = [key in document for key in on_keys]
       if any(match):
           print(document)

   def setup(site):
       site.events.register("doc-post-read", print_document)

And that's all! Be creative!
