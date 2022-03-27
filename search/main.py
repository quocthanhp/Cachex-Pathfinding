"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_coordinate

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
    

# Calculate estimated cost from current state to goal state using Manhattan distance
def heuristic(curr_state, goal_state):
    r1, q1 = curr_state
    r2, q2 = goal_state
    return abs(r1 - r2) + abs(q1 - q2)

