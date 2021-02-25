
# Butter knife because it's a scraper.

import datetime
from collections import OrderedDict
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

today = datetime.date.today().strftime("%Y%m%d")
almost_the_date = soup.find("h1")
close_to_the_date = BeautifulSoup(str(almost_the_date), "lxml").get_text()
closer_to_the_date = close_to_the_date.split()
date_ish = str(closer_to_the_date[4])

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
        trip_num_list.append(trippy)

once = False
json_out = []
little_count = 0
big_count = 0
headers = soup.find('tr')
dirty_headers = BeautifulSoup(str(headers), "lxml").get_text()
messy_headers = dirty_headers.replace(",", " ")
stinky_headers = messy_headers.replace("[", " ")
smelly_headers = stinky_headers.replace("maximum_speed", "")
smudged_headers = smelly_headers.replace("]", " ")
clean_headers = smudged_headers.split()

record_data = soup.find_all('td')
dirty_record_data = BeautifulSoup(str(record_data), "lxml").get_text()
messy_record_data = dirty_record_data.replace(",", " ")
stinky_record_data = messy_record_data.replace("]", " ")
smudged_record_data = stinky_record_data.replace("[", " ")
clean_record_data = smudged_record_data.split()

for trips in trip_num_list:
    if not once:
        json_out.append("date : " + date_ish)
        json_out.append("trip_number : " + str(trips))
    for data in clean_record_data:
        if not little_count < 22:
            little_count = 0
            json_out.append("date : " + date_ish)
            json_out.append("trip_number : " + str(trips))
            with open("stops"+today+".json", "a") as fw:
                output = json.dumps(json_out, separators=(',', ':'))
                fw.write(output)
            if not once:
                once = True
                print("I at least started doing a thing!")
        if little_count == 6 and (len(clean_record_data[big_count + 1]) != 5):
            little_count += 1
        json_out.append(clean_headers[little_count] + " : " + clean_record_data[big_count])
        little_count += 1
        big_count += 1
    # json_out.append("}")
