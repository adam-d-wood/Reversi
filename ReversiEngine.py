import ReversiGraphics as graphics
import ReversiBoard as rboard
import ReversiAIs as comps
import copy
import pygame
from math import *

board = rboard.Board(8, 8)
window = graphics.Window()

class Reversi():

	def __init__(self):
		self.display = window.setup_display(board)
		self.game_running = True
		self.black_turn = True
		self.missed_turns = 0
		self.clock = pygame.time.Clock()
		self.human_players = []
		self.human_turn = False
		# self.computer = comps.random_move
		self.black_player = comps.alphabeta
		self.red_player = comps.random_move
		self.ai_delay = 0

	def draw(self):
		window.draw_board(self.display, board, self)

	def turn_token(self):
		if self.black_turn: return 1
		else: return 2

	def game_ended(self, board):
		if self.missed_turns >= 2:
			return True

	def insert_token(self, cell, field):
		col, row = cell
		# print(self.find_legal_moves(board))
		if [row, col] in self.find_legal_moves(board):
			# print('yep')
			success = True
			field[row][col] = self.turn_token()
		else:
			# print('nah')
			success = False
		return success

	def find_legal_moves(self, board):
		legals = []
		friendly_cells = []
		enemy_cells = []
		for i in range(board.rows):
			for j in range(board.cols):
				if board.field[i][j] == self.turn_token():
					friendly_cells.append([i,j])
				elif board.field[i][j] == 3-self.turn_token():
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
					if not(0 <= ordinate < board.cols):
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
					if self.on_board(tested_cell):
						if board.field[tested_cell[1]][tested_cell[0]] == 3-self.turn_token():
							run_length += 1
						elif board.field[tested_cell[1]][tested_cell[0]] == self.turn_token():
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



		# for move in legals:
		# 	fieldcopy = copy.deepcopy(board.field)
		# 	fieldcopy[move[1]][move[0]] = self.turn_token()
		# 	newfield = copy.deepcopy(fieldcopy)
		# 	self.flip_tokens(fieldcopy, move)
		# 	if fieldcopy != newfield:
		# 		truelegals.append([move[1], move[0]])
		return truelegals

	# def mock_flip_tokens(self, board, cell):

	def on_board(self, cell):
		valid = True
		for coord in cell:
			if not(0<=coord<8):
				valid = False
		return valid

	def flip_tokens(self, field, cell):
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
				if not self.on_board(tested_cell):
					valid = False
					break
				if field[tested_cell[1]][tested_cell[0]] != 3-self.turn_token():
					ended = True
			if valid and field[tested_cell[1]][tested_cell[0]] == self.turn_token():
				runs.append(run)
		for run in runs:
			for cell in run:
				field[cell[1]][cell[0]] = self.turn_token()

	def count_tokens(self, board):
		black, red = 0, 0
		for i in range(board.rows):
			for j in range(board.cols):
				if board.field[i][j] == 1:
					black += 1
				elif board.field[i][j] == 2:
					red += 1
		return black, red


	def main_loop(self):
		while self.game_running:
			if not self.find_legal_moves(board):
				self.missed_turns += 1
				self.black_turn = not(self.black_turn)
				if self.game_ended(board):
					self.game_running = False
					break
				else: continue

			if self.turn_token() in self.human_players:
				self.human_turn = True
			else:
				self.human_turn = False
			if not self.human_turn:
				pygame.time.delay(self.ai_delay)
				if self.black_turn:
					move = self.black_player(board.field, self.find_legal_moves(board),
										6, True, self.turn_token(), -inf, inf)
				else:
					move = self.red_player(board.field, self.find_legal_moves(board),
										6, True, self.turn_token(), -inf, inf)
				value, tile = move
				print(self.turn_token(), tile, value)
				turn_done = self.insert_token(tile, board.field)
				if turn_done:
					self.flip_tokens(board.field, tile)
					self.missed_turns = 0
					self.black_turn = not(self.black_turn)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.game_running = False
				elif event.type == pygame.MOUSEMOTION:
					self.selected_tile = window.hovered_pos(board)
					# print(self.selected_tile)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.clicked_tile = window.hovered_pos(board)
					in_board = True
					try:
						for ordinate in self.clicked_tile:
							if not(0 <= ordinate < board.rows): in_board = False
					except TypeError:
						in_board = False
					# print(in_board)
					if in_board and self.human_turn:
						# print(self.clicked_tile)
						turn_done = self.insert_token(self.clicked_tile, board.field)
						if turn_done:
							self.flip_tokens(board.field, self.clicked_tile)
							self.missed_turns = 0
							self.black_turn = not(self.black_turn)
							# self.print_legals(board)
							# print(self.find_legal_moves(board))

			self.draw()
			window.mouse_coords()
			window.show_legals(board, self)
			self.clock.tick(60)
			pygame.display.flip()
		print("done")
		black, red = self.count_tokens(board)
		print('black: ',black)
		print('red: ', red)
		f = open("black_stats.txt", "a")
		out = str(black-red) + "\n"
		f.write(out)
		f.close()

app = Reversi()
app.main_loop()
