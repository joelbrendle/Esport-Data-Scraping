import requests
from bs4 import BeautifulSoup

# URL of the NRG team page on Liquipedia
url = input('URL: ')
country = input('Country: ')
region = input('Region: ')

# Send a GET request to the URL and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Get the team name, short name, organization, country, logo, and website
name = soup.find('h1', {'id': 'firstHeading'}).text.strip()
logo = soup.find('div', {'class': 'infobox-image'}).find('img').get('src')
website = soup.find('div', {'class': 'infobox-center infobox-icons'}).find_all('a')[0].get('href')

# Generate a SQL prompt and write it to a text file
with open('data.sql', 'w') as sqlfile:
    sql_statement = "INSERT INTO teams (name, logo, website, country, region) VALUES ('{}', '{}', '{}', '{}', '{}');".format(
        name, logo, website, country, region)
    sqlfile.write(sql_statement)
