import requests
from bs4 import BeautifulSoup

# Step 2: Make a GET request to the URL
url = 'https://www.infoplease.com/geography/major-cities-latitude-longitude-and-corresponding-time-zones'
response = requests.get(url)

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

# Print the data
for element in data:
    print(element)

# elminate the first two elements
data = data[2:]

# now seperate the first element in each row into city and country and insert everything into a new dataframe
for element in data:
    # split the first element into city and country
    city_country = element[0].split(',')
    # insert city and country into the dataframe



# now eliminate the last element in each row
for element in data:
    element.pop()

# now save this in a csv file
import csv
with open('cities.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)





api_url = 'https://api.api-ninjas.com/v1/city?min_population=500'    
response = requests.get(api_url, headers={'X-Api-Key': 'Omiq0qw7AkCQODAInA4yqw==981iwkdqfuPcqb84'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)