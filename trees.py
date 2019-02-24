from random import *
from math import *
import time

class Node():
	def __init__(self, value=None, children=[]):
		self.value = value
		self.children = children

	def add_child(self, value=None):
		self.children.append(Node(value, []))

	def __str__(self):
		return(str(self.value))
	def __repr__(self):
		return(str(self.value))


def gen_tree(node, branching_fact=2, depth=2):
	if depth <= 0:
		node.value = randint(-10, 10)
		return node
	for i in range(branching_fact):
		node.add_child()
	for child in node.children:
		gen_tree(child, branching_fact, depth-1)
	return node

# node = Node()
# print(node.children)
# node.add_child()
# print(node.children)
# print(node.children[0].children)
depth = 4


def minimax(node, depth, maximisingPlayer):
	if node.value != None: print(node)
	if not node.children:
		return node.value
	if maximisingPlayer:
		value = -inf
		for child in node.children:
			value = max(value, minimax(child, depth-1, False))
		return value
	else:
		value = inf
		for child in node.children:
			value = min(value, minimax(child, depth-1, True))
		return value

def negamax(node, depth, colour):
	if not node.children:
		return node.value * colour
	value = -inf
	for child in node.children:
		value = max(value, -negamax(child, depth-1, -colour))
	return value

def alphabeta(node, depth, alpha, beta, colour):
	if not node.children:
		return colour * node.value
	value = -inf
	for child in node.children:
		value = max(value, -alphabeta(child, depth-1, -beta, -alpha, -colour))
		alpha = max(alpha, value)
		if alpha >= beta:
			break
	return value

# value = minimax(node, 2, True)
# value2 = negamax(node, 2, 1)
# value3 = alphabeta(node, 2, -inf, inf, 1)
# print("values", value, value2, value3)

node = gen_tree(Node(), 2, 20)
print("value", minimax(node, 2, True))

# trees = []
# for i in range(2):
# 	tree = gen_tree(Node(), 2, i)
# 	trees.append(tree)
#
# print(trees)
#
# f = open("minimax.csv", "w")
# c = 0
# for tree in trees:
# 	print(c+1)
# 	start = time.perf_counter()
# 	value = minimax(tree, 2, True)
# 	end = time.perf_counter()
# 	out = ",".join([str(c+1),str(end-start)]) + "\n"
# 	c+=1
# 	f.write(out)
