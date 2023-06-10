import os
from csv import reader

os.chdir(os.getcwd())


def import_csv_layout(path):
    with open(path) as level_map:
        terrain_map = []
        layout = reader(level_map, delimiter='.')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


import_csv_layout("./map/fuki4_Borders.csv")