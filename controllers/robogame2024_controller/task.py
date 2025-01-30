from robot_utils import RobotUtils
from navigation_utils import NavigationUtils
from flood_fill import FloodFill

class RoboGames_2024_Round_01:
    # The positions of the cells of the colors contains (measured from the top left corner)
    CELL_OF_RED_POS = (7, 3)
    CELL_OF_YELLOW_POS = (5, 9)
    CELL_OF_PINK_POS = (7, 6)
    CELL_OF_BROWN_POS = (8, 5)
    CELL_OF_GREEN_POS = (0, 6)

    # The nearest positions to the colors (measured from the top left corner)
    NEAR_OF_RED_POS = (7.75, 3.25)
    NEAR_OF_YELLOW_POS = (5.25, 9.75)
    NEAR_OF_PINK_POS = (7.25, 6.75)
    NEAR_OF_BROWN_POS = (8.75, 5.75)
    NEAR_OF_GREEN_POS = (0.5, 6.75)

    # -------------------------------------------------------
    # RoboGames 2024 Round 01 color order
    # -------------------------------------------------------
    COLOR_ORDER = {
        'red': [CELL_OF_RED_POS, NEAR_OF_RED_POS],
        'yellow': [CELL_OF_YELLOW_POS, NEAR_OF_YELLOW_POS],
        'pink': [CELL_OF_PINK_POS, NEAR_OF_PINK_POS],
        'brown': [CELL_OF_BROWN_POS, NEAR_OF_BROWN_POS],
        'green': [CELL_OF_GREEN_POS, NEAR_OF_GREEN_POS],
    }
    # -------------------------------------------------------

    def __init__(self, robot, maze):
        self.robot = robot
        self.maze = maze
        self.robot_utils = RobotUtils(robot)
        self.nav_utils = NavigationUtils(self.robot_utils)
        self.flood_fill = FloodFill(maze)

    def prepare(self, cx, cy):
        print("Preparing...")
        
        start_pos = (cx, cy)
        path_points = []

        for color, [cell_pos, near_pos] in self.COLOR_ORDER.items():
            print(f"Applying flood fill for {color}...")
            map = self.flood_fill.generate_map(cell_pos[0], cell_pos[1])
            print(f"Getting shortest path for {color}...")
            points = self.flood_fill.get_shortest_path(map, start_pos[0], start_pos[1])
            print(f"Normalizing shortest path for {color}...")
            points = self.flood_fill.get_normalized_shortest_path(points)

            # Add 0.5 to the x and y values of the points to move the robot to the center of the cell
            points = [(point[0] + 0.5, point[1] + 0.5) for point in points]

            path_points.extend(points)
            path_points.append(near_pos)
            if color != list(self.COLOR_ORDER.keys())[-1]:
                path_points.append(points[-1])

            # Update the start cell position
            start_pos = cell_pos

        return path_points

    def run(self):
        while self.robot_utils.step():
            cx, cy = self.robot_utils.current_cell_position(True)

            points = self.prepare(int(cx), int(cy))

            print("====================================")
            print("Run Started")
            print("====================================")

            # print(points)
            # print(points[0][0], points[0][1])
            # print(points[-1][0], points[-1][1])
            # break

            for point in points:
                x, y = point
                self.nav_utils.move_to_point(x, y, True)

            print("====================================")
            print("Run End")
            print("====================================")

            break