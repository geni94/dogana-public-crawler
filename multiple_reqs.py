import requests
from bs4 import BeautifulSoup
import csv
import unicodedata
import string

# CONST's
example_keys = ['mish', 'peshk', 'djathe', 'kec']
headers = ['Nr', 'Kodi', '11 Shifrori', 'Pershkrimi', 'Tarifa baze', 'TVSH', 'EFTA', 'CEFTA', 'BE', 'Turqi']
valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print(
            "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]


# test
# s = 'fake_folder/\[]}{}|~`"\':;,/? abcABC 0123 !@#$%^&*()_+ clᐖﯫⅺຶ 讀ϯՋ㉘ ⅮRㇻᎠ⍩ 𝁱C ℿ؛ἂeuឃC ᅕ ᑉﺜͧ bⓝ s⡽Հᛕ\ue063 牢𐐥er ᐛŴ n წş .ھڱ                                 df                                         df                                  dsfsdfgsg!zip'
# clean_filename(s)  # 'fake_folder_abcABC_0123_____clxi_28_DR_C_euC___bn_s_er_W_n_s_.zip'


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
    print('Make sure your CSV file is called "keys" has one single column with the specified keywords in it!')
    file = open('keys.csv', 'r')
    for line in file:
        temp = line.split('\n')
        for t in temp:
            chosen_keys.append(t)
    print('keys: ', chosen_keys)
    if len(chosen_keys) < 1:
        print('Your keys file is empty. Try again.')
    for key in chosen_keys:
        if len(key) > 4:
            print('Looking for ' + key)
            r = requests.post('http://www.dogana.gov.al/preferenca/fetch.php', data={'keyword': key})
            if r.text:
                soup = BeautifulSoup(r.text)
                name = clean_filename(str(key))
                with open('outputs/' + name + '.csv', 'w') as f:
                    wr = csv.writer(f)
                    wr.writerow(headers)
                    wr.writerows([[td.text.encode('utf-8') for td in row.find_all('td')] for row in soup.select('tr + tr')])
            else:
                print('No results for ' + key)


def run_demo():
    for key in example_keys:
        r = requests.post('http://www.dogana.gov.al/preferenca/fetch.php', data={'keyword': key})
        soup = BeautifulSoup(r.text)
        if len(soup.select('tr+tr')) > 1:
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
