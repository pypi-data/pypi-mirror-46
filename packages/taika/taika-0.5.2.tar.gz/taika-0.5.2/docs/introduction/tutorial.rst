.. highlight:: shell

Basic Tutorial
==============

Create a directory with files::

   mkdir source
   touch source/index.txt
   touch source/contents.rst
   touch source/first-post.md
   touch source/taika.yml

And run the ``taika`` command::

   taika source /tmp/taika/
   ls /tmp/taika/

Taika will get your files from ``source`` and will process and write them into ``/tmp/taika``::

   contents.rst  first-post.md  index.txt  taika.yml

The extensions that you load into Taika will modify those files and probably will have
different extensions, new content, etc. Take a look at the :doc:`extensions <../extensions/index>`.
