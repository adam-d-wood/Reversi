def stable

def alphabeta(field, depth, alpha, beta, colour, token):
    if depth <= 0 or endcheck(field):
        return ValuedMove(colour * evaluate_by_stability(field, token), None)
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

def evaluate_by_stability(field, legals):
	legals = find_legal_moves(field)
    for i in range(len(field)):
        for j in range(len(field[0])):
            disc = field[i][j]
            stable = test_stability(field, disc, [i,j], legals)

def test_stability(field, dics, indices, legals):
    a, b = indices
    colour = disc
    for move in legals:
        newfield = mock_play(field, move, t)

