import pygame
from pygame.locals import *

class Board():

	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.field = [[0 for i in range(cols)] for j in range(rows)]
		self.field[3][3], self.field[4][4] = 1, 1
		self.field[4][3], self.field[3][4] = 2, 2

board = Board(8, 8)
# for row in board.field:
	# print(row)


