import requests
import csv
import re
from bs4 import BeautifulSoup

# Step 2: Make a GET request to the URL
URL = 'https://www.infoplease.com/geography/major-cities-latitude-longitude-and-corresponding-time-zones'
response = requests.get(URL, timeout=10)

# Step 3: Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Step 4: Find the table
table = soup.find('table')

# Step 5, 6, 7: Iterate over the rows, get the text from each cell and store the data
data = []
for row in table.find_all('tr'):
    columns = row.find_all('td')
    columns = [element.text.strip() for element in columns]
    data.append([element for element in columns if element]) # Get rid of empty values


# elminate the first two elements
data = data[2:]

# create a new array where the first element is split by the comma
array = []

for i in range(len(data)-1):
    print(i)
    tmp = data[i][0].split(', ')
    for dat in data[i][1:5]:
        tmp.append(dat)
    array.append(tmp)

data = []
for i in array:
    deg = i[2]
    minutes = i[3][:-1]
    direction = i[3][-1]
    coord1 = (float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1)
    deg = i[4]
    minutes = i[5][:-1]
    direction = i[5][-1]
    coord2 = (float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1)
    data.append([i[0], i[1], coord1, coord2])

# now save this in a csv file

with open('cities.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
