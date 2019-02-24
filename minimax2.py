import copy
from math import *

class ValuedMove():
    def __init__(self, value, move):
        self.value = value
        self.move = move

    def __lt__(self, other):
        return self.value < other
    def __le__(self, other):
        return self.value <= other
    def __gt__(self, other):
        return self.value > other
    def __ge__(self, other):
        return self.value >= other
    def __eq__(self, other):
        return self.value == other

    def __neg__(self):
        return ValuedMove(-self.value, self.move)

    def __repr__(self):
        if self.move == None:
            return str(self.value) + " " + "None"
        else:
            return str(self.value) + " " + ",".join([str(x) for x in self.move])

def endcheck(field):
	black_legals = find_legal_moves(field, 1)
	red_legals = find_legal_moves(field, 2)
	if not black_legals and not red_legals:
		return True
	else:
		return False

def evaluate(field, max_token):
	black, red = 0, 0
	for i in range(len(field)):
		for j in range(len(field[0])):
			if field[i][j] == 1:
				black += 1
			elif field[i][j] == 2:
				red += 1
	if max_token == 1:
		return black-red
	else:
		return red-black

def evaluate_by_mobility(field, max_token):
    black_moves = len(find_legal_moves(field, 1))
    red_moves = len(find_legal_moves(field, 2))
    if max_token == 1:
        return black_moves - red_moves
    else:
        return red_moves - black_moves

def mock_play(field, move, token):
    if move == None:
        return field
    newfield = copy.deepcopy(field)
    newfield[move[1]][move[0]] = token
    flip_tokens(newfield, move, token)
    return(newfield)

def inv(move):
    if move == None:
        return move
    else:
        return [move[1], move[0]]

def alphabeta(field, depth, alpha, beta, colour, token):
    if depth <= 0 or endcheck(field):
        return ValuedMove(colour * evaluate_by_mobility(field, token), None)
    value = ValuedMove(-inf, None)
    sim_token = token if colour == 1 else 3-token
    legals = find_legal_moves(field, sim_token)
    if legals == []: legals.append(None)
    # print(legals)
    for move in legals:
        # print(move)
        newfield = mock_play(field, move, token)
        value = max(value, ValuedMove(-alphabeta(newfield, depth-1, -beta,
                    -alpha, -colour, token).value, inv(move)))
        alpha = max(alpha, value.value)
        # print(alpha, beta, value)
        if alpha >= beta:
            # print("alpha cutoff")
            break
    return value

def flip_tokens(field, cell, player):
	directions = []
	for i in range(-1, 2):
		for j in range(-1, 2):
			directions.append([i,j])
	directions.remove([0,0])
	runs = []
	for d in directions:
		run = []
		tested_cell = cell
		ended = False
		valid = True
		while not ended:
			run.append(tested_cell)
			tested_cell = [tested_cell[n] + d[n] for n in [0,1]]
			if not on_board(tested_cell):
				valid = False
				break
			if field[tested_cell[1]][tested_cell[0]] != 3-player:
				ended = True
		if valid and field[tested_cell[1]][tested_cell[0]] == player:
			runs.append(run)
	for run in runs:
		for cell in run:
			field[cell[1]][cell[0]] = player

def find_legal_moves(field, player):
	legals = []
	friendly_cells = []
	enemy_cells = []
	for i in range(len(field)):
		for j in range(len(field[0])):
			if field[i][j] == player:
				friendly_cells.append([i,j])
			elif field[i][j] == 3-player:
				enemy_cells.append([i,j])
	surrounds = []
	for i in range(-1, 2):
		for j in range(-1, 2):
			if abs(i) != abs(j):
				surrounds.append([i,j])
	total_occupied = friendly_cells + enemy_cells
	for cell in total_occupied:
		for s in surrounds:
			neighbour = [cell[i]+s[i] for i in [0,1]]
			legal = True
			if neighbour in total_occupied:
				legal = False
			for ordinate in neighbour:
				if not(0 <= ordinate < len(field)):
					legal = False
			if legal:
				legals.append(neighbour)
	truelegals = []
	directions = []
	for i in range(-1, 2):
		for j in range(-1, 2):
			directions.append([i,j])
	directions.remove([0,0])
	for move in legals:
		valid = False
		for d in directions:
			tested_cell = [move[1],move[0]]
			run_length = 0
			while True:
				tested_cell = [tested_cell[i]+d[i] for i in [0,1]]
				if on_board(tested_cell):
					if field[tested_cell[1]][tested_cell[0]] == 3-player:
						run_length += 1
					elif field[tested_cell[1]][tested_cell[0]] == player:
						if run_length > 0:
							valid = True
							break
						else:
							break
					else:
						break
				else: break
		if valid:
			truelegals.append([move[0], move[1]])
	return truelegals

def on_board(cell):
	valid = True
	for coord in cell:
		if not(0<=coord<8):
			valid = False
	return valid
