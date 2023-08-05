kneejerk
=============

Image data can be messy.

Especially when considering the time it takes to label, persist, load, and operate-- generating datasets for user-preference Machine Learning projects can be a costly task.

The main goal of ``kneejerk`` is to allow users to *quickly* key in scores as they're served images, persist those scores, and formulate a way to quickly load everything into a format consumable by any number of Data Science libraries.

Motivation
----------

Ultimately, this library is intended to facilitate getting into the clean workflow outlined in François Chollet's excellent book `Deep Learning with Python <https://www.manning.com/books/deep-learning-with-python>`_.

`Link to one of his notebooks <https://github.com/fchollet/deep-learning-with-python-notebooks/blob/master/5.2-using-convnets-with-small-datasets.ipynb>`_ outlining this workflow on a neat, pre-labeled dataset.

In particular, we want to go from "big, unified directory of a ton of images" to "well-organized directories of images sorted into test/train/validation sets, by class." Crucially, though, **we want to do all of this file organization based on preferences that a user quickly generated using this library.**


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

     kneejerk score --input_dir im_dir --output_dir . --file_name preferences.csv

After you've generated your ``preferences.csv`` you can transfer all of the images to the proper directory structure via

.. code:: none

    kneejerk transfer --file_name preferences.csv


From there, you're all set to use the ``ImageDataGenerator.flow_from_directory()`` functionality in `keras <https://keras.io/preprocessing/image/>`_, or any similar library.


See the :ref:`tutorial` section in the documentation for more clarification on how this all works as well as some of the customization options.


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
- Published on PyPI


ToDo
~~~~

- Unit tests
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
