# main
# Daniel Burns

import os

class OthelloBoard():

	def __init__(self, rowsize=8, columnsize=8):
		self.rowsize = rowsize
		self.columnsize = columnsize
		self.board = [['.' for _ in range(columnsize)] for _ in range(rowsize)]
		self.board[int((len(self.board) / 2) - 1)][int((len(self.board) / 2) - 1)] = 'X'
		self.board[int(len(self.board) / 2)][int(len(self.board) / 2)] = 'X'
		self.board[int((len(self.board) / 2) - 1)][int(len(self.board) / 2)] = 'O'
		self.board[int(len(self.board) / 2)][int((len(self.board) / 2) - 1)] = 'O'

	def printBoard(self):
		print(' ', end='')
		for i in range(len(self.board)):
			print('{:>2}'.format(i), end='')
		print('')
		for i in range(len(self.board)):
			print(i, end='')
			for j in range(len(self.board)):
				print('{:>2}'.format(self.board[i][j]), end='')
			print('')

	def isGameFinished(self):
		for i in range(len(self.board)):
			for j in range(len(self.board)):
				if self.board[i][j] == '.': return False
		return True

	def captureLeft(self, row, column):
		if ((column - 2 >= 0) and \
			(self.board[row][column - 1] != '.' and \
			self.board[row][column - 1] != self.board[row][column]) and \
			(self.board[row][column - 2] == self.board[row][column])):
			return True
		return False

	def captureRight(self, row, column):
		if ((column + 2 < self.columnsize) and \
			(self.board[row][column + 1] != '.' and \
			self.board[row][column + 1] != self.board[row][column]) and \
			(self.board[row][column + 2] == self.board[row][column])):
			return True
		return False

	def captureUp(self, row, column):
		if ((row - 2 >= 0) and \
			(self.board[row - 1][column] != '.' and \
			self.board[row - 1][column] != self.board[row][column]) and \
			(self.board[row - 2][column] == self.board[row][column])):
			return True
		return False

	def captureDown(self, row, column):
		if ((row + 2 < self.rowsize) and \
			(self.board[row + 1][column] != '.' and \
			self.board[row + 1][column] != self.board[row][column]) and \
			(self.board[row + 2][column] == self.board[row][column])):
			return True
		return False

	def captureUpLeft(self, row, column):
		if ((row - 2 >= 0) and (column - 2 >= 0) and \
			(self.board[row - 1][column - 1] != '.' and \
			self.board[row - 1][column - 1] != self.board[row][column]) and \
			(self.board[row - 2][column - 2] == self.board[row][column])):
			return True
		return False

	def captureUpRight(self, row, column):
		if ((row - 2 >= 0) and (column + 2 < self.columnsize) and \
			(self.board[row - 1][column + 1] != '.' and \
			self.board[row - 1][column + 1] != self.board[row][column]) and \
			(self.board[row - 2][column + 2] == self.board[row][column])):
			return True
		return False

	def captureDownLeft(self, row, column):
		if ((row + 2 < self.rowsize) and (column - 2 >= 0) and \
			(self.board[row + 1][column - 1] != '.' and \
			self.board[row + 1][column - 1] != self.board[row][column]) and \
			(self.board[row + 2][column - 2] == self.board[row][column])):
			return True
		return False

	def captureDownRight(self, row, column):
		if ((row + 2 < self.rowsize) and (column + 2 < self.columnsize) and \
			(self.board[row + 1][column + 1] != '.' and \
			self.board[row + 1][column + 1] != self.board[row][column]) and \
			(self.board[row + 2][column + 2] == self.board[row][column])):
			return True
		return False

