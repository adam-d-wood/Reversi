import pygame
from pygame.locals import *

PADDING_X = 50
PADDING_Y = 50
COL_WIDTH = 100
ROW_HEIGHT = 100

BLACK  = (  0,   0,   0)
GREY   = (109, 109, 109)
GREY2  = (184, 184, 184)
WHITE  = (255, 255, 255)
RED    = (209,   74,   78)
MUTE_RED = (225, 139, 142)
BLUE   = (  0,   0, 255)
YELLOW = (250, 240, 190)
MUTE_BLUE = (0, 100, 150)

class Window():

	def setup_display(self, board):
		self.window_width = board.cols * COL_WIDTH + 2*PADDING_X
		self.window_height = board.rows * ROW_HEIGHT + 2*PADDING_Y
		self.display = pygame.display.set_mode((self.window_width, self.window_height))
		pygame.display.set_caption("Reversi")
		pygame.font.init()
		return self.display

	def draw_board(self, display, board, game):
		display.fill(WHITE)
		top = [PADDING_X, PADDING_Y]
		for i in range(board.cols-1):
			top[0] += COL_WIDTH
			bottom = [top[0], top[1]+ROW_HEIGHT*board.rows]
			pygame.draw.line(display, BLACK, top, bottom)

		left = [PADDING_X, PADDING_Y]
		for i in range(board.rows-1):
			left[1] += ROW_HEIGHT
			right = [left[0]+COL_WIDTH*board.cols, left[1]]
			pygame.draw.line(display, BLACK, left, right)

		for i in range(board.rows):
			for j in range(board.cols):
				cell_centre = [int(PADDING_X + COL_WIDTH/2 + COL_WIDTH*j), int(PADDING_Y + COL_WIDTH/2 + COL_WIDTH*i)]
				if board.field[i][j] == 1:
					pygame.draw.circle(display, BLACK, cell_centre, int(COL_WIDTH*0.3))
				elif board.field[i][j] == 2:
					pygame.draw.circle(display, RED, cell_centre, int(COL_WIDTH*0.3))


	def hovered_pos(self, board):
		pos = pygame.mouse.get_pos()
		if pos[0] < PADDING_X or pos[0] > self.window_width - PADDING_X:
			return None
		else:
			col = (pos[0] - PADDING_X) // (COL_WIDTH)
			row = (pos[1] - PADDING_Y) // (COL_WIDTH)
			return [col, row]

	def mouse_coords(self):
		posfont = pygame.font.SysFont('Courier New', 20)
		pos = pygame.mouse.get_pos()
		# out = str(pos)[1:-2]
		out = [(n-PADDING_X)//COL_WIDTH for n in pos]
		out = str(out)
		coords = posfont.render(out, False, BLACK)
		self.display.blit(coords, pos)

	def show_legals(self, board, game):
		legals = game.find_legal_moves(board)
		for i in range(board.rows):
			for j in range(board.cols):
				cell_centre = [int(PADDING_X + COL_WIDTH/2 + COL_WIDTH*j), int(PADDING_Y + COL_WIDTH/2 + COL_WIDTH*i)]
				if [i,j] in legals and game.turn_token()==1:
					pygame.draw.circle(self.display, GREY2, cell_centre, int(COL_WIDTH*0.3))
				if [i,j] in legals and game.turn_token()==2:
					pygame.draw.circle(self.display, MUTE_RED, cell_centre, int(COL_WIDTH*0.3))
