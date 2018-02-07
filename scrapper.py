from bs4 import BeautifulSoup
import urllib.request
import re

with urllib.request.urlopen('http://m.mlb.com/bal/roster/40-man/') as url:
    r = url.read()
soup = BeautifulSoup(r, 'html.parser')

for player in soup.find_all('td', class_='dg-name_display_first_last'):
    if(player.a is not None):
        link = player.a.get('href')
        print(re.search('\/player\/([\d]+)\/',link).group(1))
        print(player.a.get_text())
