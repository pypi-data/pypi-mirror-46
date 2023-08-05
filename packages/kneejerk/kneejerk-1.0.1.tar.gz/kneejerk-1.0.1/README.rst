kneejerk
=============

Image data can be messy.

Especially when considering the time it takes to label, persist, load, and operate-- generating datasets for user-preference Machine Learning projects can be a costly task.

The main goal of ``kneejerk`` is to allow users to *quickly* key in scores as they're served images, persist those scores, and formulate a way to quickly load everything into a format consumable by any number of Data Science libraries.

Getting Started
---------------

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
~~~~~~~~~~~~~

Using the tool is as easy as ``pip`` installing it and leveraging the command line utility

.. code:: none

    pip install kneejerk

Using the Package
~~~~~~~~~~~~~~~~~

Generating user preferences is as easy as using the command-line tool you just ``pip install`` 'ed.

.. code:: none

     kneejerk --input-dir im_dir --output-dir . --file-name preferences.csv --shuffle True

After you've generated your ``preferences.csv``, loading the data into ``X, y`` pairs of ``numpy.array`` 's looks like

.. code:: python

    from kneejerk.data.loader import transfer_normalized_image_data

    X, y = transfer_normalized_image_data('preferences.csv')


Please see the :ref:`tutorial` section in the documentation for more clarification on how this all works!


Project Goals
-------------

Done
~~~~~

- Quick command line interface that:

   - Points at a directory and combs through all images
   - Allows user to key in preference scores
   - Saves results to ``.csv`` of (filepath, score)
   - Allow for random shuffling of the order of images shown

- Loader that converts from the ``.csv`` and image files to ``numpy``
- Handle necessary data cleaning to resolve size mismatches

ToDo
~~~~

- Unit tests
- Published on PyPI
- Documentation :)


Contributing
------------

Bugs and Feature Requests should come in the form of `Issues in the project <https://github.com/NapsterInBlue/kneejerk/issues>`_

Contributions should only be made via `Pull Requests <https://github.com/NapsterInBlue/kneejerk/pulls>`_, *after* an appropriate Issue has been opened.

Please see our `contribution guide <https://github.com/NapsterInBlue/kneejerk/blob/master/.github/CONTRIBUTING.md>`_ if you've got more questions than that!


Running the tests
~~~~~~~~~~~~~~~~~

This project uses a simple combination of the ``unittest.TestCase`` object and ``pytest``. All code should be tested, and all tests should be run from the root of the project via the simple call:

.. code:: none

    pytest


Authors
-------

Huge shout-out to `avlaskin <https://github.com/avlaskin>`_ on GitHub for early collaboration via his slick library ``quickLabel``, a really cool ``TkInter`` interface that does a very similar task. My data processing extended beyond the scope of his library and so I figured I'd start from scratch instead of blow up his PR feed :)
