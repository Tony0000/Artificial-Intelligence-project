def display_board( state ):
	print("-------------")
	print("| %i | %i | %i |" % (state[0], state[1], state[2]))
	print("-------------")
	print("| %i | %i | %i |" % (state[3], state[4], state[5]))
	print("-------------")
	print("| %i | %i | %i |" % (state[6], state[7], state[8]))
	print("-------------")

def move_up(state):
	new_state = state[:]
	idx = new_state.index(0)
	if idx not in [0, 1, 2]:
		new_state[idx - 3], new_state[idx] = new_state[idx], new_state[idx - 3]
		return new_state
	else:
		return None

def move_down(state):
	new_state = state[:]
	idx = new_state.index(0)
	if idx not in [6, 7, 8]:
		new_state[idx + 3], new_state[idx] = new_state[idx], new_state[idx + 3]
		return new_state
	else:
		return None

def move_left(state):
	new_state = state[:]
	idx = new_state.index(0)
	if idx not in [0, 3, 6]:
		new_state[idx - 1], new_state[idx] = new_state[idx], new_state[idx - 1]
		return new_state
	else:
		return None

def move_right(state):
	new_state = state[:]
	idx = new_state.index(0)

	if idx not in [2, 5, 8]:
		new_state[idx + 1], new_state[idx] = new_state[idx], new_state[idx + 1]
		return new_state
	else:
		return None

def expand_children_nodes(node, known_states):
	expanded_nodes = []

	expanded_nodes.append(Node(move_down(node.state), node, "d", node.depth + 1))
	expanded_nodes.append(Node(move_up(node.state), node, "u", node.depth + 1))
	expanded_nodes.append(Node(move_right(node.state), node, "r", node.depth + 1))
	expanded_nodes.append(Node(move_left(node.state), node, "l", node.depth + 1))

	expanded_nodes = [node for node in expanded_nodes if node.state != None and node.state not in [list(state) for state in known_states]]
	return expanded_nodes


"""Performs a breadth first search from the start state to the goal"""
def bfs(start_state, goal_state):
	nodes = []
	known_states = set()
	iterations = 0
	nodes.append(Node(start_state, None, None, 0))
	while True:
		if len( nodes ) == 0: return None
		iterations += 1
		node = nodes.pop(0)
		known_states.add(tuple(node.state))
		if node.state == goal_state:
			moves = []
			temp = node
			print('\nFINISHED')
			display_board(node.state)
			while True:
				moves.insert(0, temp.operator)
				if temp.depth == 1: break
				temp = temp.parent
				display_board(temp.state)
			print('Initial state')
			display_board(temp.parent.state)
			print('Iterations: '+str(iterations))
			return moves

		nodes.extend(expand_children_nodes(node, known_states))

"""Performs a depth first search from the start state to the goal"""
def dfs(start_state, goal_state, depth=5):
	depth_limit = depth
	nodes = []
	known_states = set()
	iterations = 0
	nodes.append(Node(start_state, None, None, 0))
	while True:
		if len(nodes) == 0: return None
		node = nodes.pop(0)
		known_states.add(tuple(node.state))
		iterations += 1
		if node.state == goal_state:
			moves = []
			temp = node
			display_board(node.state)
			while True:
				moves.insert(0, temp.operator)
				if temp.depth <= 1: break
				temp = temp.parent
				display_board(temp.state)
			print('Initial state')
			display_board(temp.parent.state)
			print('Iterations: '+str(iterations))

			return moves

		if node.depth < depth_limit:
			expanded_nodes = expand_children_nodes(node, known_states)
			expanded_nodes.extend(nodes)
			print([i.depth for i in expanded_nodes])
			nodes = expanded_nodes

'''Node data structure'''
class Node:
	def __init__(self, state, parent, operator, depth):
		self.state = state
		self.parent = parent
		self.operator = operator
		self.depth = depth

'''Main method'''
def main():
	goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
	'''Input Unit Test'''
	# start_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]
	# start_state = [1, 2, 3, 0, 4, 5, 7, 8, 6]
	start_state = [0, 2, 3, 1, 4, 5, 7, 8, 6]
	# start_state = [0, 8, 7, 6, 5, 4, 3, 2, 1] # UNSOLVABLE (24 steps)
	result = bfs(start_state, goal_state) 
	if result == None:
		print("No solution found")
	elif result == [None]:
		print("Start node was the goal!")
	else:
		print(result)
		print(len(result), " moves")

if __name__ == "__main__":
	main()
