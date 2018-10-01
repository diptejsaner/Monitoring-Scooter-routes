from collections import deque
import copy
import time

start_time = time.clock()


class GridElement:
    def __init__(self, val, i, j):
        self.val = val
        self.i = i
        self.j = j


class Stack:
    def __init__(self):
        self.__list = deque()

    def push(self, key):
        self.__list.append(key)

    def pop(self):
        return self.__list.pop()

    def is_empty(self):
        return len(self.__list) == 0


class Position:
    def __init__(self, i, j):
        self.i = i
        self.j = j


class State:
    def __init__(self, grid, score, num_officers_placed, a_sum, parent, children):
        self.grid = grid
        self.score = score
        self.num_officers_placed = num_officers_placed
        self.available_sum = a_sum
        self.parent = parent
        self.children = children


def visit(state, grid_element):
    grid = copy.deepcopy(state.grid)
    glen = len(grid)
    (i, j) = grid_element.i, grid_element.j
    exclude_sum = 0

    r = i + 1
    c = j + 1
    while r < glen and c < glen:
        if grid[r][c] != -1:
            exclude_sum += grid[r][c]
            grid[r][c] = -1

        r += 1
        c += 1

    r = i - 1
    c = j - 1
    while r >= 0 and c >= 0:
        if grid[r][c] != -1:
            exclude_sum += grid[r][c]
            grid[r][c] = -1
        r -= 1
        c -= 1

    r = i + 1
    c = j - 1
    while r < glen and c >= 0:
        if grid[r][c] != -1:
            exclude_sum += grid[r][c]
            grid[r][c] = -1
        r += 1
        c -= 1

    r = i - 1
    c = j + 1
    while r >= 0 and c < glen:
        if grid[r][c] != -1:
            exclude_sum += grid[r][c]
            grid[r][c] = -1
        r -= 1
        c += 1

    r = i
    c = 0
    while c < glen:
        if c != j:
            if grid[r][c] != -1:
                exclude_sum += grid[r][c]
                grid[r][c] = -1
        c += 1

    r = 0
    c = j
    while r < glen:
        if r != i:
            if grid[r][c] != -1:
                exclude_sum += grid[r][c]
                grid[r][c] = -1
        r += 1

    # also mark the currently placed officer position as visited
    # exclude_sum += grid[i][j]
    grid[i][j] = -1

    n_state = State(grid, state.score + grid_element.val, state.num_officers_placed + 1, state.available_sum - exclude_sum, state, None)

    # return grid
    return n_state


def get_children(state):
    n = len(state.grid)
    children_states = []

    for i in range(n):
        for j in range(n):
            val = state.grid[i][j]
            if val != -1:
                # c_grid = visit(state, GridElement(val, i, j))
                # c_parent = state
                # c_children = None
                # c_num_officers_placed = state.num_officers_placed + 1

                # c_state = State(c_grid, state.score + val, c_num_officers_placed, c_parent, c_children)
                c_state = visit(state, GridElement(val, i, j))
                children_states.append(c_state)

    return children_states


def dfs(start_state, num_officers):
    s = Stack()
    s.push(start_state)
    m_heuristic = 0
    max_activity_points = 0

    while not s.is_empty():
        if time.clock() - start_time > 170:
            return max_activity_points

        state = s.pop()
        if state.available_sum <= m_heuristic:
            continue
        else:
            m_heuristic = state.available_sum

        if state.num_officers_placed == num_officers:
            if state.score > max_activity_points:
                max_activity_points = state.score
            continue

        # make the max heuristic smaller since we have selected an element
        # m_heuristic -=
        children = get_children(state)
        children.sort(key=lambda x: x.score)

        for child_state in children:
            s.push(child_state)

    return max_activity_points


n = -1
p = -1
s = -1
grid = [[]]

with open('input3.txt') as inputFile:
    lcount = 0
    for line in inputFile:
        line.rstrip()

        if lcount == 0:
            n = int(line)
            grid = [[0 for x in range(n)] for y in range(n)]
        elif lcount == 1:
            p = int(line)
        elif lcount == 2:
            s = int(line)
        else:
            (i, j) = line.rstrip().split(",")
            i = int(i)
            j = int(j)

            grid[i][j] += 1

        lcount += 1


# testgrid1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
testgrid2 = [[0, 4, 0, 0], [1, 0, 0, 0], [0, 5, 5, 0], [5, 8, 0, 0]]
# testgrid3 = [[22, 25, 6, 35, 2, 43, 11, 22], [41, 43, 48, 20, 38, 4, 28, 43], [41, 12, 48, 8, 36, 9, 46, 3], [27, 13, 37, 29, 17, 27, 24, 35], [34, 25, 21, 24, 7, 45, 39, 21], [10, 31, 31, 24, 19, 16, 15, 24], [1, 6, 27, 13, 31, 18, 23, 33], [35, 26, 28, 10, 30, 3, 35, 7]]
grid = testgrid2

n = 4
p = 3

grid_elements = []
total_sum = 0

for i in range(n):
    for j in range(n):
        grid_elements.append(GridElement(grid[i][j], i, j))
        total_sum += grid[i][j]

grid_elements.sort(key=lambda x: x.val, reverse=True)

initial_state = State(grid, 0, 0, total_sum, None, None)
max_activity_points = 0
max_heuristic = 0



for i in range(len(grid_elements)):
    num_officers = p
    activity_points = 0

    # start_grid = visit(initial_state, grid_elements[i])
    # start_state = State(start_grid, grid_elements[i].val, 1, None, None)
    start_state = visit(initial_state, grid_elements[i])
    if start_state.available_sum < max_heuristic:
        continue
    else:
        max_heuristic = start_state.available_sum

    activity_points = dfs(start_state, num_officers)

    if activity_points > max_activity_points:
        max_activity_points = activity_points

    if time.clock() - start_time > 170:
        break

    # print activity_points,

print grid
print "Max points " + str(max_activity_points)
print time.clock() - start_time, "seconds"
# with open('output.txt', 'w') as outputFile:
#     outputFile.write(str(max_activity_points))