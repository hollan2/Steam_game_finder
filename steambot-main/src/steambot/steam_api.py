from steam.webapi import WebAPI
from pprint import pprint
import requests
import json

STEAM_KEY='<fillmein>'

def get_games_list_from_steamid(api, steamid):
    games_list = api.IPlayerService.GetOwnedGames(
            steamid=steamid, 
            include_appinfo=True, 
            include_played_free_games=False, 
            appids_filter=[], 
            include_free_sub=False)
    played_game_map = { g['appid']: { 'name': g['name'], 'playtime': g['playtime_forever'] } 
            for g in games_list['response']['games'] }
    return played_game_map


def compare_games(api_key, steam_ids):
    def get_intersection(lists):
        app_ids = set(lists[0].keys())
        for l in lists[1:]:
            app_ids = app_ids.intersection(set(l.keys()))
        return app_ids

    def get_playtimes_for_appid(appid, game_lists):
        return [l[appid]['playtime'] for l in game_lists]

    api = WebAPI(key=api_key)
    game_lists = []
    for s_id in steam_ids:
        game_lists.append(get_games_list_from_steamid(api, s_id))

    overlap = get_intersection(game_lists)

    playtimes = {appid: get_playtimes_for_appid(appid, game_lists) for appid in overlap}

    overlap_games = {appid: {'name': game_lists[0][appid]['name'], 'playtime': playtimes[appid]}  for appid in overlap}
    return overlap_games

def is_game_multiplayer(api_key, appid):
    payload = {'appids': appid, 'key': api_key, 'format': 'json'}
    response = requests.get('http://store.steampowered.com/api/appdetails', params=payload)
    j = json.loads(response.text)
    if j[str(appid)]['success'] == False:
        return False
    return any([i for i in j[str(appid)]['data']['categories'] if i['id'] == 1])

if __name__ == "__main__":
    games = compare_games(STEAM_KEY, ["76561197999132492", "76561197970818679", "76561197962482553"])
    multiplayer_games = [games[g] for g in games.keys() if is_game_multiplayer(STEAM_KEY, g)]
    pprint(multiplayer_games)

    
