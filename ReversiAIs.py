import random
from math import *
import copy

def random_move(field, legals, depth=None, maximisingPlayer=None, max_token=None, alpha=None, beta=None):
	# print(legals)
	move = random.choice(legals)
	move = [move[1], move[0]]
	# print(move)
	return [None, move]

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

def minimax(field, legals, depth, maximisingPlayer, max_token, alpha=None, beta=None):
	# print(maximisingPlayer, depth)
	# print(legals)
	if depth <= 0 or endcheck(field):
		# print('done')
		return evaluate(field, max_token)
	if maximisingPlayer:
		best_move = [0,0]
		value = -inf
		if not legals:
			print("no legals")
			newlegals = find_legal_moves(field, 3-max_token)
			minmax = minimax(field, newlegals, depth-1, False, max_token)
			try:
				if minmax >= value:
					value = minmax
					best_move = None
			except:
				if minmax[0] >= value:
					value = minmax[0]
					best_move = None
			if best_move:
				best_move = [best_move[1],best_move[0]]
			return [value, best_move]
		for move in legals:
			newfield = copy.deepcopy(field)
			newfield[move[1]][move[0]] = max_token
			flip_tokens(newfield, move, max_token)
			newlegals = find_legal_moves(newfield, 3-max_token)
			minmax = minimax(newfield, newlegals, depth-1, False, max_token)
			try:
				if minmax >= value:
					value = minmax
					best_move = move
			except:
				if minmax[0] >= value:
					value = minmax[0]
					best_move = move
		if best_move:
			best_move = [best_move[1],best_move[0]]
		return [value, best_move]
	else: #minimising player
		value = inf
		best_move = [0,0]
		if not legals:
			# print("no legals")
			newlegals = find_legal_moves(field, max_token)
			minmax = minimax(field, newlegals, depth-1, True, max_token)
			try:
				if minmax <= value:
					value = minmax
					best_move = None
			except:
				if minmax[0] <= value:
					value = minmax[0]
					best_move = None
			if best_move:
				best_move = [best_move[1],best_move[0]] 
			return [value, best_move]
		for move in legals:
			newfield = copy.deepcopy(field)
			newfield[move[1]][move[0]] = 3-max_token
			flip_tokens(newfield, move, 3-max_token)
			newlegals = find_legal_moves(newfield, max_token)
			minmax = minimax(newfield, newlegals, depth-1, True, max_token)
			try:
				if minmax <= value:
					value = minmax
					best_move = move
			except:
				if minmax[0] <= value:
					value = minmax[0]
					best_move = move
		if best_move:
			best_move = [best_move[1],best_move[0]]
		return [value, best_move]


def alphabeta(field, legals, depth, maximisingPlayer, max_token, alpha, beta):
	# print(maximisingPlayer, depth)
	# print(legals)
	if depth <= 0 or endcheck(field):
		# print('done')
		return evaluate(field, max_token)
	if maximisingPlayer:
		best_move = [0,0]
		value = -inf
		if not legals:
			print("no legals")
			newlegals = find_legal_moves(field, 3-max_token)
			minmax = alphabeta(field, newlegals, depth-1, False, max_token, alpha, beta)
			try:
				if minmax >= value:
					value = minmax
					best_move = None
			except:
				if minmax[0] >= value:
					value = minmax[0]
					best_move = None
			alpha = max(alpha, value)
			if best_move:
				best_move = [best_move[1],best_move[0]]

			return [value, best_move]
		for move in legals:
			newfield = copy.deepcopy(field)
			newfield[move[1]][move[0]] = max_token
			flip_tokens(newfield, move, max_token)
			newlegals = find_legal_moves(newfield, 3-max_token)
			minmax = alphabeta(newfield, newlegals, depth-1, False, max_token, alpha, beta)
			try:
				if minmax >= value:
					value = minmax
					best_move = move
			except:
				if minmax[0] >= value:
					value = minmax[0]
					best_move = move
			alpha = max(alpha, value)

			if alpha >= beta:
				break #beta cut off
		if best_move:
			best_move = [best_move[1],best_move[0]]
		return [value, best_move]
	else: #minimising player
		value = inf
		best_move = [0,0]
		if not legals:
			# print("no legals")
			newlegals = find_legal_moves(field, max_token)
			minmax = alphabeta(field, newlegals, depth-1, True, max_token, alpha, beta)
			try:
				if minmax <= value:
					value = minmax
					best_move = None
			except:
				if minmax[0] <= value:
					value = minmax[0]
					best_move = None
			beta = min(beta, value)
			if best_move:
				best_move = [best_move[1],best_move[0]]
			return [value, best_move]
		for move in legals:
			newfield = copy.deepcopy(field)
			newfield[move[1]][move[0]] = 3-max_token
			flip_tokens(newfield, move, 3-max_token)
			newlegals = find_legal_moves(newfield, max_token)
			minmax = alphabeta(newfield, newlegals, depth-1, True, max_token, alpha, beta)
			try:
				if minmax <= value:
					value = minmax
					best_move = move
			except:
				if minmax[0] <= value:
					value = minmax[0]
					best_move = move
			beta = min(beta, value)
			if alpha >= beta:
				break #alpha cut off
		if best_move:
			best_move = [best_move[1],best_move[0]]
		return [value, best_move]

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
