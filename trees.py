class Node():
	def __init__(self, value=None, children=[]):
		self.value = value
		self.children = children

	def add_child(self, value=None):
		self.children.append(Node(value))

def gen_tree(node,branching_fact=2, depth=5):
	if depth <=0:
		return node
	for i in range(branching_fact):
		node.add_child()
	for child in node.children:
		return gen_tree(child, branching_fact, depth-1)

node = Node()
gen_tree(node)
print(node.children)



