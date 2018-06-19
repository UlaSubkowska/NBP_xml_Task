import time
import math


url='http://api.nbp.pl/api/exchangerates/rates/C/{code}/{startDate}/{endDate}/'
first_archival_date = time.strptime('2002-01-02', '%Y-%m-%d')


ERROR_CHECK_CODE= 'Błędny format kodu waluty, spróbuj jeszcze raz.\ndostępne kody: USD, EUR, CHF, GBP'
ERROR_FUTURE_DATE='Nie przepowiadamy przyszłości :P\nwpisz datę jeszcze raz:'
ERROR_TOO_OLD_DATE='Niestety aż tak archwalnych danych NBP nie udostępnia, wpisz proszę datę po 2002-01-02.'
ERROR_TO_SHORT_FORMAT='Błędny format daty, pamiętaj o zerach przed pierwszym, drugim itd. dniem miesiąca, oraz ' \
                      'miesiącami styczniem, lutym itd. Przykładowy poprawny format: 2018-01-01.'
ERROR_WRONG_DATE_FORMAT='Błędny format daty, spróbuj jeszcze raz, poprawny format: YYYY-MM-DD.'
ERROR_END_EARLIER_THEN_START='Daty zostały błędnie wprowadzone (końcowa data nie może być przed datą początkową).\n'


def check_code():
    list_of_codes = ['USD', 'EUR', 'CHF', 'GBP']
    while True:
        code = input().upper()
        if code in list_of_codes:
            return code
        else:
            print(ERROR_CHECK_CODE)

def check_format_date(first_archival_date):
    proper_len_of_date_format=10
    now = time.gmtime()
    while True:
        date=input()
        try:
            date_UTC = time.strptime(date, '%Y-%m-%d')
            if date_UTC > now:
                print(ERROR_FUTURE_DATE)
            elif date_UTC < first_archival_date:
                print(ERROR_TOO_OLD_DATE)
            elif len(date)!=proper_len_of_date_format:
                print(ERROR_TO_SHORT_FORMAT)
            else:
                return date, date_UTC
        except ValueError:
            print(ERROR_WRONG_DATE_FORMAT)

def check_end_earlier_then_start(start_UTC, end_UTC):
    if start_UTC>end_UTC:
        print(ERROR_END_EARLIER_THEN_START)
        return True


def get_average(tag_name, dataNodes):
    list_of = []
    sum_of = 0

    for item in dataNodes[0].getElementsByTagName(tag_name):
        item = float(item.toxml().replace('<{}>'.format(tag_name), '').replace('</{}>'.format(tag_name), ''))
        list_of.append(item)
        sum_of += item
    average = '%.4f' % (sum_of / len(list_of))
    return average


def best_date(dataNodes):
    biggest_bid = 0
    smallest_ask = math.inf
    date_of_ask, date_of_bid = None, None

    for (index, rate) in enumerate(dataNodes[0].getElementsByTagName('Rate')):
        bid = dataNodes[0].getElementsByTagName('Bid')[index]
        bid = float(bid.toxml().replace('<Bid>', '').replace('</Bid>', ''))
        if biggest_bid < bid:
            biggest_bid = bid
            date = dataNodes[0].getElementsByTagName('EffectiveDate')[index]
            date_of_bid = date.toxml().replace('<EffectiveDate>', '').replace('</EffectiveDate>', '')

        ask = dataNodes[0].getElementsByTagName('Ask')[index]
        ask = float(ask.toxml().replace('<Ask>', '').replace('</Ask>', ''))
        if smallest_ask > ask:
            smallest_ask = ask
            date = dataNodes[0].getElementsByTagName('EffectiveDate')[index]
            date_of_ask = date.toxml().replace('<EffectiveDate>', '').replace('</EffectiveDate>', '')
    return biggest_bid, date_of_bid, smallest_ask, date_of_ask







