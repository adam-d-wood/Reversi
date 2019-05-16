f = open("cutoffs.csv", "w")

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
    def __sub__(self, other):
        return ValuedMove(self.value - other, self.move)

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

def evaluate_by_territory(field, max_token):
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

def evaluate_by_weight(field, max_token):
    weightings = ([100,-5,5,5,5,5,-5,100],
                [-5,0,0,0,0,0,0,-5],
                [5,0,0,0,0,0,0,5],
                [5,0,0,0,0,0,0,5],
                [5,0,0,0,0,0,0,5],
                [5,0,0,0,0,0,0,5],
                [-5,0,0,0,0,0,0,-5],  
                [100,-5,5,5,5,5,-5,100])
    result = 0
    for i in range(len(weightings)):
        for j in range(len(weightings[0])):
            if field[i][j] == 1:
                mult = 1
            elif field[i][j] == 2:
                mult = -1
            else: mult = 0
            result += mult * weightings[i][j]
    # print(result)
    return result

def count_frontiers(field):
    black, red = 0, 0
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] != 0:
                surrounds = [(0,1), (0,-1), (-1,0), (1,0)]
                frontier = False
                for s in surrounds:
                    cell = [i+s[0], j+s[1]]
                    if on_board(cell) and field[cell[0]][cell[1]] == 0:
                        frontier = True
                if frontier:
                    if field[i][j] == 1: black += 1
                    else: red += 1
    # print(black, red)
    return [black, red]

def evaluate_by_mobility(field, max_token):
    black_moves = len(find_legal_moves(field, 1))
    red_moves = len(find_legal_moves(field, 2))
    team = 1 if max_token == 1 else (-1)
    mobility = black_moves - red_moves
    return mobility * team

def mock_play(field, move, token):
    if move == None:
        return field
    newfield = copy.deepcopy(field)
    newfield[move[0]][move[1]] = token
    flip_tokens(newfield, [move[1],move[0]], token)
    return(newfield)

def evaluate_by_frontiers(field, max_token):
    frontiers = count_frontiers(field)
    # print(frontiers)
    black, red = frontiers
    if max_token == 1:
        return red-black
    elif max_token == 2:
        return black-red

def count_frees(field):
    free_tiles = 0
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == 0:
                free_tiles += 1
    return free_tiles

def evaluate_2(field, max_token):
    discs = 64 - count_frees(field)
    EC = 500
    MC = 350 - 2 * discs
    # if discs < 10:
    #     SC = 200 - discs
    # elif discs < 20:
    #     SC =  190-2*(discs-10)
    # elif discs < 40:
    #     SC = 170-5*(discs-20)
    # elif discs < 50:
    #     SC = 70 - 7*(discs-40)
    # else:
    #     SC = 0

def evaluate(field, max_token, tiles_left):
    if tiles_left > 5:
        mc = 1 #1
        fc = 1 #20
        ec = 1
        mobility = evaluate_by_mobility(field, max_token)
        frontiers = evaluate_by_frontiers(field, max_token)
        edges = evaluate_by_weight(field, max_token)
        # print(mobility, frontiers, edges)
        # print(mobility, fc*frontiers)
        return mobility*mc + fc*frontiers + ec*edges
    else:
        return evaluate_by_territory(field, max_token)

def inv(move):
    if move == None:
        return move
    else:  
        return [move[1], move[0]]


def negascout(field, depth, alpha, beta, colour, token, tiles_left):
    if depth <= 0 or endcheck(field):
        return ValuedMove(colour * evaluate(field, token, tiles_left), None)
    sim_token = token if colour == 1 else 3-token
    legals = find_legal_moves(field, sim_token)
    ordered_val_legals = []
    order_moves(field, depth-1, colour, token, tiles_left, legals, ordered_val_legals)
    ordered_legals = deval(ordered_val_legals)
    if not ordered_legals:
        ordered_legals = legals
    if ordered_legals == []: ordered_legals.append(None)
    # print(ordered_legals)
    for move in ordered_legals:
        newfield = mock_play(field, move, sim_token)
        if move == ordered_legals[0]:
            score = ValuedMove(-negascout(newfield, depth-1, -beta, -alpha, -colour, token, tiles_left).value, inv(move))
        else:
            score = ValuedMove(-negascout(newfield, depth-1, -alpha-1, -alpha, -colour, token, tiles_left).value, inv(move))
            if alpha < score < beta:
                score = ValuedMove(-negascout(newfield, depth-1, -beta, -score, -colour, token, tiles_left).value, inv(move))
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    # print("returning", alpha)
    return alpha



