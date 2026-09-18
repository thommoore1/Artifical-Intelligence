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

def isInGrid(pos):
    return GridMin <= pos[0] <= GridMax and GridMin <= pos[1] <= GridMax

def getActionCost(posOld, posNew):
    if posNew in FragileCosts:
        return FragileCosts[posNew]
    else:
        for direction in Directions:
            if (posOld[0] + direction[1][0], posOld[1] + direction[1][1]) == posNew:
                return direction[2]

def getHueristic(pos, goal, heuristic_type):
    if heuristic_type == "manhattan":
        return get_manhattan_distance(pos, goal)
    elif heuristic_type == "euclidean":
        return get_euclidean_distance(pos, goal)

def format_node(node):
    parent = node.parent.state if node.parent else None
    return f"{parent}->{node.state}({node.g:.2f}, {node.f:.2f})"

def pop(frontier):
    index = 0
    for i in range(1, len(frontier)):
        if frontier[i].f < frontier[index].f:
            index = i
    return frontier.pop(index)

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

#TODO: Complete this
def a_star_search(start_pos, goal_pos, heuristic_type="manhattan", weight = 1.0):
    print(f"=== A* Search ({heuristic_type}) ===")

    hueristic = getHueristic(start_pos, goal_pos, heuristic_type)
    start = Node(start_pos, parent=None, action=None, g=0.0, h=hueristic, w=weight)

    frontier = [start]
    reached = {start_pos: start.g}

    print(f"Initial frontier: [{format_node(start)}]")

    step = 0
    node_expansions = 0

    while frontier:
        current = pop(frontier)
        step += 1
        node_expansions += 1

        print(f"\nStep {step}")
        print(f"Expanded: {format_node(current)}")

        if current.state == goal_pos:
            path = reconstruct_path(current)

    pass
    


# Test Case (run twice and compare)
if __name__ == "__main__":
    start = (1, 1)
    goal = (4, 5)

    a_star_search(start, goal, heuristic_type="manhattan", weight=1.0) # modify the weight here for Task 2
    a_star_search(start, goal, heuristic_type="euclidean", weight=1.0) # modify the weight here for Task 2