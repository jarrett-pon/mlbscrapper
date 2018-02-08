from bs4 import BeautifulSoup
import urllib.request
import re
import mysql.connector

from settings import *

mlb_teams = []

# Connect to mysql database
cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, database='mlbstats')
cursor = cnx.cursor()

query = ("SELECT id, abbreviation FROM teams")
truncate_players_table = ("TRUNCATE TABLE players")
add_players = ("INSERT INTO players (mlb_name, mlb_id, teams_id) VALUES (%s, %s, %s)")

cursor.execute(query)

for (id, abbreviation) in cursor:
    mlb_teams.append({'abbrev': abbreviation, 'id': id})

# Will get all player info so truncate old players
cursor.execute(truncate_players_table)

for team in mlb_teams:
    team_abbrev = team['abbrev'].lower()
    team_id = team['id']

    with urllib.request.urlopen('http://m.mlb.com/' + team_abbrev + '/roster/40-man/') as url:
        r = url.read()

    soup = BeautifulSoup(r, 'html.parser')

    for player in soup.find_all('td', class_='dg-name_display_first_last'):
        if(player.a is not None):
            link = player.a.get('href')
            player_id = re.search('\/player\/([\d]+)\/',link).group(1)
            player_name = player.a.get_text()
            data_players = (player_name, player_id, team_id)
            cursor.execute(add_players, data_players)

cnx.commit()
cursor.close()
cnx.close()
