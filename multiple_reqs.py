import requests
from bs4 import BeautifulSoup
import csv

# CONST's
example_keys = ['mish', 'peshk', 'djathe']
headers = ['Nr', 'Kodi', '11 Shifrori', 'Pershkrimi', 'Tarifa baze', 'TVSH', 'EFTA', 'CEFTA', 'BE', 'Turqi']


"""Entry point: greet the user and ask for the querying method"""
user_screen = input('Hey. Press 1 to type your keywords. Press 2 to import your keywords from a CSV file. Press 3 to run the demo.\n')
user_response = int(user_screen)


def typed_by_user():
    """Method to handle user input keywords and query API"""
    input_keys = input('Enter your keywords separated by a comma and a space: ')
    chosen_keys = input_keys.split(', ')
    if len(input_keys) < 1:
        print('No key typed. Try again.')
        typed_by_user()
    else:
        for key in chosen_keys:
            r = requests.post('http://www.dogana.gov.al/preferenca/fetch.php', data={'keyword': key})
            if r.text:
                soup = BeautifulSoup(r.text)
                with open(key + '_responses.csv', 'w') as f:
                    wr = csv.writer(f)
                    wr.writerow(headers)
                    wr.writerows([[td.text.encode('utf-8') for td in row.find_all('td')] for row in soup.select('tr + tr')])
            else:
                print('No results for the given keywords.')


def imported_from_file():
    """Method to handle file input keywords and query API"""
    chosen_keys = []
    print('Make sure your CSV file is called "keys" has one single row with the specified keywords in it!')
    file = open('keys.csv', 'r')
    for line in file:
        temp = line.split(',')
        for t in temp:
            chosen_keys.append(t)
    print('keys: ', chosen_keys)
    if len(chosen_keys) < 1:
        print('Your keys file is empty. Try again.')
    for key in chosen_keys:
        r = requests.post('http://www.dogana.gov.al/preferenca/fetch.php', data={'keyword': key})
        if r.text:
            soup = BeautifulSoup(r.text)
            with open(key + '_responses_from_file.csv', 'w') as f:
                wr = csv.writer(f)
                wr.writerow(headers)
                wr.writerows([[td.text.encode('utf-8') for td in row.find_all('td')] for row in soup.select('tr + tr')])
        else:
            print('No results for the given keywords.')


def run_demo():
    for key in example_keys:
        r = requests.post('http://www.dogana.gov.al/preferenca/fetch.php', data={'keyword': key})
        soup = BeautifulSoup(r.text)
        with open(key + '_example_responses.csv', 'w') as f:
            wr = csv.writer(f)
            wr.writerow(headers)
            wr.writerows([[td.text.encode('utf-8') for td in row.find_all('td')] for row in soup.select('tr + tr')])


if user_response == 1:
    typed_by_user()
elif user_response == 2:
    imported_from_file()
else:
    run_demo()
