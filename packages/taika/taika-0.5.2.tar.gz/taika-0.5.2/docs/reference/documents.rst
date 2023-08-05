Document specification
======================

Taika works with a dictionary representation of the documents. The following
keys are defined in the documents when are read by Taika. The document can contain other
keys, but they will be added by extensions:

.. data:: path (pathlib.Path)

The path that the file has in the source folder. **Shouldn't be modified**.

.. data:: url (pathlib.Path)

The path that the file will have in the destination folder. **Can be modified**.

.. data:: raw_content (bytes)

The content that has the file in the source directory. **Shouldn't be modified**.

.. data:: content (bytes)

The content after splitting the frontmatter from it. **Can be modified**.


