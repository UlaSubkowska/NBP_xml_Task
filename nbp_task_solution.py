import time
import requests
import math

from xml.dom import minidom


def check_code():
    list_of_codes = ['USD', 'EUR', 'CHF', 'GBP']
    while True:
        code = input().upper()
        if code in list_of_codes:
            break
        else:
            print('Błędny format kodu waluty, spróbuj jeszcze raz.\ndostępne kody: USD, EUR, CHF, GBP')
    return code


def check_format_date():
    global date_UTC
    now = time.gmtime()
    start_date='2002-01-02'
    start_date=time.strptime(start_date, '%Y-%m-%d')

    while True:
        date = input()
        try:
            date_UTC = time.strptime(date, '%Y-%m-%d')
            if date_UTC > now:
                print('Nie przepowiadamy przyszłości :P\nwpisz datę jeszcze raz:')
            elif date_UTC < start_date:
                print('Niestety aż tak archwalnych danych NBP nie udostępnia, wpisz proszę datę po 2002-01-02.')
            else:
                break
        except ValueError:
            print('Błędny format daty, spróbuj jeszcze raz.')

    return date, date_UTC


def get_average(tag_name):
    list_of = []
    sum_of = 0

    for item in dataNodes[0].getElementsByTagName(tag_name):
        item = float(item.toxml().replace('<{}>'.format(tag_name), '').replace('</{}>'.format(tag_name), ''))
        list_of.append(item)
        sum_of += item
    average = '%.4f' % (sum_of / len(list_of))
    return average


def best_date():
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



# ---MAIN PROGRAM---#

# info from official NBP website limit=93 dni
#real limit = 1 year and 3 days

print('Podaj kod waluty (USD, EUR, CHF, GBP):')
code = check_code()

print('Podaj daty rozpoczęcia i zakończenia (w formacie: YYYY-MM-DD):\n*limit obsługiwanego zakresu = 1 rok')
print('początek:')
start, start_UTC = check_format_date()

print('koniec:')
end, end_UTC = check_format_date()


adress = 'http://api.nbp.pl/api/exchangerates/rates/C/{code}/{startDate}/{endDate}/'.replace('{code}', code).replace(
    '{startDate}', start).replace('{endDate}', end)

try:
    response_data = requests.get(adress, headers={'accept': 'application/xml'})
    data = minidom.parseString(response_data.text)
    dataNodes = data.childNodes

    average_ask = get_average('Ask')
    average_bid = get_average('Bid')

    biggest_bid, date_of_bid, smallest_ask, date_of_ask = best_date()

    print('Średni kurs sprzedaży w zadanym okresie dla {} wynosi {}.'.format(code, average_ask))
    print('Średni kurs kupna w zadanym okresie dla {} wynosi {}.'.format(code, average_bid))

    print('Najkorzystniejszym dniem na zakup waluty w zadanym okresie był {}.\nKurs sprzedaży wynosił {}.'.format(
        date_of_ask, smallest_ask))
    print('Najkorzystniejszym dniem na sprzedaż waluty w zadanym okresie był {}.\nKurs zakupu wynosił {}.'.format(
        date_of_bid, biggest_bid))
except:
    print('BŁĄD\nDaty zostały błędnie wprowadzone (końcowa data nie może być przed datą początkową).\n'
          'Lub przekroczono 1 roku.\n'
          'Uruchom program raz jeszcze i wprowadź poprawne dane.')



