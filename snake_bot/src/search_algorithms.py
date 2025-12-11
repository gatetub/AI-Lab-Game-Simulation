import random
from collections import deque

# Directions (Up, Down, Left, Right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Random movement algorithm (limited moves)
def random_move(start, goal, obstacles, rows, cols):
    path = []
    current = start

    for _ in range(1000):  # Limit to 1000 moves
        direction = random.choice(DIRECTIONS)
        new_pos = (current[0] + direction[0], current[1] + direction[1])

        if (
            0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
            new_pos not in obstacles
        ):
            path.append(direction)
            current = new_pos

        if current == goal:
            return path

    return []  # If it takes too long, return empty path


# Write your code below this only

# Breadth First Search (BFS) Algorithm
def bfs(start, goal, obstacles, rows, cols):
    from collections import deque
    
    # Initialize queue with start position and empty path
    queue = deque([(start, [])])
    visited = {start}  # Using set for O(1) lookup
    
    while queue:
        current, path = queue.popleft()
        
        # Early exit if goal is found
        if current == goal:
            return path
            
        # Check all possible directions
        for dx, dy in DIRECTIONS:
            next_pos = (current[0] + dx, current[1] + dy)
            
            # Validate move and check if not visited
            if (0 <= next_pos[0] < rows and 
                0 <= next_pos[1] < cols and 
                next_pos not in obstacles and 
                next_pos not in visited):
                
                visited.add(next_pos)
                queue.append((next_pos, path + [(dx, dy)]))
    
    return []  # Return empty path if goal not found

# Depth First Search (DFS) Algorithm
def dfs(start, goal, obstacles, rows, cols):
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    stack = [(start, [])]
    visited = {start}  # Using set for O(1) lookup
    
    while stack:
        current, path = stack.pop()
        
        # Early exit if goal is found
        if current == goal:
            return path
            
        # Get all valid neighbors
        neighbors = []
        for dx, dy in DIRECTIONS:
            next_pos = (current[0] + dx, current[1] + dy)
            if (0 <= next_pos[0] < rows and 
                0 <= next_pos[1] < cols and 
                next_pos not in obstacles and 
                next_pos not in visited):
                neighbors.append((next_pos, (dx, dy)))
        
        # Sort neighbors by manhattan distance for better performance
        neighbors.sort(key=lambda x: manhattan_distance(x[0], goal), reverse=True)
        
        for next_pos, direction in neighbors:
            visited.add(next_pos)
            stack.append((next_pos, path + [direction]))
    
    return []  # Return empty path if goal not found

# Iterative Deepening Search (IDS Algorithm
def ids(start, goal, obstacles, rows, cols):
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def depth_limited_search(node, depth, path, visited):
        if depth < 0:
            return None
        if node == goal:
            return path
            
        visited.add(node)
        
        # Get and sort neighbors by manhattan distance
        neighbors = []
        for dx, dy in DIRECTIONS:
            next_pos = (node[0] + dx, node[1] + dy)
            if (0 <= next_pos[0] < rows and 
                0 <= next_pos[1] < cols and 
                next_pos not in obstacles and 
                next_pos not in visited):
                neighbors.append((next_pos, (dx, dy)))
        
        neighbors.sort(key=lambda x: manhattan_distance(x[0], goal))
        
        for next_pos, direction in neighbors:
            result = depth_limited_search(next_pos, depth - 1, path + [direction], visited)
            if result is not None:
                return result
                
        visited.remove(node)
        return None

    # Iterative deepening
    max_depth = rows * cols  # Maximum possible path length
    for depth in range(max_depth):
        visited = {start}
        result = depth_limited_search(start, depth, [], visited)
        if result is not None:
            return result
    
    return []  # Return empty path if goal not found
# Uniform Cost Search (UCS) Algorithm
def ucs(start, goal, obstacles, rows, cols):
    from heapq import heappush, heappop
    
    # Use heapq instead of PriorityQueue for better performance
    pq = [(0, start, [])]
    # Use dictionary to track costs - more efficient than checking visited set
    costs = {start: 0}
    
    while pq:
        cost, current, path = heappop(pq)
        
        # Early exit if we found the goal
        if current == goal:
            return path
            
        # Skip if we found a better path already
        if cost > costs.get(current, float('inf')):
            continue
            
        # Check all possible directions
        for dx, dy in DIRECTIONS:
            new_pos = (current[0] + dx, current[1] + dy)
            
            # Combine all validation checks into one condition
            if (0 <= new_pos[0] < rows and 
                0 <= new_pos[1] < cols and 
                new_pos not in obstacles and 
                cost + 1 < costs.get(new_pos, float('inf'))):
                
                new_cost = cost + 1
                costs[new_pos] = new_cost
                heappush(pq, (new_cost, new_pos, path + [(dx, dy)]))
    
    return []
# Greedy Best First Search Algorithm
def greedy_bfs(start, goal, obstacles, rows, cols):
    from heapq import heappush, heappop
    
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    # Priority queue with (heuristic, position, path)
    pq = [(manhattan_distance(start, goal), start, [])]
    visited = {start}  # Using set for O(1) lookup
    
    while pq:
        _, current, path = heappop(pq)
        
        # Early exit if goal is found
        if current == goal:
            return path
            
        # Check all possible directions
        for dx, dy in DIRECTIONS:
            next_pos = (current[0] + dx, current[1] + dy)
            
            # Validate move and check if not visited
            if (0 <= next_pos[0] < rows and 
                0 <= next_pos[1] < cols and 
                next_pos not in obstacles and 
                next_pos not in visited):
                
                visited.add(next_pos)
                # Priority is determined by manhattan distance to goal
                heappush(pq, (
                    manhattan_distance(next_pos, goal),
                    next_pos,
                    path + [(dx, dy)]
                ))
    
    return []  # Return empty path if goal not found

# A* Search Algorithm
def astar(start, goal, obstacles, rows, cols):
    from heapq import heappush, heappop
    
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors(pos):
        neighbors = []
        for dx, dy in DIRECTIONS:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if (0 <= new_pos[0] < rows and 
                0 <= new_pos[1] < cols and 
                new_pos not in obstacles):
                neighbors.append((new_pos, (dx, dy)))
        return neighbors
    
    # Priority queue: (f_score, g_score, position, path)
    open_set = [(manhattan_distance(start, goal), 0, start, [])]
    # Dictionary to store g_scores (cost from start to node)
    g_scores = {start: 0}
    # Dictionary to store f_scores (estimated total cost)
    f_scores = {start: manhattan_distance(start, goal)}
    
    while open_set:
        _, g_score, current, path = heappop(open_set)
        
        # Early exit if goal found
        if current == goal:
            return path
            
        # Skip if we found a better path already
        if g_score > g_scores.get(current, float('inf')):
            continue
            
        # Check neighbors
        for next_pos, direction in get_neighbors(current):
            tentative_g = g_scores[current] + 1
            
            if tentative_g < g_scores.get(next_pos, float('inf')):
                g_scores[next_pos] = tentative_g
                f_score = tentative_g + manhattan_distance(next_pos, goal)
                f_scores[next_pos] = f_score
                heappush(open_set, (f_score, tentative_g, next_pos, path + [direction]))
    
    return []