def alphabeta(field, depth, alpha, beta, colour, token, tiles_left):
    if depth <= 0 or endcheck(field):
        return ValuedMove(colour * evaluate(field, token, tiles_left), None)
    value = ValuedMove(-inf, None)
    sim_token = token if colour == 1 else 3-token
    # print("sim", sim_token)
    legals = find_legal_moves(field, sim_token)
    # if legals == []: legals.append(None)
    # print(legals)
    ordered_val_legals = []
    order_moves(field, depth-1, colour, token, tiles_left, legals,
                                ordered_val_legals)
    ordered_legals = deval(ordered_val_legals)
    if not ordered_legals:
        ordered_legals = legals
    # print("", ordered_legals)
    # print(legals)
    # print("legals: ", legals)
    # print("ordered_legals", ordered_legals)
    if ordered_legals == []: ordered_legals.append(None)
    # print()
    for move in ordered_legals:
        # print(move)
        newfield = mock_play(field, move, sim_token)
        # print(move)
        # display_field(newfield)
        value = max(value, ValuedMove(-alphabeta(newfield, depth-1, -beta,
                    -alpha, -colour, token, tiles_left).value, inv(move)))
        alpha = max(alpha, value.value)
        # print(alpha, beta, value)
        # print()
        if alpha >= beta:
            if token == 1: f.write("1+")
            # pass
            # print("alpha cutoff")
            break
    return value

def order_moves(field, depth, colour, token, tiles_left, legals, ordered_legals):
    # print(depth)
    cont = True
    if depth <= 0 or endcheck(field):
        # print("end")
        return ValuedMove(colour * evaluate(field, token, tiles_left), None)
    sim_token = token if colour == 1 else 3-token
    for move in legals:
        newfield = mock_play(field, move, sim_token)
        # print(len(ordered_legals), len(legals))
        if len(ordered_legals) < len(legals):
            # print("ya")
            value = ValuedMove(-order_moves(newfield, depth-1, -colour, token, 
                                tiles_left, legals, ordered_legals).value, move)
        else: 
            cont = False
            value = ValuedMove(0, None)
            # print(value)
            # print("h")
        # print(value)
        # print("depth: ", depth)
        # print("depth", depth)
        if depth == 1 and cont:
            # print("yuh")
            # print(depth)
            insert_in_order(value, ordered_legals)
            # print(ordered_legals)
        # print(ordered_legals, len(ordered_legals))
        if not cont: break
    # print('end')
    return ValuedMove(0, None)

def deval(valmoves):    
    # print("valmoves", valmoves)
    result = []
    for valmove in valmoves:
        result.append(valmove.move)
    return result

def insert_in_order(value, ordered_legals):
    # print(value)
    ordered_legals.append(value)
    # print(ordered_legals)
    ordered_legals.sort()
    return ordered_legals.reverse()
    # return ordered_legals

def display_field(field):
    for i in range(len(field)):
        print(field[i])
    print('\n')


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

def find_neighbours(field, player):
    neighbours = []
    occupied_cells = []
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] != 0:
                occupied_cells.append([i,j])
    surrounds = [(0,1), (0,-1), (-1,0), (1,0)]
    for cell in occupied_cells:
        for s in surrounds:
            neighbour = [cell[i]+s[i] for i in [0,1]]
            if on_board(neighbour) and field[neighbour[0]][neighbour[1]] == 0:
                neighbours.append(neighbour)
    return neighbours

def validate_neighbours(neighbours, field, player):
    legals = []
    directions = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            directions.append([i,j])
    directions.remove([0,0])
    for move in neighbours:
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
            legals.append([move[0], move[1]])
    return legals

def find_legal_moves(field, player):
    neighbours = find_neighbours(field, player)
    legals = validate_neighbours(neighbours, field, player)
    return delete_duplicates(legals)

def delete_duplicates(legals):
    result = []
    for move in legals:
        if move not in result:
            result.append(move)
    return result

def on_board(cell):
	valid = True
	for coord in cell:
		if not(0<=coord<8):
			valid = False
	return valid
