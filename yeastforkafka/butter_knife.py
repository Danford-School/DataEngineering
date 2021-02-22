
# Butter knife because it's a scraper.

import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import re
import json

url = "http://rbi.ddns.net/getStopEvents"
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')

today = datetime.date.today().strftime("%Y%m%d")
almost_the_date = soup.find("h1")
close_to_the_date = BeautifulSoup(str(almost_the_date), "lxml").get_text()
date_ish = re.search(r'\d{4}-\d{2}-\d{2}', close_to_the_date)

# h1 contains the date
# h3 contains the trip number
# table contains <tr> that are the rows, <th> which is the header and <td> which are the lines of data.
# There are 23 columns
all_trips = soup.find_all('h3')
clean_trips = BeautifulSoup(str(all_trips), "lxml").get_text()
# print(clean_trips)


header_storage = []
json_out = []
count = 0

for trips in clean_trips:
#    header_storage.clear()
#    trip_number = re.search(r'\d{9}', trips)
#   print(trip_number)
    records = soup.find_all('tr')
    clean_records = BeautifulSoup(str(records), "lxml").get_text()

    for record in clean_records:

        headers = soup.find_all('th')
        clean_headers = BeautifulSoup(str(headers), "lxml").get_text()

        record_data = soup.find_all('td')
        clean_record_data = BeautifulSoup(str(record_data), "lxml").get_text()

        json_out.append("{\n")
#        json_out.append("date : " + str(date_ish) + ",\n")
#        json_out.append("trip_number : " + str(trip_number) + ",\n")
        for data in clean_record_data:
            if not count < 23:
                count = 0
                with open("stops"+today+".json", "a") as fw:
                    json.dump(json_out, fw)
            json_out.append(header_storage[count] + " : " + data + ",\n")
            print(header_storage)
            count += 1
        json_out.append("}\n")
