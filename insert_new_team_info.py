# Script for hitting mlb api to get mlb team info
import requests

from classes.database import Database

# Api Url Constants
BASE_URL = "http://lookup-service-prod.mlb.com/lookup/json/"
TEAM_INFO_EXT = "named.historical_standings_schedule_date.bam?season=2017&game_date='2017/10/01'&sit_code='h0'&league_id=103&league_id=104"
# MySQL query constants
GET_TEAMS = ("SELECT mlb_id FROM teams")
ADD_TEAMS = ("INSERT INTO teams (name, short_name, abbreviation, mlb_id) VALUES (%s, %s, %s, %s)")

response = requests.get(BASE_URL + TEAM_INFO_EXT).json()

# Response structure
mlb_data = response["historical_standings_schedule_date"]["standings_all_date_rptr"]["standings_all_date"]

all_team_data = []

for league in mlb_data:
    teams = league["queryResults"]["row"]

    for team in teams:
        team_data = (team["team_full"], team["team_short"], team["team_abbrev"], team["team_id"])
        all_team_data.append(team_data)

# Connect to mysql database
db = Database()

# Get all current teams in DB
database_teams = db.query(GET_TEAMS)
# Unpack list of tuples to list
database_teams = [team[0] for team in database_teams]
# Only add teams that weren't already in the DB based on mlb id
all_team_data = [team for team in all_team_data if int(team[3]) not in database_teams ]

print("New teams", all_team_data)
db.insert(ADD_TEAMS, all_team_data, many=True)
