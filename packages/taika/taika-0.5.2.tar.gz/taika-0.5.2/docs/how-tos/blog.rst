Blogging site
=============

With taika you can setup a little static blog as you can do it with Jekyll, Hugo, Pelican
or others. You should add a few extensions and options to your ``taika.yml`` configuration.

.. code-block:: yaml

   title: Hector Martinez-Lopez
   subtitle: Scientific Software Developer
   url: https://hectormartinez.gitlab.io
   extensions:
      - taika.ext.rst
      - taika.ext.collections
      - taika.ext.layouts
      - taika.ext.excerpt

   assets:
      source: assets
      destination: assets

   collections:
      posts:
         pattern: "posts/(?!index.rst).*"

   layouts_pattern: '*.rst'
   layouts_options:
      autoescape: False
      lstrip_blocks: True
      trim_blocks: True

Adding those options, Taika will be able to parse the '\*.rst' files into html, aggregate
them into collections, render them using Jinja2 and extract their excerpt. You need to
have a ``templates/`` directory in the working directory so Jinja2 can template your
posts and pages. Check the :doc:`layouts extension</extensions/layouts>` for more detail.
