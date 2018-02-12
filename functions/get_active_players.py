# Get active players from all teams 40 man roster
from bs4 import BeautifulSoup
import urllib.request
import re

from classes.database import Database

# MySQL query constants
GET_TEAMS = ("SELECT id, abbreviation FROM teams")

def get_active_players():
    # Connect to mysql database
    db = Database()

    mlb_teams = db.query(GET_TEAMS)

    all_player_info = []
    # Grab all player id/names
    for team in mlb_teams:
        # Data comes in as tuple with id, abbreviation
        team_id = team[0]
        team_abbrev = team[1].lower()

        # Gets active 40 man rosters only
        with urllib.request.urlopen('http://m.mlb.com/' + team_abbrev + '/roster/40-man/') as url:
            r = url.read()

        soup = BeautifulSoup(r, 'html.parser')

        for player in soup.find_all('td', class_='dg-name_display_first_last'):
            if(player.a is not None):
                link = player.a.get('href')
                player_id = re.search('\/player\/([\d]+)\/',link).group(1)
                player_name = player.a.get_text()
                all_player_info.append((player_id, player_name, team_id))

    return all_player_info
