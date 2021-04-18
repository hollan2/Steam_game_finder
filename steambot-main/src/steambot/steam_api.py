from steam.webapi import WebAPI
import steam.steamid
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

def get_game_info(api_key, appid):
    payload = {'appids': appid, 'key': api_key, 'format': 'json'}
    response = requests.get('http://store.steampowered.com/api/appdetails', params=payload)
    if response.ok:
        game_info = json.loads(response.text)
        if game_info[str(appid)]['success'] == False:
            return {}
        return game_info[str(appid)]['data']
    else:
        print("Rate-limited by steam", response.status_code)
        return {}

def is_game_multiplayer(appid, games_info):
    return any([i for i in games_info[appid]['categories'] if i['id'] == 1])

def get_steam_ids(urls):
     return [steam.steamid.steam64_from_url(url, http_timeout=30) for url in urls]

if __name__ == "__main__":
    steam_ids = get_steam_ids(["https://steamcommunity.com/id/logustus/", "https://steamcommunity.com/profiles/76561198039359036", "https://steamcommunity.com/id/rattboi/"])

    games = compare_games(STEAM_KEY, steam_ids)
    games_info = {g: get_game_info(STEAM_KEY, g) for g in games.keys()}
    no_info_games = {k:v for k,v in games_info.items() if v == {}}
    for key in no_info_games:
        games.pop(key)
        games_info.pop(key)

    multiplayer_games = [games[g] for g in games.keys() if is_game_multiplayer(g, games_info)]
    # pprint([v.get('metacritic', 75) for k,v in games_info.items()])
    pprint(multiplayer_games)
