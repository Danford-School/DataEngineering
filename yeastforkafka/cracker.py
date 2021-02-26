# Butter knife because it's a scraper.

import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
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
type(soup)

rows = soup.find_all('tr')
list_rows = []
for row in rows[1:]:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)

df = pd.DataFrame(list_rows)
df = df[0].str.split(',', expand=True)

col_labels = soup.find_all('th')

all_header = []
col_str = str(col_labels)
text = BeautifulSoup(col_str, "lxml").get_text()
# get all of our individual columns
x = text.split(',')
# strip the first and last [ ] from our lislt
x[0] = x[0].strip('[')
x[len(x)-1] = x[len(x)-1].strip(']')

# get rid of all duplicates (definitely overkill but works)
header_set = set()
result = []
temp = ''
for item in x:
    item = item.strip(' ')
    if item not in header_set:
        header_set.add(item)
        temp = temp + str(item) + ","
        
# get rid of the last ',' so we don't have an extra column at the end
temp = temp[:-1]
# put the string in a list then to a dataframe 
# (since that's what we did in the lab so I can copy and paste)
result.append(temp)
df2 = pd.DataFrame(result)

df2 = df2[0].str.split(',', expand=True)

frames = [df2, df]
df = pd.concat(frames)
# remove all rows that are 'empty' aka contain [] as the input in vehicle_number column aka column 0
#df = df[~df[0].isin(['[]'])]
# remove the [ character from all items in vehicle_number aka column 0
df[0] = df[0].str.strip('[')
# remove the ] character from all items in schedule_status aka column 22
df[22] = df[22].str.strip(']')

json_data = df.to_json(orient="records")
parsed = json.loads(json_data)
with open('test.json', 'w') as outfile:
    json.dump(parsed, outfile)
    outfile.close()
    
test = ''
with open('test.json', 'r') as file:
    test = pd.read_json(file, orient='records')