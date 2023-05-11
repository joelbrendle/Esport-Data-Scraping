import requests
from bs4 import BeautifulSoup
import datetime

# URL of the team page
url = input('URL: ')
event = input('Event: ')
team_size = input('Team size: ')

if not team_size:
    team_size = 3

# Send a GET request to the URL and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

matches = soup.find_all('div', {'class': 'brkts-popup brkts-match-info-popup'})

# Generate a SQL prompt and open it in "append" mode
with open('data.sql', 'a') as sqlfile:
    for match in matches:
        try:
            left_team = match.find('div', {'class': 'brkts-popup-header-opponent brkts-popup-header-opponent-left'}).find('span', {'class': 'name'}).find('a').get('title')
        except AttributeError:
            continue

        try:
            right_team = match.find('div', {'class': 'brkts-popup-header-opponent brkts-popup-header-opponent-right'}).find('span', {'class': 'name'}).find('a').get('title')
        except AttributeError:
            continue

        date_time = match.find('div', {'class': 'match-countdown-block'}).find('span', {'class': 'timer-object'}).get('data-timestamp')

        # Convert the timestamp to a datetime object
        dt_object = datetime.datetime.fromtimestamp(int(date_time))

        # Convert the datetime object to a string
        date_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        # Append the SQL statement to the SQL prompt
        sql_statement = "INSERT INTO matches (event, home_team, away_team, team_size, date_time) VALUES ('{}', '{}', '{}', '{}', '{}');\n".format(
            event, left_team, right_team, team_size, date_time)
        sqlfile.write(sql_statement)
