from collections import deque
from dataclasses import dataclass
import queue
import sys

class State:
    name: str
    cost: float
    path: str
    path_length: int
    heuristic: float

    def __gt__(self, U):
        if self.cost == U.cost:
            return self.name > U.name
        return self.cost > U.cost
    def __init__(self, name, cost, path, path_length, heuristic):
        self.name = name
        self.cost = cost
        self.path = path
        self.path_length = path_length
        self.heuristic = heuristic
        

index = {}

def insert_bfs(cur_state: State, open: list, costs: list, visited: list):
    for state in costs[cur_state.name]:
        if visited[index[state]] == False:
            new_state = State(state,
                         cur_state.cost + costs[cur_state.name][state],
                         cur_state.path + " => " + state,
                         cur_state.path_length + 1, 0)
            open.append(new_state)

def insert_ucs(cur_state: State, open: list, costs: list, visited: list):
    for state in costs[cur_state.name]:
        if visited[index[state]] == False:
            new_state = State(state,
                         cur_state.cost + costs[cur_state.name][state],
                         cur_state.path + " => " + state,
                         cur_state.path_length + 1, 0)
            #print((new_state.cost, new_state.name, new_state))
            open.put((new_state.cost, new_state))
            


def insert_Astar(cur_state: State, open: list, costs: list, visited: list):
    for state in costs[cur_state.name]:
        if visited[index[state]] < cur_state.cost + costs[cur_state.name][state]:
            new_state = State(state,
                         cur_state.cost + costs[cur_state.name][state],
                         cur_state.path + " => " + state,
                         cur_state.path_length + 1, heuristic[index[state]])
            open.append(new_state)
    
    open = open.sort(key = lambda x: x.cost + x.heuristic)

def search_aSTAR(first_state: str, final_states: list, costs: list):
    visited = [-1 for i in range(len(index))]
    no_visited = 0
    cur_state = State(first_state, 0, first_state, 1, heuristic[index[first_state]])
    open = []
    open.append(cur_state)

    while (cur_state.name not in final_states) and open:
        cur_state = open.pop(0)
        if visited[index[cur_state.name]] < cur_state.cost and visited[index[cur_state.name]] != -1:
            continue
        visited[index[cur_state.name]] = cur_state.cost
        no_visited+=1
        insert_Astar(cur_state, open, costs, visited)
        
    return (cur_state.name in final_states), no_visited, cur_state.path_length, cur_state.cost, cur_state.path

def search_bfs(first_state: str, final_states, costs):
    visited = [False for i in range(len(costs))]
    no_visited = 0
    cur_state = State(first_state, 0, first_state, 1, 0)
    open = deque()
    open.append(cur_state)

    while (cur_state.name not in final_states) and open:
        cur_state = open.popleft()
        if visited[index[cur_state.name]] == True:
            continue

        visited[index[cur_state.name]] = True
        no_visited+=1
        insert_bfs(cur_state, open, costs, visited)

    return (cur_state.name in final_states), no_visited, cur_state.path_length, cur_state.cost, cur_state.path


def search_ucs(first_state: str, final_states, costs):
    visited = [False for i in range(len(costs))]
    no_visited = 0
    cur_state = State(first_state, 0, first_state, 1, 0)
    open = queue.PriorityQueue()
    open.put((cur_state.cost, cur_state))

    while (cur_state.name not in final_states) and not open.empty():
        head = open.get()
        cur_state = head[1]
        if visited[index[cur_state.name]] == True:
            continue

        visited[index[cur_state.name]] = True
        no_visited+=1
        insert_ucs(cur_state, open, costs, visited)

    return (cur_state.name in final_states), no_visited, cur_state.path_length, cur_state.cost, cur_state.path

def dijkstra(final_states, costs):
    h_star = [-1 for i in range(len(index))]
    open = queue.PriorityQueue()
    for x in final_states:
        h_star[index[x]] = 0.0
        open.put((0.0, x))

    while not open.empty():
        state = open.get()[1]
        for i in index:
            if costs[i].get(state, 0) != 0:
                if h_star[index[i]] == -1 or h_star[index[i]] > h_star[index[state]] + costs[i][state]:
                    h_star[index[i]] = h_star[index[state]] + costs[i][state]
                    open.put((h_star[index[i]], i))

    return h_star

