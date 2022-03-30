"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

from operator import ne
import math
import queue 
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
    #   we will base it off hexagonal points to calculate and get accurate distances
    # This grid is just used to locate blocked hexagons
    grid = [[0]*data["n"] for i in range(data["n"])]
    for _,x,y in data["board"]:
        grid[x][y] = 1
    
    # Start position, Goal position
    start = tuple(data["start"])
    goal = tuple(data["goal"])
    
    # Finding Shortest Path
    path = shortest_path(start, goal, grid)

    # Printing Solution
    if not path:
        print(0)
    else:
        print(len(path))
        for coord in path:
            print(coord)

############################################################################################################

def shortest_path(start, goal, grid):
    """
    Finding the shortest path from start to goal using A* search 
        where our heuristic function uses the euclidean distance
    """
    # Initialise start node
    node = Node(state=start, parent=None, cost_h=0, cost_g=0)
    
    # Intialise frontier with start node added
    frontier = PriorityQueue()
    frontier.add(node)

    # Initalise empty set storing node already generated
    generate = set()

    # Initialise empty solution
    solution = []

    # Initialise heuristic dictionary with heuristic value of start node
    heuristic_dict = {}
    heuristic_dict[start] = 0
    
    while not frontier.is_empty():

        node = frontier.pop()
        
        # Check goal state and if solution cost is better than previously found ones
        if node.state == goal:
            while node is not None:
                solution.append(node.state)
                node = node.parent
            solution.reverse()
            return solution

        # Mark node as already generated
        generate.add(node.state)
       
        # Expand current node
        for state in get_neighbors(node.state, grid):
            if state not in generate:
                # Calculate heuristic value of node if haven't
                if not frontier.contain_state(state):
                    heuristic_dict[state] = heuristic(state, goal)
                
                # Add to frontier
                neighbor = Node(state=state, parent=node, cost_h=heuristic_dict[state], cost_g=node.cost_g + 1)
                frontier.add(neighbor)

    # If no solutions just return empty solution 
    return solution

############################################################################################################

def heuristic(curr_state, goal_state):
    """ 
    Calculate estimated cost from current state to goal state using Euclidean distance
    """
    r1, q1 = convert_hex_points(curr_state[0], curr_state[1])
    r2, q2 = convert_hex_points(goal_state[0], goal_state[1])
    return math.sqrt( (r2-r1)**2 + (q2-q1)**2 )

############################################################################################################

def get_neighbors(state, grid):
    """ 
    Get every neighboring nodes of node
    """
    r, q = state
    n = len(grid)
    neighbors = []
    possible_neighbors = [(r+1, q), (r-1, q), 
                            (r, q+1), (r, q-1),
                            (r+1, q-1), (r-1, q+1)]

    # Check valid neighbors
    for (r, q) in possible_neighbors:
        if 0 <= r < n  and 0 <= q < n  and grid[r][q] == 0:
            neighbors.append((r, q))

    return neighbors

############################################################################################################
def convert_hex_points(r,q):
    """
    Transform points to hexagonal points for accurate distance calculations
    
    Got information from "Size and Spacing" section 
        from https://www.redblobgames.com/grids/hexagons/
    
    We know that the Width is 1 because moving from one hexagon to another has a cost of 1
        W = 1
    
    Given W, we find the SIZE of hexagon (from centre of hexagon to a corner of the hexagon)
        W = sqrt(3) * SIZE = 1 --> SIZE = 1/sqrt(3)
    
    Now we can find the height
        H = 2 * size = 2/sqrt(3)

    We assume the origin is the centre point of hexagon (0,0)
    """
    # Distance of centre point of hexagon on one row to that of next row (3/4 H)
    HEIGHT = 0.75 * (2 / math.sqrt(3)) 

    # Distance of centre point of hexagon on one row to that of same row (W)  
    WIDTH = 1
    
    # Finding new point for r
    h_r = r * HEIGHT

    # Finding new point for q
    #   BUT keep note that columns are at a slant 
    #   so we have to compensate for the shift in each row other than on row 0
    #       r * 0.5 * WIDTH --> shifts points according to which row its located in
    h_q = r * 0.5 * WIDTH + q * WIDTH 

    return h_r, h_q
            



