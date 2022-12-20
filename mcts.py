#!/usr/bin/env python

import numpy as np
import random
import math
import copy
import time

dx = [1, 1, 1, 0]
dy = [1, 0, -1, 1]

class Board(object):
	
	def __init__(self, board , last_move = [ None , None ] ):
		self.board = board 
		self.last_move = last_move

	def tryMove(self, move):
		# Takes the current board and a possible move specified 
		# by the column. Returns the appropiate row where the 
		# piece and be located. If it's not found it returns -1.

		if move < 0 or move > 7 or self.board[0][move] != 0:
			return -1

		for i in range(len(self.board)):
			if self.board[i][move] != 0:
				return i-1
		return len(self.board)-1

	def terminal(self):
	   # Returns true when the game is finished, otherwise false.
		for i in range(len(self.board[0])):
			if self.board[0][i] == 0:
				return False
		return True

	def legal_moves(self):
		# Returns the full list of legal moves that for next player.
		legal = []
		for i in range(len(self.board[0])):
			if self.board[0][i] == 0:
				legal.append(i)

		return legal

	def next_state(self, turn):
		# Retuns next state
		aux = copy.deepcopy(self)
		moves = aux.legal_moves()
		if len(moves) > 0:
			ind = random.randint(0,len(moves)-1)
			row = aux.tryMove(moves[ind])
			aux.board[row][moves[ind]] = turn
			aux.last_move = [ row, moves[ind] ]
		return aux 

	def winner(self):
		# Takes the board as input and determines if there is a winner.
		# If the game has a winner, it returns the player number (Computer = 1, Human = -1).
		# If the game is still ongoing, it returns zero.  

		x = self.last_move[0]
		y = self.last_move[1]

		if x == None:
			return 0 

		for d in range(4):

			h_counter = 0
			c_counter = 0

			for k in range(-3,4):

				u = x + k * dx[d]
				v = y + k * dy[d]

				if u < 0 or u >= 6:
					continue

				if v < 0 or v >= 7:
					continue

				if self.board[u][v] == -1:
					c_counter = 0
					h_counter += 1
				elif self.board[u][v] == 1:
					h_counter = 0
					c_counter += 1
				else:
					h_counter = 0
					c_counter = 0

				if h_counter == 4:
					return -1 

				if c_counter == 4:	
					return 1

		return 0

class Node():
	def __init__(self, state, parent = None):
		self.visits = 1 
		self.reward = 0.0
		self.state = state
		self.children = []
		self.children_move = []
		self.parent = parent 

	def addChild(self ,child_state ,move):
		child = Node(child_state,self)
		self.children.append(child)
		self.children_move.append(move)

	def update(self, reward):
		self.reward += reward 
		self.visits += 1

	def fully_explored(self):
		if len(self.children) == len(self.state.legal_moves()):
			return True
		return False

def MCTS(root):
	maxIter = 3000
	factor = 2.0

	for inter in range(maxIter):
		front, turn = treePolicy( root , 1 , factor )
		reward = defaultPolicy(front.state, turn)
		backup(front,reward,turn)

	ans = bestChild(root, 0)
	score = ans.reward / ans.visits

	# print(score, [(c.reward/c.visits) for c in ans.parent.children ])

	return ans, score


def treePolicy(node, turn, factor):
	while node.state.terminal() == False and node.state.winner() == 0:
		if node.fully_explored() == False:
			return expand(node, turn), -turn
		else:
			node = bestChild(node, factor)
			turn *= -1
	return node, turn

def expand(node, turn):
	tried_children_move = [m for m in node.children_move]
	possible_moves = node.state.legal_moves()

	for move in possible_moves:
		if move not in tried_children_move:
			row = node.state.tryMove(move)
			new_state = copy.deepcopy(node.state)
			new_state.board[row][move] = turn 
			new_state.last_move = [row, move]
			break

	node.addChild(new_state,move)
	return node.children[-1]

def bestChild(node, factor):
	bestscore = -10000000.0
	bestChildren = []
	for c in node.children:
		exploit = c.reward / c.visits
		explore = math.sqrt(math.log(2.0*node.visits)/float(c.visits))
		score = exploit + factor*explore
		if score == bestscore:
			bestChildren.append(c)
		if score > bestscore:
			bestChildren = [c]
			bestscore = score 
	return random.choice(bestChildren)

def defaultPolicy(state, turn):
	while state.terminal() == False and state.winner() == 0 :
		state = state.next_state(turn)
		turn *= -1
	return  state.winner() 

def backup(node, reward, turn):
	while node != None:
		node.visits += 1 
		node.reward -= turn*reward
		node = node.parent
		turn *= -1
	return

def transform_board(board):
	# flip the whole board
	# this will flip the rows as well (but we do not want it)
	b=np.flip(board.copy())

	# so flip the rows back
	for row in range(len(b)):
		b[row] = np.flip(b[row])

		# and transform (1,2) -> (-1, 1) since MCTS algorithm
		# uses -1 to denote user action and 1 for AI action. 
		for col in range(len(b[row])):
			if b[row][col] == 1:
				b[row][col] = -1
			elif b[row][col] == 2:
				b[row][col] = 1

	return b

# Entry point to the MCTS algorithm
def run(board):
	# MCTS algorithm uses the board flipped so do a transformation here
	b = transform_board(board)
	
	# create a tree node based on the current board 
	o = Node(Board(b))

	# feed it to the MCTS algorithm to find the best move possible
	bestMove, score = MCTS(o)

	# print(bestMove.state.last_move, score)

	# we are only interested in the column of the move and the score
	return bestMove.state.last_move[1], score