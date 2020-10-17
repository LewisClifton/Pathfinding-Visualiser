GRID_SIZE = 5
INFINITY = 99999

class Dijkstras:
    def __init__(self, grid, start, end, walls):
        self.grid = grid
        self.walls = walls
        self.start = start
        self.end = end
        self.distance = INFINITY
        self.visited = [self.start]
        self.route = []

    def main(self):
        while self.end not in self.visited:
            new_visits = self.handle_neighbours()
            if new_visits:
                for new_visit in new_visits:
                    if new_visit not in self.visited:
                        self.visited.append(new_visit)
            yield self.grid

    def get_neighbours_with_corners(self, current_node):
        row_length = len(self.grid[0])
        column_length = len(self.grid)

        current_node_neighbors = []
        x = current_node[0]
        y = current_node[1]

        if x != 0 and y != 0:
            i, j = x - 1, y - 1
            current_node_neighbors.append([i, j])
        if y != 0:
            i, j = x, y - 1
            current_node_neighbors.append([i, j])
        if x != row_length - 1 and y != 0:
            i, j = x + 1, y - 1
            current_node_neighbors.append([i, j])
        if x != row_length - 1:
            i, j = x + 1, y
            current_node_neighbors.append([i, j])
        if x != row_length - 1 and y != column_length - 1:
            i, j = x + 1, y + 1
            current_node_neighbors.append([i, j])
        if y != row_length - 1:
            i, j = x, y + 1
            current_node_neighbors.append([i, j])
        if x != 0 and y != column_length - 1:
            i, j = x - 1, y + 1
            current_node_neighbors.append([i, j])
        if x != 0:
            i, j = x - 1, y
            current_node_neighbors.append([i, j])

        return current_node_neighbors


    def get_neighbours(self, current_node):
        row_length = len(self.grid[0])
        column_length = len(self.grid)

        current_node_neighbors = []
        x = current_node[0]
        y = current_node[1]

        if y != 0:
            i, j = x, y - 1
            current_node_neighbors.append([i, j])
        if x != row_length - 1:
            i, j = x + 1, y
            current_node_neighbors.append([i, j])
        if y != row_length - 1:
            i, j = x, y + 1
            current_node_neighbors.append([i, j])
        if x != 0:
            i, j = x - 1, y
            current_node_neighbors.append([i, j])

        return current_node_neighbors

    def handle_neighbours(self):

        valid_neighbors = []

        for current_node in self.visited:
            current_node_neighbors = self.get_neighbours(current_node)
            for i in self.get_valid_neighbors(current_node, current_node_neighbors):
                if i not in valid_neighbors and i not in self.visited and [i[0],i[1]] not in self.walls:
                    valid_neighbors.append(i)

        return valid_neighbors

    def get_valid_neighbors(self,previous_node, previous_node_neighbors):
        valid_neighbors = []

        for i in range(len(previous_node_neighbors)):
            next_node = previous_node_neighbors[i]
            if next_node not in valid_neighbors and next_node not in self.visited and next_node not in self.walls:
                self.grid[next_node[0]][next_node[1]] = self.grid[previous_node[0]][previous_node[1]] + 1
                valid_neighbors.append(next_node)

        return valid_neighbors

    def output_result(self):
        for row in self.grid:
            print(row)
        print(f"Distance from {self.start} to {self.end} is {self.grid[self.end[0]][self.end[1]]}")

    def get_route(self):
        import time
        current = self.end
        while current != self.start:
            if current != self.end:
                self.route.append(current)
            valid_neighbours = []
            for current_neighbour in self.get_neighbours(current):
                if current_neighbour in self.visited and self.grid[current_neighbour[0]][current_neighbour[1]] != -1:
                    valid_neighbours.append(current_neighbour)

            valid_neighbour_weights = []
            for valid_neighbour in valid_neighbours:
                valid_neighbour_weights.append(self.grid[valid_neighbour[0]][valid_neighbour[1]])
            current = valid_neighbours[valid_neighbour_weights.index(min(valid_neighbour_weights))]

        self.route = self.route[::-1]
        return self.route, len(self.route)