def heuristic_optimistic(final_states, costs, heuristic):
    h_star = dijkstra(final_states, costs)
    optimistic = True
    for state in index:
        if heuristic[index[state]] <= h_star[index[state]]:
            print("[CONDITION]: [OK] h(" + state + ") <= h*: " + str(heuristic[index[state]]) + " <= " + str(h_star[index[state]]))
        else:
            print("[CONDITION]: [ERR] h(" + state + ") <= h*: " + str(heuristic[index[state]]) + " <= " + str(h_star[index[state]]))
            optimistic = False
    
    if optimistic:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")
    return

def heuristic_consistent(costs, heuristic):
    consistent = True
    for state in index:
        for state2 in index:
            if costs[state].get(state2, 0) != 0:
                if heuristic[index[state]] <= heuristic[index[state2]] + costs[state][state2]:
                    print("[CONDITION]: [OK] h(" + state + ") <= h(" + state2 + ") + c: " + str(heuristic[index[state]]) + " <= " + str(heuristic[index[state2]]) + " + " + str(costs[state][state2]))
                else:
                    print("[CONDITION]: [ERR] h(" + state + ") <= h(" + state2 + ") + c: " + str(heuristic[index[state]]) + " <= " + str(heuristic[index[state2]]) + " + " + str(costs[state][state2]))
                    consistent = False
    if consistent:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")
    return

def load_next_line(cost_file):
    line = cost_file.readline().strip()
    if len(line) == 0:
        return 0
    if line[0] != "#":
        return line
    return load_next_line(cost_file)

def load_costs(path: str):
    with open(path) as cost_file:
        first = load_next_line(cost_file) # ucitavanje pocetnog stanja
        final = load_next_line(cost_file).split(" ") # ucitavanje zavrsnog stanja
        x = load_next_line(cost_file)
        n = 0
        while x:
            list = {}
            state = x.split(":")
            if(len(state[1]) == 0):
                x = load_next_line(cost_file)
                costs[state[0]] = list
                index[state[0]] = n
                n += 1
                continue
            for entry in state[1][1:].split(" "):
                prijelaz = entry.split(",")
                list[prijelaz[0]] = float(prijelaz[1])
            costs[state[0]] = list
            index[state[0]] = n
            n += 1
            x = load_next_line(cost_file)
    return first, final

def load_heuristic(path: str):
    heuristic_file = open(path)
    heuristic = [0 for i in range(len(costs))]
    line = load_next_line(heuristic_file)
    while line:
        h = line.split(":")
        heuristic[index[h[0]]] = float(h[1])
        line = load_next_line(heuristic_file)
    return heuristic


costs = {}
algoritam = ""
optimistic = False
consistent = False
h_path = ""
cost_path = ""

# argparse
for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "--alg":
        algoritam = sys.argv[i + 1]
    if sys.argv[i] == "--ss":
        cost_path = sys.argv[i + 1]
    if sys.argv[i] == "--h":
        h_path = sys.argv[i + 1]
    if sys.argv[i] == "--check-optimistic":
        optimistic = True
        i -= 1
    if sys.argv[i] == "--check-consistent":
        consistent = True
        i -= 1

first, final = load_costs(cost_path)
sorted_index = sorted(index)
if algoritam == "astar":
    heuristic = load_heuristic(h_path)
    found, no_visited, path_length, cost, path = search_aSTAR(first, final, costs)
    print("# A-STAR " + cost_path)
    if found:
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: " + str(no_visited))
        print("[PATH_LENGTH]: " + str(path_length))
        print("[TOTAL_COST]: " + str(cost))
        print("[PATH]: " + path)
    else:
        print("[FOUND_SOLUTION]: no")
elif algoritam == "bfs":
    found, no_visited, path_length, cost, path = search_bfs(first, final, costs)
    print("# BFS " + cost_path)
    if found:
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: " + str(no_visited))
        print("[PATH_LENGTH]: " + str(path_length))
        print("[TOTAL_COST]: " + str(cost))
        print("[PATH]: " + path)
    else:
        print("[FOUND_SOLUTION]: no")
elif algoritam == "ucs":
    found, no_visited, path_length, cost, path = search_ucs(first, final, costs)
    print("# UCS " + cost_path)
    if found:
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: " + str(no_visited))
        print("[PATH_LENGTH]: " + str(path_length))
        print("[TOTAL_COST]: " + str(cost))
        print("[PATH]: " + path)
    else:
        print("[FOUND_SOLUTION]: no")

if consistent:
    print("# HEURISTIC-CONSISTENT " + h_path)
    heuristic = load_heuristic(h_path)
    heuristic_consistent(costs, heuristic)
if optimistic:
    print("# HEURISTIC-OPTIMISTIC " + h_path)
    heuristic = load_heuristic(h_path)
    heuristic_optimistic(final, costs, heuristic)