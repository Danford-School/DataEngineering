
# A bench knife is used to cut and scrape dough in a bakery.

import datetime
from collections import OrderedDict
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import re
import json
import csv


#################################################
# Danford Note:

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
headers = soup.find('tr')
dirty_headers = BeautifulSoup(str(headers), "lxml").get_text()
messy_headers = dirty_headers.replace(",", " ")
stinky_headers = messy_headers.replace("[", " ")
stanky_headers = stinky_headers.replace("maximum_speed", "")
smudged_headers = stanky_headers.replace("]", " ")
clean_headers = smudged_headers.split()
clean_headers.insert(0, "trip_number")
clean_headers.insert(1, "trip_date")

record_data = soup.find_all('td')
dirty_record_data = BeautifulSoup(str(record_data), "lxml").get_text()
messy_record_data = dirty_record_data.replace(",", " ")
stinky_record_data = messy_record_data.replace("]", " ")
smudged_record_data = stinky_record_data.replace("[", " ")
clean_record_data = smudged_record_data.split()

big_count = 0
little_count = 2
trip_count = 0
output = []
trip_no = 0
stored_direction = clean_record_data[4]
stored_vehicle = clean_record_data[0]
number_of_trips = len(trip_num_list)

with open("stops"+today+".csv", "a", newline='') as fw:
    writer = csv.writer(fw)
    if not once:
        writer.writerow(clean_headers)
    while trip_no <= number_of_trips:
        while little_count < 24:

            # This checks if stop_time is blank, inserts " " if so
            if little_count == 8:
                if len(clean_record_data[big_count + 1]) != 5:
                    output.insert(little_count, " ")
                    little_count += 1

            # This checks if location_id is blank and inserts " " if so
            if little_count == 11:
                if not len(clean_record_data[big_count]) >= 2:
                    output.insert(little_count, " ")
                    little_count += 1

            output.insert(little_count, clean_record_data[big_count])
            little_count += 1
            big_count += 1

        if little_count >= 24:
            print(stored_direction + " with " + output[4])
            print(output[0] + " with " + stored_vehicle)
            if not (stored_direction == output[5]) or not (output[0] == stored_vehicle):
                stored_direction = output[4]
                stored_vehicle = output[0]
                trip_no += 1

            output.insert(0, trip_num_list[trip_no])
            output.insert(1, date_ish)

            writer.writerow(output)
            if not once:
                once = True
                print("I at least started doing a thing!")
            little_count = 2
            output = []
