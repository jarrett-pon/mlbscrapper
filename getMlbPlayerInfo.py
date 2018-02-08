from bs4 import BeautifulSoup
import urllib.request
import re
import mysql.connector
import requests

from settings import *

mlb_teams = []

base_url = "http://lookup-service-prod.mlb.com/lookup/json/"
api_extension_primary_stat_type = "named.player_teams.bam?player_id="
api_extension_active_years = "named.comp_player_has_stats_game_type.bam?league_list_id='mlb_hist'&player_id="

# Connect to mysql database
cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, database='mlbstats')
cursor = cnx.cursor()

query = ("SELECT id, abbreviation FROM teams")
add_players = ("INSERT INTO players (mlb_name, mlb_id, teams_id, primary_stat_type) VALUES (%s, %s, %s, %s)")

# Will get all player info so truncate old players
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("TRUNCATE TABLE players")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

cursor.execute(query)

for (id, abbreviation) in cursor:
    mlb_teams.append({'abbrev': abbreviation, 'id': id})

for team in mlb_teams:
    team_abbrev = team['abbrev'].lower()
    team_id = team['id']

    # Gets active 40 man rosters only
    with urllib.request.urlopen('http://m.mlb.com/' + team_abbrev + '/roster/40-man/') as url:
        r = url.read()

    soup = BeautifulSoup(r, 'html.parser')

    for player in soup.find_all('td', class_='dg-name_display_first_last'):
        if(player.a is not None):
            link = player.a.get('href')
            player_id = re.search('\/player\/([\d]+)\/',link).group(1)
            player_name = player.a.get_text()
            response = requests.get(base_url + api_extension_primary_stat_type + player_id).json()
            results = response["player_teams"]["queryResults"]
            size = results["totalSize"]
            if(size is "0"):
                primary_stat_type = 'unknown'
            elif(size is "1"):
                primary_stat_type = results["row"]["primary_stat_type"]
            else:
                primary_stat_type = results["row"][0]["primary_stat_type"]
            data_players = (player_name, player_id, team_id, primary_stat_type)
            cursor.execute(add_players, data_players)

cnx.commit()
cursor.close()
cnx.close()
