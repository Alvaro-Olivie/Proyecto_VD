import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_cities():
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
        coord1 = round((float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1),2)
        deg = i[4]
        minutes = i[5][:-1]
        direction = i[5][-1]
        coord2 = round((float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1),2)
        data.append([i[0], i[1], coord1, coord2])

    result = pd.DataFrame(data, columns = ['City', 'Country', 'Latitude', 'Longitude'])

    return result
