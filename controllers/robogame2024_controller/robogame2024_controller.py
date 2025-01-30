# First explore the maze for generate maze.json
# import explore

from controller import Robot
from maze import Maze
from task import RoboGames_2024_Round_01

robot = Robot()
maze = Maze("maze.json")

task = RoboGames_2024_Round_01(robot, maze)

task.run()

