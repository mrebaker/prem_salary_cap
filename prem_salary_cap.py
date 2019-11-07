from datetime import datetime as dt
import csv
import numpy as np

from companies_house.api import CompaniesHouseAPI
import yaml


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    print(matrix)
    return matrix[size_x - 1, size_y - 1]


def load_player_list():
    player_list = []
    with open('player_list.csv', 'r', encoding='utf-8-sig') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            d = dict()
            d['club'] = row['Club']
            d['name'] = row['Name']
            d['position'] = row['Position']
            d['country'] = row['Country']
            player_list.append(d)
    return player_list


if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    ch = CompaniesHouseAPI(config['chapi_key'])

    players = load_player_list()

    if len(players) > 600:
        print(f'Warning: {len(players)} will likely cause the API rate limit to be exceeded.')

    for player in players:
        results = ch.search_officers(q=player['name'])
        print(f"{player['name']}: {results['total_results']}")
