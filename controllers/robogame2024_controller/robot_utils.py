import math
from maze_conf import maze_conf

class RobotUtils:
    TIME_STEP = 64           # in milliseconds
    MAX_SPEED = 6.28         # in rad/s
    WHEEL_RADIUS = 0.0205    # in meters
    AXLE_LENGTH = 0.0584     # in meters

    def __init__(self, robot):
        self.robot = robot

        # motors
        self.left_motor = self.robot.getDevice('left wheel motor')
        self.right_motor = self.robot.getDevice('right wheel motor')
        self.left_motor.setPosition(0)
        self.right_motor.setPosition(0)
        # wheel sensors
        self.left_wheel_sensor = self.robot.getDevice('left wheel sensor')
        self.right_wheel_sensor = self.robot.getDevice('right wheel sensor')
        self.left_wheel_sensor.enable(self.TIME_STEP)
        self.right_wheel_sensor.enable(self.TIME_STEP)
        # compass
        self.compass = self.robot.getDevice('compass')
        self.compass.enable(self.TIME_STEP)
        # gps
        self.gps = self.robot.getDevice('gps')
        self.gps.enable(self.TIME_STEP)

        self.left_motor_position = 0
        self.right_motor_position = 0

    def step(self):
        return self.robot.step(self.TIME_STEP) != -1

    #----------------------------------------------
    # Methods for motors
    #----------------------------------------------

    def add_left_motor_position(self, position):
        self.left_motor_position += position
        self.left_motor.setPosition(self.left_motor_position)

    def add_right_motor_position(self, position):
        self.right_motor_position += position
        self.right_motor.setPosition(self.right_motor_position)

    def set_left_motor_speed(self, speed):
        self.left_motor.setVelocity((speed / 100) * self.MAX_SPEED)

    def set_right_motor_speed(self, speed):
        self.right_motor.setVelocity((speed / 100) * self.MAX_SPEED)

    def set_speed(self, speed):
        self.set_left_motor_speed(speed)
        self.set_right_motor_speed(speed)

    #----------------------------------------------
    # Methods for wheel sensors
    #----------------------------------------------

    def left_wheel_sensor_value(self):
        return self.left_wheel_sensor.getValue()
    
    def right_wheel_sensor_value(self):
        return self.right_wheel_sensor.getValue()
    
    #----------------------------------------------
    # Methods for compass
    #----------------------------------------------

    def compass_value(self):
        return self.compass.getValues()
    
    def bearing(self):
        dir = self.compass_value()
        if math.isnan(dir[0]):
            return None
        rad = math.atan2(dir[0], dir[1])
        bearing = (rad - 1.5708) / math.pi * 180.0
        if bearing < 0.0:
            bearing = bearing + 360.0
        return bearing
    
    #----------------------------------------------
    # Methods for gps
    #----------------------------------------------

    def current_cell_position(self, from_top_left=False): # from_top_left=True if the origin is the top left corner
        x, y, z = self.gps.getValues()
        # Move axis origin to the bottom left corner
        x = x + maze_conf['ARENA_SIZE'] / 2
        y = y + maze_conf['ARENA_SIZE'] / 2
        # Convert to cell coordinates
        x = x / maze_conf['CELL_SIZE']
        y = y / maze_conf['CELL_SIZE']

        if from_top_left:
            y = maze_conf['CELLS'] - y

        return x, y