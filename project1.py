#!CAUSION: NO OTHER IMPORTS ARE ALLOWED!
import math 

#NOTE: You must use the Node class below to define your nodes
class Node:
    def __init__(self, state, parent=None, action=None, g=0.0, h=0.0, w=1.0):
        self.state = state     # (x, y)
        self.parent = parent   # Parent Node object
        self.action = action   # e.g., "U", "UR"
        self.g = float(g)      # Path-cost from start to this node
        self.h = float(h)      # Heuristic estimate to goal
        self.w = float(w)      # When w>1.0, A* -> Weighted A*
        self.f = self.g + self.w * self.h # total estimated cost

def get_manhattan_distance(pos, goal):
    """|x1-x2| + |y1-y2|"""
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def get_euclidean_distance(pos, goal):
    """sqrt((x1-x2)^2 + (y1-y2)^2)"""
    return math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2)

## You may define more utility functions here

GridMin = 1
GridMax = 5

FragileCosts = {(3,3): 5, (4,2): 2, (3,4): 3.0}

Directions = {
    ("U", (0, 1), 1.0),
    ("D", (0, -1), 1.0),
    ("L", (-1, 0), 1.0),
    ("R", (1, 0), 1.0),
    ("UL", (-1, 1), 1.41),
    ("UR", (1, 1), 1.41),
    ("DL", (-1, -1), 1.41),
    ("DR", (1, -1), 1.41)
}


#TODO: Complete this
def a_star_search(start_pos, goal_pos, heuristic_type="manhattan", weight = 1.0):
    if heuristic_type == "manhattan":
        heuristic_func = get_manhattan_distance
    elif heuristic_type == "euclidean":
        heuristic_func = get_euclidean_distance
    else:
        raise ValueError("Invalid heuristic type. Choose 'manhattan' or 'euclidean'.")

    


# Test Case (run twice and compare)
if __name__ == "__main__":
    start = (1, 1)
    goal = (4, 5)

    a_star_search(start, goal, heuristic_type="manhattan", weight=1.0) # modify the weight here for Task 2
    a_star_search(start, goal, heuristic_type="euclidean", weight=1.0) # modify the weight here for Task 2