Import/Export CSV files to Google Spreadsheets
==============================================

Simple CSV import/export wrapper for gspread_ package.

.. _gspread: https://gspread.readthedocs.io.

.. image:: https://travis-ci.org/dlancer/csv-export-gsheets.svg?branch=master
    :target: https://travis-ci.org/dlancer/csv-export-gsheets/
    :alt: Build status

.. image:: https://img.shields.io/pypi/v/csv-export-gsheets.svg
    :target: https://pypi.python.org/pypi/csv-export-gsheets/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/format/csv-export-gsheets.svg
    :target: https://pypi.python.org/pypi/csv-export-gsheets/
    :alt: Download format

.. image:: https://img.shields.io/pypi/l/csv-export-gsheets.svg
    :target: https://pypi.python.org/pypi/csv-export-gsheets/
    :alt: License

Installation
============


PIP
---

You can install the latest stable package running this command::

    $ pip install csv_export_gsheets


Also you can install the development version running this command::

    $ pip install git+http://github.com/dlancer/csv_export_gsheets.git@dev


Usage
=====

Before you start you should:

1. Create Google Service Account key (use JSON format):

   https://gspread.readthedocs.io/en/latest/oauth2.html

2. Create new spreadsheet in the Google Spreadsheets.

3. Share this spreadsheet with email from created service account file.

From command line::

    $ csv2gsheets --help


From python code:

.. code-block:: python

    from csv_export_gsheets.gsheet import import_csv

    # src - path to source CSV file or StringIO object
    # url - destination sheet url
    # cell - destination sheet cell (can include tab name: 'MyTab!A1')
    # credentials - path to service account credentials or dict
    # config - path to config file or dict
    import_csv(source=src, url=url, cell=cell, credentials=credentials, config=config)

..

Please note: destination sheet will be cleared before import.

TODO
====

- export from google spreadsheet to CSV
