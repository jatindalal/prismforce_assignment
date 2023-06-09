import json
from datetime import datetime
import argparse
import os

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def load_file():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()

    if not os.path.isfile(args.file_path):
        print("[!] File name provided doesn't refer to an actual file...")

    file = open(args.file_path)
    json_data = json.load(file)
    return json_data

def get_balance_sheet(json_data):
    expense_data = json_data["expenseData"]
    revenue_data = json_data["revenueData"]

    balance_sheet = {}
    year_wise_max_month = {}

    for _ in expense_data:
        start_date = _['startDate']
        start_date = datetime.strptime(start_date, DATE_TIME_FORMAT)
        if start_date.year in year_wise_max_month:
            year_wise_max_month[start_date.year] = max(year_wise_max_month[start_date.year], start_date.month)
        else:
            year_wise_max_month[start_date.year] = start_date.month

        if start_date in balance_sheet:
            balance_sheet[start_date] -= _['amount']
        else:
            balance_sheet[start_date] = -_['amount']


    for _ in revenue_data:
        start_date = _['startDate']
        start_date = datetime.strptime(start_date, DATE_TIME_FORMAT)
        if start_date.year in year_wise_max_month:
            year_wise_max_month[start_date.year] = max(year_wise_max_month[start_date.year], start_date.month)
        else:
            year_wise_max_month[start_date.year] = start_date.month

        if start_date in balance_sheet:
            balance_sheet[start_date] += _['amount']
        else:
            balance_sheet[start_date] = _['amount']

    # add empty month entries
    for year, month in year_wise_max_month.items():
        for i in range(1, month + 1):
            if datetime(year, i, 1) not in balance_sheet:
                balance_sheet[datetime(year, i, 1)] = 0

    balance_sheet = dict(sorted(balance_sheet.items()))
    return balance_sheet

def pretty_print(balance_sheet):
    print("Balance Sheet\n")
    for _ in balance_sheet.items():
        print('| {:1} | {:^4} |'.format(_[0].strftime('%Y-%m'), _[1]))


if __name__ == '__main__':
    json_data = load_file()
    balance_sheet = get_balance_sheet(json_data)
    pretty_print(balance_sheet)