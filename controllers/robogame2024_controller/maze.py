from maze_conf import maze_conf
import json

#----------------------------------------------
# Structure of the cell map
#
# ============================================================
# [
#  [[<cell_data_0_0>], [<cell_data_1_0], ... [<cell_data_x_y>]],
#  [[<cell_data_0_1>], [<cell_data_1_1], ... [<cell_data_x_y>]],
#  ...
#  [[<cell_data_0_y>], [<cell_data_1_y], ... [<cell_data_x_y>]]
# ]
# 
# <cell_data_x_y> = {<has_wall_north>, <has_wall_south>, <has_wall_east>, <has_wall_west>} # 1 if wall is present, 0 if wall is absent
# ============================================================
#
# Example:
# [ 
#   [[1, 0, 1, 0], [1, 1, 0, 1], [0, 1, 1, 0], ... ],
#   [[1, 0, 1, 0], [1, 1, 0, 1], [0, 1, 1, 0], ... ],
#   ...
#   [[1, 0, 1, 0], [1, 1, 0, 1], [0, 1, 1, 0], ... ]
# ]
#----------------------------------------------

class Maze:
    def __init__(self, file):
        self.file = file
        self.cell_map = None
        self.load()

    def load(self):
        with open(self.file, 'r') as f:
            json_data = f.read()
            self.cell_map = json.loads(json_data)