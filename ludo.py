import sys
from Tkinter import *
from threading import Thread
import argparse
import copy

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
		# TODO: Handle  moves with multiple counters and REPEAT at the end, eg: R0_5<next>R1_3<REPEAT>
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
		if dice.length == 1: # i.e. no 6
			roll = dice[0]
			player_col = self.colour[player_id]
			ini = self.local_positions[player_col]#initial positions
			ini_glob = self.global_positions[player_col]
			opp = self.global_positions[self.opp(player_col)]# opponent position
			# checking for cutting
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c > 52 : continue # home lane
				poss_c = local_to_global(ini[ctr_num]+roll,player_col)	
				if poss_c in self.safe_squares: continue # person on safe sqaure
				if ini_c == 0:continue # completed
				if ini_c ==-1 : continue # unopened
				if poss_c in opp: 
					str1 = player_col + str(ctr_num) + '_' + str(roll) #cutting....Scope: Case-Multiple cuttings..........
					self.execute_move(player_id,str1)#execution of cutting					
					return str1
			# if my counter is ahead within 6 distance of opposition
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c > 52 : continue # home lane
				poss_c = local_to_global(ini[ctr_num]+roll,player_col)	
				if ini_c in self.safe_squares: continue # I am not in danger
				if ini_c == 0:continue # completed
				if ini_c ==-1 : continue # unopened
				for opp_c in opp: 
					if opp_c == -1: continue # opponent unopened
					if opp_c >52:continue # opponent on home lane
					if opp_c == 0: continue # opponent counter completed
					if (ini_c - opp_c)%52 <= 6:#Scope: If multiple counters are under threat......................
						boolean = True
						for opp_c2 in opp:# Scope: If a counter under threat from multiple opposition counters..........
							if opp_c2 == -1: continue # opponent unopened
							if opp_c2 >52:continue # opponent on home lane
							if opp_c2 == 0: continue # opponent counter completed
							if poss_c - opp_c2 <=6: # No increase in safety even if I move
								boolean = False
								break
						if boolean:
							str1 = player_col + str(ctr_num) + '_' + str(roll)
							self.execute_move(player_id,str1)
							return str1
			# open with 1
			if roll == 1:
				for ctr_num in range(4):
					if ini_glob[ctr_num]==-1:
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						self.execute_move(player_id,str1)
						return str1
			# if my predicted counter is behind within 6 distance of opposition
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c > 52 : continue # home lane
				poss_c = local_to_global(ini[ctr_num]+roll,player_col)
				if ini_c == 0:continue # completed
				if ini_c ==-1 : continue # unopened
				for opp_c in opp: # doesnt matter if opponent is sitting on safe square, he has to move at some point
					# Scope: Check if this move decreases my own safety..........
					if opp_c == -1: continue # opponent unopened
					if opp_c >52:continue # opponent on home lane
					if opp_c == 0: continue # opponent counter completed
					if (opp_c - poss_c)%52 <= 6:
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						self.execute_move(player_id,str1)
						return str1
			# homing for extra move
			for ctr_num in range(4):
				try: # if local_to_global gets input > 57 then exception case
					ini_l_c = ini[ctr_num]
					poss_c = local_to_global(ini_l_c+roll,player_col)
					if poss_c == 0: 
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						self.execute_move(player_id,str1)
						return str1
				except:
					pass
			# if my counter is ahead within 12 distance of opposition(no immediate danger but danger still)(only for local counters greater than 27)
			for ctr_num in range(4):
				if ini[ctr_num] <= 27: continue
				ini_c = ini_glob[ctr_num]
				if ini_c > 52 : continue # home lane
				poss_c = local_to_global(ini[ctr_num]+roll,player_col)
				if poss_c in self.safe_square: # If I reach a safe square
					str1 = player_col + str(ctr_num) + '_' + str(roll)
					self.execute_move(player_id,str1)
					return str1
				if ini_c == 0: continue # completed
				if ini_c ==-1: continue # unopened
				for opp_c in opp: 
					if opp_c == -1: continue     # opponent unopened
					if opp_c >  52: continue     # opponent on home lane
					if opp_c ==  0: continue     # opponent counter completed
					if (ini_c - opp_c)%52 <= 12: # Scope: If multiple counters are under threat......................
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						self.execute_move(player_id,str1)
						return str1
			# opening with 6
			if roll == 6:
				for ctr_num in range(4):
					if ini_glob[ctr_num]==-1:
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						self.execute_move(player_id,str1)
						return str1
			# safing
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c > 52 : continue # home lane
				poss_c = local_to_global(ini[ctr_num]+roll,player_col)
				if poss_c in self.safe_square: # If I reach a safe square
					str1 = player_col + str(ctr_num) + '_' + str(roll)
					self.execute_move(player_id,str1)
					return str1
			# moving inside home lane
			for ctr_num in range(4):
				try:
					ini_c = ini_glob[ctr_num]
					poss_c = local_to_global(ini[ctr_num]+roll,player_col)
					if poss_c >= 52: # If I reach a home lane
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						self.execute_move(player_id,str1)
						return str1
				except:
					pass
			# forwardmost without endangering that
			def sort(l1,b):
				return copy.copy(l1).sort(reverse=b)
			for c in sort(ini,True):
				ctr_num = ini.index(c)
				try:
					ini_c = ini_glob[ctr_num]
					poss_c = local_to_global(ini[ctr_num]+roll,player_col)
					if poss_c in self.safe_square: # If I reach a safe square
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						self.execute_move(player_id,str1)
						return str1
				except:
					pass
		# order -> cutting(aggressive bot): done, defending(if any opponent near(within 6 steps)): done, 
		# escaping(if meri aadhi badi hui goti(>25) ko bhaga saku danger ke bahar(>6 ditance) even if it is safe initially): will be case when len(dice)>1, 
		# opening with 1:done, pursuing (agar mere aage doosre ki goti h toh follow it but not cross)(if I reach within 6 steps) : done, 
		# homing:done, not completely out of danger aage vaali goti ko bhagao:done, opening with 6: done, 
		# safing:done, move inside home lane:done, forwardmost (if no danger)

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

