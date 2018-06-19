from script import *

MAIN_DIALOG={
    'type_code':'Podaj kod waluty (USD, EUR, CHF, GBP):',
    'type_date':'Podaj daty rozpoczęcia i zakończenia (w formacie: YYYY-MM-DD):\n*limit obsługiwanego zakresu = 1 rok',
    'beginning':'początek:',
    'end':'koniec:',
}

RESPONSE={
    'average_buying':'Średni kurs sprzedaży w zadanym okresie dla {} wynosił {}.',
    'average_selling':'Średni kurs kupna w zadanym okresie dla {} wynosił {}.',
    'time_to_buy':'Najkorzystniejszym dniem na zakup waluty w zadanym okresie był {}.\nKurs sprzedaży wynosił {}.',
    'time_to_sell':'Najkorzystniejszym dniem na sprzedaż waluty w zadanym okresie był {}.\nKurs zakupu wynosił {}.',
    'error_message':'BŁĄD\n''Lub przekroczono 1 roku.\n Uruchom program raz jeszcze i wprowadź poprawne dane.'
}

# ---MAIN PROGRAM---#

# info from official NBP website limit=93 dni
#real limit = 1 year and 3 days

def main():

    print(MAIN_DIALOG['type_code'])
    code = check_code()

    while True:
        print(MAIN_DIALOG['type_date'])
        print(MAIN_DIALOG['beginning'])
        start, start_UTC = check_format_date(first_archival_date)

        print(MAIN_DIALOG['end'])
        end, end_UTC = check_format_date(first_archival_date)
        if not check_end_earlier_then_start(start_UTC, end_UTC):
            break

    adress = url.replace('{code}', code).replace('{startDate}', start).replace('{endDate}', end)


    try:
        response_data = requests.get(adress, headers={'accept': 'application/xml'})
        data = minidom.parseString(response_data.text)
        dataNodes = data.childNodes

        average_ask = get_average('Ask', dataNodes)
        average_bid = get_average('Bid', dataNodes)

        biggest_bid, date_of_bid, smallest_ask, date_of_ask = best_date(dataNodes)

        print(RESPONSE['average_buying'].format(code, average_ask))
        print(RESPONSE['average_selling'].format(code, average_bid))

        print(RESPONSE['time_to_buy'].format(date_of_ask, smallest_ask))
        print(RESPONSE['time_to_sell'].format(date_of_bid, biggest_bid))
    except:
        print(RESPONSE['error_message'])

main()


