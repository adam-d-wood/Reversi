def find_neighbours(field, player):
    neighbours = []
    enemy_cells = []
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == 3-player:
                enemy_cells.append([i,j])
    surrounds = [(0,1), (0,-1), (-1,0), (1,0)]
    for cell in enemy_cells:
        for s in surrounds:
            neighbour = [cell[i]+s[i]] for i in [0,1]]
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
            legals.append([move[0], move[1]])
    return legals

def find_legal_moves(field, player):
    neighbours = find_neighbours(field, player)
    return validate_neighbours(neighbours, field, player)
