from controller import Robot
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from enum import Enum
from robot_utils import RobotUtils
from maze_conf import maze_conf

# --------------------------------------------------------------------

# Direction Class
class Direction(Enum):
    North = 'North'
    South = 'South'
    East = 'East'
    West = 'West'
    Left = 'Left'
    Right = 'Right'

# RobotState Class
class RobotState(Enum):
    FindWall = 'Find Wall'
    MountWall = 'Mount Wall'
    FollowWall = 'Follow Wall'
    TurnCorner = 'Turn Corner'
    CorrectTurn = 'CorrectTurn'
    GameOver = 'Game Over'

# According to right hand rule
WALL_DIR = {
    Direction.North : 2, # east
    Direction.East : 1, # south
    Direction.South : 3, # west
    Direction.West: 0, # north
}

# --------------------------------------------------------------------

# maze = [
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
# ]

maze = [
    [[0, 0, 0, 0] for _ in range(maze_conf['CELLS'])] for _ in range(maze_conf['CELLS'])
]

plt.ion()
fig, ax = plt.subplots(figsize=(10, 10))
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Real-Time Scatter Plot')

def visualize_maze(maze):
    ax.set_xticks(range(len(maze[0])))
    ax.set_yticks(range(len(maze)))
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Set limits to fit the maze size
    ax.set_xlim(0, len(maze[0]))
    ax.set_ylim(0, len(maze))

    # Plot the maze
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            north, south, east, west = maze[i][j]

            # Draw the north wall
            if north == 1:
                ax.add_patch(patches.Rectangle((j, i), 1, 0.1, edgecolor='black', facecolor='black'))
                
            # Draw the south wall
            if south == 1:
                ax.add_patch(patches.Rectangle((j, i + 1), 1, 0.1, edgecolor='black', facecolor='black'))

            # Draw the east wall
            if east == 1:
                ax.add_patch(patches.Rectangle((j + 1, i), 0.1, 1, edgecolor='black', facecolor='black'))

            # Draw the west wall
            if west == 1:
                ax.add_patch(patches.Rectangle((j, i), 0.1, 1, edgecolor='black', facecolor='black'))

    # Invert the y-axis to match the grid orientation
    ax.invert_yaxis()

    fig.canvas.draw()
    fig.canvas.flush_events()

visualize_maze(maze)

# --------------------------------------------------------------------

class WallFollow:
    def __init__(self, robot):
        self.robot = robot

        # get and enable proximity sensors
        self.ps = []
        for i in range(8):
            sensorName = "ps{!s}".format(i)
            sensor = self.robot.robot.getDevice(sensorName)
            sensor.enable(self.robot.TIME_STEP)
            self.ps.append(sensor)

        # Setup left and right motors
        self.robot.add_left_motor_position(float('inf'))
        self.robot.add_right_motor_position(float('inf'))
        self.robot.set_left_motor_speed(0)
        self.robot.set_right_motor_speed(0)

        self.state = RobotState.FindWall

        self.disable_tracking = True

    def direction(self):
        bearing = self.robot.bearing()
        if bearing is None:
            return None
        if 45 < bearing <= 135:
            return Direction.West
        elif 135 < bearing <= 225:
            return Direction.South
        elif 225 < bearing <= 315:
            return Direction.East
        else:
            return Direction.North

    def trackPos(self):
        if (self.disable_tracking): return

        gps_values = self.robot.gps.getValues()
        x = gps_values[0]
        y = gps_values[1]

        x += 1.25
        y -= 1.25

        x = (x/0.25)
        y = abs(y/0.25)

        x_f = x - int(x)
        y_f = y - int(y)

        dir = self.direction()

        if dir == Direction.North or dir == Direction.South:
            if not(y_f > 0.4 and y_f <= 0.5): return
        elif dir == Direction.East or dir == Direction.West:
            if not(x_f > 0.4 and x_f <= 0.5): return

        wall_existance = WALL_DIR[dir]

        x = int(x)
        y = int(y)

        if maze[y][x][wall_existance] == 1: return

        maze[y][x][wall_existance] = 1
        visualize_maze(maze)

        # write to json file
        with open('maze.json', 'w') as f:
            f.write(str(maze))

    # ----------------------------------------------------------------
    # Right-hand wall following algorithm.
    # ----------------------------------------------------------------
    def travel(self):
        self.trackPos()

        front_left = self.ps[7].getValue()
        front_right = self.ps[0].getValue()
        corner_right = self.ps[1].getValue()
        side_right = self.ps[2].getValue()

        # Use right-hand rule sensors directly
        hand_front = front_right
        opposite_front = front_left
        hand_corner = corner_right
        hand_side = side_right

        # ------------------------------------------------------------
        # Find Wall
        # ------------------------------------------------------------
        if self.state == RobotState.FindWall:
            self.disable_tracking = True
            self.robot.set_speed(50)
            if opposite_front > 200 and hand_front > 200:
                self.robot.set_speed(0)
                self.state = RobotState.MountWall
            elif opposite_front > 150 and hand_front > 150:
                self.robot.set_speed(5)
            elif opposite_front > 80 and hand_front > 80:
                if hand_side < 400 and hand_corner < 125:
                    self.robot.set_left_motor_speed(100)
                    self.robot.set_right_motor_speed(80)
                else:
                    self.robot.set_speed(20)
        # ------------------------------------------------------------
        # Mount Wall
        # ------------------------------------------------------------
        elif self.state == RobotState.MountWall:
            self.disable_tracking = True
            self.robot.set_left_motor_speed(-35)
            self.robot.set_right_motor_speed(35)
            if opposite_front > 80:
                return
            if hand_corner < 120 and hand_side > 150:
                self.robot.set_speed(0)
                self.state = RobotState.FollowWall
        # ------------------------------------------------------------
        # Follow Wall
        # ------------------------------------------------------------
        elif self.state == RobotState.FollowWall:
            self.disable_tracking = False
            self.robot.set_speed(100)
            # Facing Wall
            if opposite_front > 150 and hand_front > 150: ###
                self.robot.set_speed(0)
                self.state = RobotState.MountWall
            # Turn Corner
            elif hand_side < 80 and hand_corner < 80:
                self.robot.set_speed(50) # TODO: do we need this?
                self.state = RobotState.TurnCorner
            # Adjust Left (more severly)
            elif hand_side > 430 and hand_corner > 150:
                self.robot.set_left_motor_speed(-10)
                self.robot.set_right_motor_speed(50)
            # Adjust Left (moderate)
            elif hand_side > 430 and hand_corner > 100:
                self.robot.set_left_motor_speed(80)
                self.robot.set_right_motor_speed(100)
            # Adjust Right
            elif hand_side < 400 and hand_corner < 125:
                self.robot.set_left_motor_speed(100)
                self.robot.set_right_motor_speed(80)
        # ------------------------------------------------------------
        # Turn Corner
        # ------------------------------------------------------------
        elif self.state == RobotState.TurnCorner:
            self.disable_tracking = True
            self.robot.set_left_motor_speed(50)
            self.robot.set_right_motor_speed(10) 
            # Facing Wall
            if opposite_front > 300 and hand_front > 150:
                self.robot.set_speed(0)
                self.state = RobotState.MountWall
            elif hand_corner > 80:
                self.robot.set_speed(5) 
                self.state = RobotState.FollowWall

# --------------------------------------------------------------------

robot = Robot()
robot_utils = RobotUtils(robot)
wall_follow = WallFollow(robot_utils)

print("Starting...")

while robot_utils.step():
    wall_follow.travel()