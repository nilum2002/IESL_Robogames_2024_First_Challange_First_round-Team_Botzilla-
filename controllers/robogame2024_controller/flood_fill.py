import matplotlib.pyplot as plt

class FloodFill:
    def __init__(self, maze):
        self.maze = maze

    def visualize_map(self, map):
        print(map)
        rows, cols = len(map), len(map[0])
        fig, ax = plt.subplots(figsize=(cols, rows))

        # Draw the grid
        for x in range(rows):
            for y in range(cols):
                value = map[x][y]
                color = "white" if value == -1 else "lightblue"
                ax.add_patch(plt.Rectangle((y, rows - 1 - x), 1, 1, color=color, edgecolor="black"))
                if value != -1:  # Only annotate visited cells
                    ax.text(y + 0.5, rows - 1 - x + 0.5, str(value), ha="center", va="center", fontsize=8, color="black")

        # Set axis properties
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_xticks(range(cols + 1))
        ax.set_yticks(range(rows + 1))
        ax.set_xticks([], minor=True)  # Hide axis ticks
        ax.set_yticks([], minor=True)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        plt.show()

    def visualize_shortest_path(self, map, points):
        rows, cols = len(map), len(map[0])
        fig, ax = plt.subplots(figsize=(cols, rows))

        # Draw the grid
        for x in range(rows):
            for y in range(cols):
                value = map[x][y]
                color = "white" if value == -1 else "lightblue"

                # Check if the cell is in points
                if (y, x) in points:
                    color = "red"

                ax.add_patch(plt.Rectangle((y, rows - 1 - x), 1, 1, color=color, edgecolor="black"))

                if value != -1:  # Only annotate visited cells
                    ax.text(y + 0.5, rows - 1 - x + 0.5, str(value), ha="center", va="center", fontsize=8, color="black")

        # Set axis properties
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_xticks(range(cols + 1))
        ax.set_yticks(range(rows + 1))
        ax.set_xticks([], minor=True)  # Hide axis ticks
        ax.set_yticks([], minor=True)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        plt.show()

    def generate_map(self, target_x, target_y):
        # Initialize the flood fill map with -1 (unvisited cells)
        map = [[-1 for _ in range(len(self.maze.cell_map[0]))] for _ in range(len(self.maze.cell_map))]

        # Directions for moving in the maze: [left, right, down, up]
        directions = [(-1, 0, 3), (1, 0, 2), (0, 1, 1), (0, -1, 0)]

        # Start the flood fill from the target cell
        queue = [(target_x, target_y)]
        # Set the target cell value to 0
        map[target_y][target_x] = 0  

        while queue:
            x, y = queue.pop(0)
            current_value = map[y][x]

            for dx, dy, wall_index in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.maze.cell_map) and 0 <= ny < len(self.maze.cell_map[0]):  # Check bounds
                    # Check if movement is allowed based on the current cell's walls
                    if map[ny][nx] == -1 and self.maze.cell_map[y][x][wall_index] == 0:
                        map[ny][nx] = current_value + 1
                        queue.append((nx, ny))

        return map
    
    def get_shortest_path(self, map, start_x, start_y):
        # Directions for moving in the maze: [left, right, down, up]
        directions = [(-1, 0, 3), (1, 0, 2), (0, 1, 1), (0, -1, 0)]
        path = [(start_x, start_y)]
        x, y = start_x, start_y

        while map[y][x] != 0:
            for dx, dy, wall_index in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.maze.cell_map) and 0 <= ny < len(self.maze.cell_map[0]):  # Check bounds
                    if map[ny][nx] == map[y][x] - 1 and self.maze.cell_map[y][x][wall_index] == 0:
                        x, y = nx, ny
                        path.append((x, y))
                        break

        return path
    
    def get_normalized_shortest_path(self, points):
        if len(points) <= 2:
            return points
        
        normalized_points = [] 

        previous_direction = None

        for i in range(1, len(points)):
            x1, y1 = points[i - 1]
            x2, y2 = points[i]
            if x1 == x2:
                if y2 > y1:
                    current_direction = "D"
                else:
                    current_direction = "U"
            else:
                if x2 > x1:
                    current_direction = "R"
                else:
                    current_direction = "L"

            if i == 1:
                pass
            elif current_direction != previous_direction:
                normalized_points.append(points[i - 1])
                if i == len(points) - 1:
                    normalized_points.append(points[i])
            elif i == len(points) - 1:
                normalized_points.append(points[i])

            previous_direction = current_direction

        return normalized_points