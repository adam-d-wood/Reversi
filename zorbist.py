import random

def bitstring():
	string = ''
	for i in range(64):
		string += random.choice(['0', '1'])
	return string


def init_zorbist_hash():
	table = [[None for i in range(3)] for j in range(64)]
	for i in range(64):
		for j in range(3):
			table[i][j] = bitstring()
	return table

table = init_zorbist_hash()

def random_genboard():
	board = [[random.randint(0,2) for i in range(8)] for j in range(8)]
	return board

def hash(board, table):
	h = 0
	for i in range(8):
		for j in range(8):
			if board[i][j] != 0:
				k = board[i][j]
				h = h ^ int(table[8*i + j][k], 2)
	return hex(h)[2:]

for i in range(10000):
	print(hash(random_genboard(), table))
