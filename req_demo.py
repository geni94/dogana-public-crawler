import requests
from bs4 import BeautifulSoup
import csv

r = requests.post('http://www.dogana.gov.al/preferenca/fetch.php', data={'keyword': 'mish'})

# declare html file w/ Bootstrap + table
html = """
<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body>
<div class="container">
<div class="row">
<div class="col-md-12">
<table class="table">
<thead class="thead-dark">
<tr>
<th>Numri</th>
<th>Kodi</th>
<th>11</th>
<th>Shifrori</th>
<th>Përshkrimi</th>
<th>Tarifa</th>
<th>bazë</th>
<th>TVSH</th>
<th>EFTA</th>
<th>CEFTA</th>
<th>BE</th>
<th>Turqi</th>
</tr>
</thead>
<tbody>
""" + r.text + """
</tbody>
</table>
</div>
</div>
</div>
</body>
"""

soup = BeautifulSoup(html)
table = soup.select_one('table.table')
headers = [th.text.encode("utf-8") for th in table.select("tr th")]

with open('out.csv', 'w') as f:
    wr = csv.writer(f)
    wr.writerow(headers)
    wr.writerows([[td.text.encode('utf-8') for td in row.find_all('td')] for row in table.select('tr + tr')])

with open('outOther.csv', 'w') as f:
    wr = csv.writer(f)
    wr.writerow(headers)
    wr.writerows([[td.text.encode('utf-8') for td in row.find_all('td')] for row in soup.select('tr + tr')])

print(r.status_code, r.reason)

Html_file = open('test', 'w')
Html_file.write(html)
Html_file.close()
Html_file1 = open('test1', 'w')
Html_file1.write(html)
Html_file1.close()
