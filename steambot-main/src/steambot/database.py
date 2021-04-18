import json
from os import path

db = {'parties': {}}


def save_db():
    with open('data.txt', 'w') as outfile:
        json.dump(db, outfile)


def load_db():
    if not path.exists('data.txt'):
        save_db()
        return

    with open('data.txt') as json_file:
        temp = json.load(json_file)
        db['parties'] = temp['parties']
