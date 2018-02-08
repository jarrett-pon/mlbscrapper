# Script for hitting mlb api to get mlb team info
import requests
import mysql.connector

from settings import *

add_teams = ("INSERT INTO teams (name, short_name, abbreviation, mlb_id) VALUES (%s, %s, %s, %s)")

base_url = "http://lookup-service-prod.mlb.com/lookup/json/"
api_extension_team_info = "named.historical_standings_schedule_date.bam?season=2017&game_date='2017/10/01'&sit_code='h0'&league_id=103&league_id=104"

response = requests.get(base_url + api_extension_team_info).json()
# Response structure
# historical_standings_schedule_date.standings_all_date_rptr.standings_all_date is an array of two leagues
# Each array is object (dictionary) of league_id and queryResults
# queryResults.row is array of all teams in the league

mlb_data = response["historical_standings_schedule_date"]["standings_all_date_rptr"]["standings_all_date"]

# Connect to mysql database
cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, database='mlbstats')
cursor = cnx.cursor()

# Script gets all teams so truncate table first
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("TRUNCATE TABLE teams")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

for league in mlb_data:
    team_data = league["queryResults"]["row"]
    for team in team_data:
        data_teams = (team["team_full"], team["team_short"], team["team_abbrev"], team["team_id"])
        cursor.execute(add_teams, data_teams)

cnx.commit()
cursor.close()
cnx.close()
