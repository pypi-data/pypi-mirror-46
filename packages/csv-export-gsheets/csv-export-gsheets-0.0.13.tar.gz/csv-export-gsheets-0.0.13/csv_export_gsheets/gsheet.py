import csv
import gspread
from gspread import utils
from io import StringIO
from typing import Union, Optional

from .utils.conf import load_config
from .utils.credentials import load_credentials_from_json, load_credentials_from_dict


CSV_SNIFFER_BUFFER_SIZE = 4096


def import_csv(source: Optional[Union[str, StringIO]] = None,
               url: Optional[str] = None,
               cell: Optional[str] = None,
               credentials: Optional[Union[str, dict]] = None,
               config: Optional[Union[str, dict]] = None) -> dict:
    """
    Import CSV file to Google sheet

    :param source: path to source CSV file or StringIO object
    :param url: destination sheet url
    :param cell: destination sheet cell (can include tab name: 'MyTab!A1')
    :param credentials: path to google service account credentials file or dict
    :param config: path to config file or dict
    :return: Google Sheet API response object
    """
    settings = load_config(config) if isinstance(config, str) else None
    if settings is None and (source is None or url is None or credentials is None):
        raise ValueError('required parameters missed')

    csv_sniffer_buffer_size = CSV_SNIFFER_BUFFER_SIZE

    if settings is not None:
        source = settings.get('source', source)
        url = settings.get('url', url)
        cell = settings.get('cell', 'A1')
        credentials = settings.get('credentials', credentials)
        csv_sniffer_buffer_size = settings.get('csv_sniffer_buffer_size', CSV_SNIFFER_BUFFER_SIZE)

    cell = cell if cell is not None else 'A1'

    # TODO: add other types of credentials
    if isinstance(credentials, dict):
        credentials = load_credentials_from_dict(credentials)
    elif isinstance(credentials, str):
        credentials = load_credentials_from_json(credentials)
    else:
        credentials = None

    if credentials is None:
        raise ValueError('invalid credentials')

    if isinstance(source, str):
        try:
            infile = open(source, 'r')
            dialect = csv.Sniffer().sniff(infile.read(csv_sniffer_buffer_size))
            infile.seek(0)
            csv_data = infile.read()
        except Exception as e:
            raise ValueError(f'source file error {str(e)}')
    elif isinstance(source, StringIO):
        dialect = csv.Sniffer().sniff(source.read(csv_sniffer_buffer_size))
        source.seek(0)
        csv_data = source.read()
    else:
        raise ValueError('not supported source type')

    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(url)

    if '!' in cell:
        tab_name, cell = cell.split('!')
        worksheet = sheet.worksheet(tab_name)
        clear_range = f'{tab_name}!'
    else:
        worksheet = sheet.sheet1
        clear_range = ''

    # clear old values in the sheet
    row_col = utils.rowcol_to_a1(worksheet.row_count, worksheet.col_count)
    clear_range = f'{clear_range}A1:{row_col}'
    sheet.values_clear(clear_range)

    first_row, first_column = utils.a1_to_rowcol(cell)

    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": worksheet.id,
                    "rowIndex": first_row - 1,
                    "columnIndex": first_column - 1,
                },
                "data": csv_data,
                "type": 'PASTE_NORMAL',
                "delimiter": dialect.delimiter
            }
        }]
    }

    return sheet.batch_update(body)
