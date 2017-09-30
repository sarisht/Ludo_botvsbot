import sys
from Tkinter import *
from threading import Thread
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--noBoard", help="Doesn't display the GUI board", action="store_true")
args = parser.parse_args()

class Board(object):
	"""Class for storing the current state of the game and moves"""
	def __init__(self, game_mode, gui_enable=False):
		self.gui_enable = gui_enable
		self.start_squares = {'G':1, 'Y':14, 'B':27, 'R':40}
		self.walk_start_squares = {'G':53, 'Y':58, 'B':63, 'R':68}
		self.safe_squares = [1,9,14,22,27,35,40,48]
		self.home_squares = {'R':[(80,80), (120,80), (80,120), (120,120)], 'G':[(440,80), (480,80), (440,120), (480,120)], 
							'B':[(80,440), (120,440), (80,480), (120,480)], 'Y':[(440,440), (480,440), (440,480),(480,480)]}
		if game_mode==0:
			self.colours = ['R','Y']
			self.local_positions = {'R':[-1,-1,-1,-1], 'Y':[-1,-1,-1,-1]}
			self.global_positions = {'R':[-1,-1,-1,-1], 'Y':[-1,-1,-1,-1]}
		else:
			self.colours = ['B', 'G']
			self.local_positions = {'B':[-1,-1,-1,-1], 'G':[-1,-1,-1,-1]}
			self.global_positions = {'B':[-1,-1,-1,-1], 'G':[-1,-1,-1,-1]}

	def draw_counter(self, position, colour, txt, canvas):
		val = canvas.create_oval(position[0],position[1],position[0]+40,position[1]+40,fill=colour)
		canvas.create_text(position[0]+20, position[1]+20, fill="white", text=txt, font=(40))
		return val

	def intialize_board(self):
		self.tk_obj = Tk()
		self.canvas = Canvas(self.tk_obj,bg="white", width = 600, height = 600)
		self.canvas.pack()
		self.canvas.create_rectangle(0,0,240,240,fill="red")
		self.canvas.create_rectangle(360,0,600,240,fill="green")
		self.canvas.create_rectangle(0,360,240,600,fill="blue")
		self.canvas.create_rectangle(360,360,600,600,fill="yellow")
		self.canvas.create_rectangle(240,240,360,360,fill="gray")
		self.canvas.create_rectangle(80,80,160,160,fill="white")
		self.canvas.create_rectangle(440,80,520,160,fill="white")
		self.canvas.create_rectangle(80,440,160,520,fill="white")
		self.canvas.create_rectangle(440,440,520,520,fill="white")
		self.x_coord = {}
		self.y_coord = {}
		f = open('squares.txt')
		current_line = 0
		for line in f:
			line = line.strip().split('\t')
			line = [int(j) for j in line]
			for i in xrange(len(line)):
				if line[i]!=0:
					self.x_coord[line[i]] = 40*i
					self.y_coord[line[i]] = 40*current_line
			current_line+=1
		f.close()
		for i in xrange(1,73):
			if (i in self.safe_squares or i>=53):
				if (i==1 or i==48 or (i>=53 and i<=57)):
					self.canvas.create_rectangle(self.x_coord[i],self.y_coord[i],self.x_coord[i]+40,self.y_coord[i]+40,fill="green",width=2)
				elif (i==9 or i==14 or (i>=58 and i<=62)):
					self.canvas.create_rectangle(self.x_coord[i],self.y_coord[i],self.x_coord[i]+40,self.y_coord[i]+40,fill="yellow",width=2)
				elif (i==22 or i==27 or (i>=63 and i<=67)):
					self.canvas.create_rectangle(self.x_coord[i],self.y_coord[i],self.x_coord[i]+40,self.y_coord[i]+40,fill="blue",width=2)
				else:
					self.canvas.create_rectangle(self.x_coord[i],self.y_coord[i],self.x_coord[i]+40,self.y_coord[i]+40,fill="red",width=2)
			else:
				self.canvas.create_rectangle(self.x_coord[i],self.y_coord[i],self.x_coord[i]+40,self.y_coord[i]+40,fill="white",width=2)
		if self.colours[0]=='B':
			self.board_objects = {'B':[-1,-1,-1,-1], 'G':[-1,-1,-1,-1]}
			for i in xrange(4):
				self.board_objects['B'][i] = self.draw_counter(self.home_squares['B'][i], "blue", i, self.canvas)
				self.board_objects['G'][i] = self.draw_counter(self.home_squares['G'][i], "green", i, self.canvas)
		else:
			self.board_objects = {'R':[-1,-1,-1,-1], 'Y':[-1,-1,-1,-1]}
			for i in xrange(4):
				self.board_objects['R'][i] = self.draw_counter(self.home_squares['R'][i], "red", i, self.canvas)
				self.board_objects['Y'][i] = self.draw_counter(self.home_squares['Y'][i], "yellow", i, self.canvas)

	def refresh_counters(self):
		# First delete all existing counters
		for i in self.board_objects:
			for j in self.board_objects[i]:
				self.canvas.delete(j)
				self.canvas.delete(j+1)
		# Redraw all counters, keep updating board_objects
		if self.colours[0]=='B':
			for i in xrange(4):
				if self.global_positions['B'][i]==-1:
					self.board_objects['B'][i] = self.draw_counter(self.home_squares['B'][i], "blue", i, self.canvas)
				elif self.global_positions['B'][i]!=0:
					g_pos = self.global_positions['B'][i]
					self.board_objects['B'][i] = self.draw_counter((self.x_coord[g_pos],self.y_coord[g_pos]), "blue", i, self.canvas)
			for i in xrange(4):
				if self.global_positions['G'][i]==-1:
					self.board_objects['G'][i] = self.draw_counter(self.home_squares['G'][i], "green", i, self.canvas)
				elif self.global_positions['G'][i]!=0:
					g_pos = self.global_positions['G'][i]
					self.board_objects['G'][i] = self.draw_counter((self.x_coord[g_pos],self.y_coord[g_pos]), "green", i, self.canvas)
		else:
			for i in xrange(4):
				if self.global_positions['R'][i]==-1:
					self.board_objects['R'][i] = self.draw_counter(self.home_squares['R'][i], "red", i, self.canvas)
				elif self.global_positions['R'][i]!=0:
					g_pos = self.global_positions['R'][i]
					self.board_objects['R'][i] = self.draw_counter((self.x_coord[g_pos],self.y_coord[g_pos]), "red", i, self.canvas)
			for i in xrange(4):
				if self.global_positions['Y'][i]==-1:
					self.board_objects['Y'][i] = self.draw_counter(self.home_squares['Y'][i], "yellow", i, self.canvas)
				elif self.global_positions['Y'][i]!=0:
					g_pos = self.global_positions['Y'][i]
					self.board_objects['Y'][i] = self.draw_counter((self.x_coord[g_pos],self.y_coord[g_pos]), "yellow", i, self.canvas)


	def opp(self,c):
		''' Returns the other colour on the board'''
		if c not in colours: raise Exception("wrong colour input in opp function")
		if c == self.colours[0]:
			return self.colours[1]
		else:
			return self.colours[0]
	
	def local_to_global(self, i, c):
		''' Converts a local position w.r.t a colour to a global board position
		'''
		# Local position of 0 represents counter has completed the circuit
		# Local position = 0 => Global position 0 
		if (i==-1):
			return -1
		elif(i<=0):
			raise Exception("Input given to Board.local_to_global is <=0 and not = -1")
		elif (i==57):
			return 0
		elif (i>57):
			raise Exception("Input given to Board.local_to_global is > 57")			
		elif (i<52):
			return (i+self.start_squares[c]-2)%52 + 1
		else:
			return (i-52 + self.walk_start_squares[c])

	def global_to_local(self, i, c):
		''' Converts a global board position to a local board position w.r.t a colour
		'''
		# Added a check for squares not reachable by a colour. (Eg: Sq 52 cannot be reached by green)
		if ((c=='G' and i==52) or (c=='R' and i==39) or (c=='Y' and i==13) or (c=='B' and i==26)):
			raise Exception("Square "+str(i)+" cannot be reached by colour "+str(c))
		elif (i==-1):
			return -1
		elif (i==0):
			return 0
		elif (i<0):
			raise Exception("Input given to Board.global_to_local is < 0 and not = -1 or 0")
		elif (i>72):
			raise Exception("Input given to Board.global_to_local is > 72")			
		elif (i<53):
			return (i - self.start_squares[c])%52 + 1
		else:
			return (i-self.walk_start_squares[c] + 52)

	# TODO: Complete this method		I think this should handle execution except for case where multiple dices are thrown example (6,3)
	# In that case what will be the input like? one at a time followed by <\n> should handled
	def execute_move(self, player_id, move_str):
		''' Executes a move on the board
		'''
		# move will be of form R1_5-> ['R','1','_','5']
		move = list(move_str)
		colour = move[0]
		counter_no = int(move[1])
		movement = int(move[3])
		if self.local_positions[colour][counter_no] == -1: 
			if (movement == 1 | movement == 6):# Goti khul gayi varna kuch nhi chal skta/invalid move
				self.local_positions[colour][counter_no] = 1
				self.global_positions[colour][counter_no] = self.start_squares[colour]
		# TODO: What if two counters are present on the same square? Can one of them be cut?
		else:# Goti pehle se khuli thee
			self.local_positions[colour][counter_no] += movement
			current_local = self.local_positions[colour][counter_no]
			self.global_positions[colour][counter_no] = self.local_to_global(current_local, colour)
			current_global = self.global_positions[colour][counter_no]
			if current_global not in self.safe_squares: 
				if current_global in self.global_positions[self.opp(colour)]:# Goti kat gayi
						opp_colour = self.opp(colour)
						i = self.global_positions[opp_colour].index(current_global)
						self.global_positions[opp_colour][i] = -1
						self.local_positions[opp_colour][i] = -1
		if (self.gui_enable):
			self.refresh_counters()

	# TODO: Complete this method to double check we don't make a mistake
	def is_valid_move(self, move, player_id):
		'''Returns True is a given move is valid, False otherwise
		'''
	# TODO: Complete this method
	def get_best_move(self, player_id, dice):
		''' Returns the best possible move
		'''
		# order -> cutting(aggressive bot), defending(if any opponent near(within 12 steps)), 
		#escaping(if meri aadhi badi hui goti(>24) ko bhaga saku danger ke bahar even if it is safe initially), 
		#pursuing(agar mere aage doosre ki goti h toh follow it but not cross), 
		# opening, frowardmost (if no danger), safing, least in danger

