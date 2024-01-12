
import copy
import sys

# Set the recursion limit for the system.
sys.setrecursionlimit(10 ** 6)

# Create functions for each floor to check if all residents can be taken and update the floor's occupancy accordingly.

def go_to_floor1(state):
    # Check if there is space in the elevator and residents are present on the first floor.
    if state[-1] < 8 and state[1] > 0:
        # Check if there are more residents on the first floor than the available space in the elevator.
        if state[1] > 8 - state[-1]:
            new_state = [1] + [state[1] + state[-1] - 8] + [state[2]] + [state[3]] + [state[4]] + [8]
        else:
            new_state = [1] + [0] + [state[2]] + [state[3]] + [state[4]] + [state[1] + state[-1]]
            
        return new_state

# Similar functions for the other floors.

# Function that runs each time the elevator is full and moves to the roof, then resets the number of residents in the elevator.

def go_to_roof(state):
    if state[-1] == 8 or (state[1] == 0 and state[2] == 0 and state[3] == 0 and state[4] == 0):
        new_state = [5] + [state[1]] + [state[2]] + [state[3]] + [state[4]] + [0]
        return new_state

# Find the children states from the current state.

def find_children(state):
    children = []

    roof_state = copy.deepcopy(state)
    roof_child = go_to_roof(roof_state)

    # Similar processing for other floors.

    if roof_child is not None:
        children.append(roof_child)

    # Append children states for other floors.

    return children

# Initialize the front.

def make_front(state):
    return [state]

# Expand the front for either DFS or BFS.

def expand_front(front, method):
    if method == "DFS":
        if front:
            print("Front:")
            print(front)
            node = front.pop(0)
            for child in find_children(node):
                front.insert(0, child)
    elif method == "BFS":
        if front:
            print("Front:")
            print(front)
            node = front.pop(0)
            for child in find_children(node):
                front.append(child)
    return front

# The main function that performs the recursive search.

def find_solution(front, queue, closed, goal, method):
    if not front:
        print("_NO_SOLUTION_FOUND_")
    elif front[0] in closed:
        new_front = copy.deepcopy(front)
        new_front.pop(0)
        new_queue = copy.deepcopy(queue)
        new_queue.pop(0)
        find_solution(new_front, new_queue, closed, goal, method)
    elif is_goal_state(front[0], goal):
        print("_GOAL_FOUND_")
        print(front[0])
    else:
        if method == "DFS":
            closed.append(front[0])
            front_copy = copy.deepcopy(front)
            front_children = expand_front(front_copy, method)
            queue_copy = copy.deepcopy(queue)
            queue_children = extend_queue(queue_copy, method)
            closed_copy = copy.deepcopy(closed)
        elif method == "BFS":
            closed.append(front[0])
            front_copy = copy.deepcopy(front)
            front_children = expand_front(front_copy, method)
            front_copy.sort()
            front_children.sort()
            queue_copy = copy.deepcopy(queue)
            queue_children = extend_queue(queue_copy, method)
            queue_copy.sort()
            queue_children.sort()
            closed_copy = copy.deepcopy(closed)
        find_solution(front_children, queue_children, closed_copy, goal, method)

# Check if the front state is equal to the goal state.

def is_goal_state(front, goal):
    return front == goal

# Initialize the queue.

def make_queue(state):
    return [[state]]

# Extend the queue based on the search method.

def extend_queue(queue, method):
    if method == "DFS":
        print("Queue:")
        print(queue)
        node = queue.pop(0)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0, path)
    elif method == "BFS":
        print("Queue:")
        print(queue)
        node = queue.pop(0)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.append(path)
    return queue_copy

# The main function that initializes the states and starts the search.

def main():
    # Declare the initial and goal states of the problem.
    initial_state = [0, 9, 4, 12, 7, 0] 
    goal = [5, 0, 0, 0, 0, 0] 
    
    # Menu for choosing the blind algorithm to use.
    print("Choose search algorithm: \n1. Depth-First Search (DFS)\n2. Breadth-First Search (BFS")
    choice = int(input("Enter your choice (1 or 2): "))

    if choice == 1:
        method = "DFS"
    elif choice == 2:
        method = "BFS"   
    else:
        print("Invalid choice. Exiting.")
        return 0
    
    # Begin the search.
    print('____BEGIN__SEARCHING____')
    find_solution(make_front(initial_state), make_queue(initial_state), [], goal, method)

if __name__ == "__main__":
    main()
