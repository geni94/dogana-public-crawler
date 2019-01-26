import requests
from bs4 import BeautifulSoup
import csv

keys = ['mish', 'peshk', 'djathe']
headers = ['Nr', 'Kodi', '11 Shifrori', 'Pershkrimi', 'Tarifa baze', 'TVSH', 'EFTA', 'CEFTA', 'BE', 'Turqi']

for key in keys:
    r = requests.post('http://www.dogana.gov.al/preferenca/fetch.php', data={'keyword': key})
    soup = BeautifulSoup(r.text)
    with open(key + '_responses.csv', 'w') as f:
        wr = csv.writer(f)
        wr.writerow(headers)
        wr.writerows([[td.text.encode('utf-8') for td in row.find_all('td')] for row in soup.select('tr + tr')])
