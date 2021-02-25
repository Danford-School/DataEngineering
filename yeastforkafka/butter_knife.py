
# Butter knife because it's a scraper.

import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import re
import json


#################################################
# Danford Note:
# This isn't working because it is taking every character because it doesn't know that words are words, it just sees
# characters. Beautiful Soup should really have a solution for this.
# if not, we can pull out whitespace-divided characters and turn them into strings and either use them on the fly,
# or put them into an array or dict.
#################################################


url = "http://rbi.ddns.net/getStopEvents"
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')

date_ish = 0
today = datetime.date.today().strftime("%Y%m%d")
almost_the_date = soup.find("h1")
close_to_the_date = BeautifulSoup(str(almost_the_date), "lxml").get_text()
closer_to_the_date = close_to_the_date.split()
for stuff in closer_to_the_date:
    if stuff.isnumeric():
        date_ish = re.search(r'\d{4}-\d{2}-\d{2}', close_to_the_date)

# h1 contains the date
# h3 contains the trip number
# table contains <tr> that are the rows, <th> which is the header and <td> which are the lines of data.
# There are 23 columns
all_trips = soup.find_all('h3')
clean_trips = BeautifulSoup(str(all_trips), "lxml").get_text()
cleaner_trips = clean_trips.split()
trip_num_list = []
for trippy in cleaner_trips:
    if trippy.isnumeric():
        trip_num_list.append(re.search(r'\d{9}', trippy))


json_out = []
count = 0

for trips in trip_num_list:
    records = soup.find_all('tr')
    dirty_records = BeautifulSoup(str(records), "lxml").get_text()
    messy_records = dirty_records.replace('\n', " ")
    stinky_records = messy_records.replace("[", " ")
    smudged_records = stinky_records.replace("]", " ")
    clean_records = smudged_records.split()

    for record in clean_records:

        headers = soup.find_all('th')
        dirty_headers = BeautifulSoup(str(headers), "lxml").get_text()
        messy_headers = dirty_headers.replace(",", " ")
        stinky_headers = messy_headers.replace("[", " ")
        smudged_headers = stinky_headers.replace("]", " ")
        clean_headers = smudged_headers.split()

        record_data = soup.find_all('td')
        dirty_record_data = BeautifulSoup(str(record_data), "lxml").get_text()
        messy_record_data = dirty_record_data.replace(",", " ")
        stinky_record_data = messy_record_data.replace("]", " ")
        smudged_record_data = stinky_record_data.replace("[", " ")
        clean_record_data = smudged_record_data.split()

        json_out.append("{")
        json_out.append("date : " + str(date_ish) + ",")
        json_out.append("trip_number : " + str(trips) + ",")
        for data in clean_record_data:
            if not count < 23:
                count = 0
                with open("stops"+today+".json", "a") as fw:
                    json.dump(json_out, fw, separators=(',', ':'))
            json_out.append(clean_headers[count] + " : " + data + ",")
            print(clean_headers[count])
            count += 1
        json_out.append("}")
