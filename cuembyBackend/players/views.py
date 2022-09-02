import requests

from players.models import Player

# Create your views here.

def get_info_fut():

    nations_consulted = {}
    clubs_consulted = {}

    base_end_point = 'https://futdb.app/api'
    end_point_players = f'{base_end_point}/players'
    end_point_nations = f'{base_end_point}/nations'
    end_point_clubs = f'{base_end_point}/clubs'
    headers = {'X-AUTH-TOKEN': '16bf6051-c932-48d1-b4f5-c7c0c04651c1'}
    response = requests.get(end_point_players, headers=headers)
    data = response.json()
    page_total = int(data['page_total'])
    for page in range(1, page_total+1):
        res = requests.get(end_point_players, headers=headers, params={'page':page})
        print(res.url)

        players = res.json()['items']
        for player in players:
            id_fut = player['id']
            name = player['name']
            position = player['position']
            nation = player['nation']
            club = player['club']

            if nation not in nations_consulted:
                res_nations = requests.get(f'{end_point_nations}/{nation}', headers=headers)
                data_nations = res_nations.json()
                nations_consulted.update({nation: data_nations['item']['name']})
            nation = nations_consulted[nation]

            if club not in clubs_consulted:
                res_clubs = requests.get(f'{end_point_clubs}/{club}', headers=headers)
                data_clubs = res_clubs.json()
                clubs_consulted.update({club: data_clubs['item']['name']})
            club = clubs_consulted[club]

            
            Player(id_fut=id_fut, name=name, position=position, nation=nation, club=club).save()

        
