import os


def test_csv_import():
    from csv_export_gsheets.gsheet import import_csv

    res = import_csv(source='tests/data/test1.csv',
                     url=os.environ.get('GOOGLE_SHEET_TEST_URL', None),
                     credentials='api-key.json')

    assert res is not None, "csv import failed"
