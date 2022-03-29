"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

from operator import ne
import math 
import sys
import json

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import Node, PriorityQueue, print_board, print_coordinate


def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).

    ## Create necessary variables tor inputs to our functions
    # Getting the grid with occupied cells as 1 and rest as 0
    # Although grid is in square form, when calculating distances later, 
    #   we will base it off hexagonal grid to calculate and get accurate distances
    # This grid is just used to locate 
    grid = [[0]*data["n"] for i in range(data["n"])]
    for b,x,y in data["board"]:
        grid[x][y] = 1
    
    # Start position, Goal position
    start = tuple(data["start"])
    goal = tuple(data["goal"])
    
    # Visited Nodes
    visited = []
    
    # Path from Start to Finish
    path = []

    # Run the algorithm using Manhattan distance
    
    

# Calculate estimated cost from current state to goal state using Manhattan distance
def heuristic(curr_state, goal_state):
    r1, q1 = curr_state
    r2, q2 = goal_state
    return abs(r1 - r2) + abs(q1 - q2)

# Calculate estimated cost from current state to goal state using Euclidean distance
def heuristic_alt(curr_state, goal_state)
    r1, q1 = curr_state
    r2, q2 = goal_state
    return math.sqrt( (r2-r1)**2 + (q2-q1)**2 )

# Find the shortest path from start to goal
def shortest_path(start, goal, grid):
    
    # Initialise start node
    node = Node(state=start, parent=None, cost=heuristic(start, goal))
    
    # Intialise frontier with start node added
    frontier = PriorityQueue()
    frontier.add(node)

    # Initalise empty set storing node already generated
    generate = set()

    # Initialise empty solution
    solution = []

    while not frontier.is_empty:
        node = frontier.pop()
        
        # Check goal state
        if node.state == goal:
            while node.parent is not None:
                solution.append(node.state)
                node = node.parent
            solution.reverse()
            return solution

        # Mark node as already generated
        generate.add(node.state)

        # Expand current node
        for state in get_neighbors(node.state, grid):
            if state not in generate:
                neighbor = Node(state=state, parent=node, cost= 1 + heuristic(state, goal))
                frontier.add(neighbor)

# Get every neighbor of node
def get_neighbors(state, grid):
    r, q = state
    n = len(grid)
    neighbors = []
    possible_neighbors = [(r + 1, q), (r - 1, q), (r, q + 1), (r, q - 1),
                          (r + 1, q + 1), (r - 1, q - 1)]

    # Check valid neighbors
    for (r, q) in possible_neighbors:
        if 0 <= r < n - 1 and 0 <= q < n - 1 and grid[r][q] == 0:
            neighbors.append((r, q))

    return neighbors

# Transform points to hexagonal points for accurate distance calculations
# Got information from "Size and Spacing" section 
#   from https://www.redblobgames.com/grids/hexagons/
# We will let the size of hexagon be 1 (from centre of hexagon to a corner of the hexagon)
#   H = 2 * size = 2
#   W = sqrt(3) * size = sqrt(3)
def convert_hex_points(r,q):
    
    HEIGHT = 0.75 * 2  #Distance of centre point of hexagon on one row to that of next row (3/4 H)
    WIDTH = math.sqrt(3) #Distance of centre point of hexagon on one row to that of same row (W)
    
    # Finding new point for r
    h_r = r * HEIGHT

    # Finding new point for q
    #   BUT keep note that columns are at a slant 
    #   so we have to compensate for the shift in each row other than on row 0
    #       r * 0.5 * WIDTH --> shifts points according to which row its located in
    h_q = r * 0.5 * WIDTH + WIDTH 


            