class PlayerVsPlayer():

	def __init__(self):
		self.row = None
		self.column = None
		self.turn = 1
		self.gameBoard = OthelloBoard()

	def mainExecution(self):
		os.system('clear')
		self.gameBoard.printBoard()
		print('\nPlayer X goes first', end='')
		while not self.gameBoard.isGameFinished():
			if self.turn % 2: print('\nPlayer X:')
			else: print('\nPlayer O:')
			print('---------', end='\n\n')
			self.column = int(input('Enter X Coordinate: '))
			self.row = int(input('Enter Y Coordinate: '))
			if self.gameBoard.board[self.row][self.column] != '.':
				print('\nThere is already a piece there.. Please re-enter X and Y coordinates', end='\n\n')
				continue
			if not self.isConnectedToOtherPiece():
				print('\nPiece must be connected to another piece.. Please re-enter X and Y coordinates', end='\n\n')
				continue
			if self.turn % 2:
				self.gameBoard.board[self.row][self.column] = 'X'
			else:
				self.gameBoard.board[self.row][self.column] = 'O'
			self.iterateBoard()
			self.turn += 1
			os.system('clear')
			self.gameBoard.printBoard()

		xCount = 0
		oCount = 0
		for i in range(len(self.gameBoard.rowsize)):
			for j in range(len(self.gameBoard.columnsize)):
				if self.gameBoard.board[i][j] == 'X': xCount += 1
				elif self.gameBoard.board[i][j] == 'O': oCount += 1
		if xCount > oCount: print('Player X wins!')
		elif xCount < oCount: print('Player O wins!')
		else: print("It's a tie!")
		print('Thank you for playing', end='\n\n')

	def isConnectedToOtherPiece(self):
		for i in range(-1, 2):
			for j in range(-1, 2):
				if self.row + i < self.gameBoard.rowsize and self.row + i >= 0 and \
					self.column + j < self.gameBoard.columnsize and \
					self.column + j >= 0:
					if self.gameBoard.board[self.row + i][self.column + j] \
						!= '.':
						return True
		return False

	def iterateBoard(self):
		if self.gameBoard.captureLeft(self.row, self.column):
			if self.turn % 2: self.gameBoard.board[self.row][self.column - 1] = 'X'
			else: self.gameBoard.board[self.row][self.column - 1] = 'O'
		if self.gameBoard.captureRight(self.row, self.column):
			if self.turn % 2: self.gameBoard.board[self.row][self.column + 1] = 'X'
			else: self.gameBoard.board[self.row][self.column + 1] = 'O'
		if self.gameBoard.captureUp(self.row, self.column):
			if self.turn % 2: self.gameBoard.board[self.row - 1][self.column] = 'X'
			else: self.gameBoard.board[self.row - 1][self.column] = 'O'
		if self.gameBoard.captureDown(self.row, self.column):
			if self.turn % 2: self.gameBoard.board[self.row + 1][self.column] = 'X'
			else: self.gameBoard.board[self.row + 1][self.column] = 'O'
		if self.gameBoard.captureUpLeft(self.row, self.column):
			if self.turn % 2: self.gameBoard.board[self.row - 1][self.column - 1] = 'X'
			else: self.gameBoard.board[self.row - 1][self.column - 1] = 'O'
		if self.gameBoard.captureUpRight(self.row, self.column):
			if self.turn % 2: self.gameBoard.board[self.row - 1][self.column + 1] = 'X'
			else: self.gameBoard.board[self.row - 1][self.column + 1] = 'O'
		if self.gameBoard.captureDownLeft(self.row, self.column):
			if self.turn % 2: self.gameBoard.board[self.row + 1][self.column - 1] = 'X'
			else: self.gameBoard.board[self.row + 1][self.column - 1] = 'O'
		if self.gameBoard.captureDownRight(self.row, self.column):
			if self.turn % 2: self.gameBoard.board[self.row + 1][self.column + 1] = 'X'
			else: self.gameBoard.board[self.row + 1][self.column + 1] = 'O'

def main():
	playerVsPlayer = PlayerVsPlayer()
	playerVsPlayer.mainExecution()

if __name__ == '__main__':
	main()
