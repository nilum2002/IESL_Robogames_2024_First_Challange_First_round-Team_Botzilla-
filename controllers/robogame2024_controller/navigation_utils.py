import math
from maze_conf import maze_conf

class NavigationUtils:
    def __init__(self, robot):
        self.robot = robot

    def shortest_diff_degree(self, current_degree, target_degree):
        return (current_degree - target_degree + 180) % 360 - 180
    
    # The direction of the tow points is the angle between the line connecting the two points and the y-axis (north)
    def direction_of_tow_poits(self, x1, y1, x2, y2): # x1, y1 is the current position, x2, y2 is the target position
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angle -= 90
        angle = (angle + 360) % 360
        return angle
    
    def distance_of_two_points(self, x1, y1, x2, y2):
        x1 = x1 * maze_conf['CELL_SIZE']
        y1 = y1 * maze_conf['CELL_SIZE']
        x2 = x2 * maze_conf['CELL_SIZE']
        y2 = y2 * maze_conf['CELL_SIZE']
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def rotate_to_angle(self, target_degree):
        current_bearing = self.robot.bearing()
        target_bearing = target_degree

        shortest_diff = self.shortest_diff_degree(current_bearing, target_bearing)
        shortest_diff_rad = math.radians((abs(shortest_diff)))

        # Calculate the distance the robot needs to rotate
        rotation_distance = shortest_diff_rad * self.robot.AXLE_LENGTH / 2

        # Calculate the required wheel rotation in radians
        wheel_rotation = rotation_distance / self.robot.WHEEL_RADIUS

        if shortest_diff < 0:
            self.robot.add_left_motor_position(-wheel_rotation)  # Left wheel moves backward
            self.robot.add_right_motor_position(wheel_rotation)  # Right wheel moves forward
        else:
            self.robot.add_left_motor_position(wheel_rotation)
            self.robot.add_right_motor_position(-wheel_rotation)

        # Start the motors
        self.robot.set_left_motor_speed(40)
        self.robot.set_right_motor_speed(40)

        # Wait for the motion to complete
        while self.robot.step():
            # Check if the motors have reached their target positions
            left_position = self.robot.left_wheel_sensor_value()
            right_position = self.robot.right_wheel_sensor_value()

            if abs(left_position - self.robot.left_motor_position) < 0.01 and abs(right_position - self.robot.right_motor_position) < 0.01:
                break

        # Stop the motors
        self.robot.set_speed(0) # TODO: Do we need to stop the motors?

    def move_straight(self, distance):
        # Calculate the required wheel rotation in radians
        wheel_rotation = distance / self.robot.WHEEL_RADIUS

        # Set the target
        self.robot.add_left_motor_position(wheel_rotation)
        self.robot.add_right_motor_position(wheel_rotation)

        # Start the motors
        self.robot.set_left_motor_speed(100)
        self.robot.set_right_motor_speed(100)

        # Wait for the motion to complete
        while self.robot.step():
            # Check if the motors have reached their target positions
            left_position = self.robot.left_wheel_sensor_value()
            right_position = self.robot.right_wheel_sensor_value()

            if abs(left_position - self.robot.left_motor_position) < 0.01 and abs(right_position - self.robot.right_motor_position) < 0.01:
                break

    def move_to_point(self, x, y, from_top_left=False): # from_top_left=True if the origin is the top left corner
        if from_top_left:
            y = maze_conf['CELLS'] - y
        
        current_x, current_y = self.robot.current_cell_position()

        target_degree = self.direction_of_tow_poits(current_x, current_y, x, y)
        self.rotate_to_angle(target_degree)

        distance = self.distance_of_two_points(current_x, current_y, x, y)
        self.move_straight(distance)