start_string = sys.stdin.readline().strip().split(' ')
start_string = [int(i) for i in start_string]

player_id = start_string[0] - 1 # Get player id to be 0 or 1
time_limit = start_string[1]
game_mode = start_string[2]

if args.noBoard:
	board = Board(game_mode, False)
else:
	board = Board(game_mode, True)


def play_game(board):
	# Wait for first move from the other player (only if player_id is 1 i.e.(You are player 2))
	if player_id==1:
		dice = sys.stdin.readline().strip()
		move = sys.stdin.readline().strip()
		board.execute_move(0, move)

	while(True):
		sys.stdout.write('<THROW>\n')
		sys.stdout.flush()
		dice = sys.stdin.readline().strip()
		best_move = board.get_best_move(player_id, dice)
		# TODO: Find the best move for player_id, dice
		# and update this move on the board (Add the get_best_move method)
		sys.stdout.write(best_move)
		sys.stdout.flush()
		board.execute_move(player_id, best_move)
		# TODO: Check winning condition
		# Wait for opponents move
		dice = sys.stdin.readline().strip()
		if (dice=='REPEAT'):
			continue
		move = sys.stdin.readline().strip()
		temp_move = move.split('<next>')
		if temp_move[-1]=='REPEAT':
			board.execute_move(1-player_id, move)
			dice = sys.stdin.readline().strip()
			move = sys.stdin.readline().strip()
			board.execute_move(1-player_id, move)
		else:
			board.execute_move(1-player_id, move)			

if (args.noBoard):
	play_game(board)

else:
	Th = Thread(target = lambda : play_game(board))
	Th.start()
	board.intialize_board()
	board.tk_obj.mainloop()

