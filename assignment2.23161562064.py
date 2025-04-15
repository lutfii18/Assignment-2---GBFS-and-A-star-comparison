import heapq
import time

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def is_goal(state):
    return state == goal_state

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    moves = []
    x, y = find_zero(state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            moves.append(new_state)
    return moves

def misplaced_tiles(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                count += 1
    return count

def greedy_bfs(start):
    start_time = time.time()
    visited = set()
    queue = []
    heapq.heappush(queue, (misplaced_tiles(start), start, []))
    nodes_explored = 0

    while queue:
        h, current, path = heapq.heappop(queue)
        nodes_explored += 1
        if is_goal(current):
            return path + [current], time.time() - start_time, nodes_explored

        visited.add(state_to_tuple(current))
        for neighbor in get_neighbors(current):
            if state_to_tuple(neighbor) not in visited:
                heapq.heappush(queue, (misplaced_tiles(neighbor), neighbor, path + [current]))

    return None, time.time() - start_time, nodes_explored

def a_star(start):
    start_time = time.time()
    visited = set()
    queue = []
    heapq.heappush(queue, (misplaced_tiles(start), 0, start, []))
    nodes_explored = 0

    while queue:
        f, g, current, path = heapq.heappop(queue)
        nodes_explored += 1
        if is_goal(current):
            return path + [current], time.time() - start_time, nodes_explored

        visited.add(state_to_tuple(current))
        for neighbor in get_neighbors(current):
            if state_to_tuple(neighbor) not in visited:
                new_g = g + 1
                h = misplaced_tiles(neighbor)
                heapq.heappush(queue, (new_g + h, new_g, neighbor, path + [current]))

    return None, time.time() - start_time, nodes_explored

initial_states = [
    [[1, 2, 3], [4, 0, 6], [7, 5, 8]],
    [[1, 2, 3], [5, 0, 6], [4, 7, 8]],
    [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
]

for idx, state in enumerate(initial_states):
    print(f"\nInitial Board #{idx+1}")
    print("GBFS:")
    path, t, n = greedy_bfs(state)
    print(f"Steps: {len(path)-1}, Time: {t:.4f}s, Nodes: {n}")
    
    print("A*:")
    path, t, n = a_star(state)
    print(f"Steps: {len(path)-1}, Time: {t:.4f}s, Nodes: {n}")
