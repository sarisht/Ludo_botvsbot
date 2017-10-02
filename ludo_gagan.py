import sys
from Tkinter import *
from threading import Thread
import copy
import time
import pickle

class Board(object):
	"""Class for storing the current state of the game and moves"""
	def __init__(self, game_mode, player_id, gui_enable):
		self.gui_enable = gui_enable
		self.game_mode = game_mode
		self.player_id = player_id
		self.start_squares = {'G':1, 'Y':14, 'B':27, 'R':40}
		self.walk_start_squares = {'G':53, 'Y':58, 'B':63, 'R':68}
		self.safe_squares = [1,9,14,22,27,35,40,48]
		self.home_squares = {'R':[(80,80), (120,80), (80,120), (120,120)], 'G':[(440,80), (480,80), (440,120), (480,120)], 
							'B':[(80,440), (120,440), (80,480), (120,480)], 'Y':[(440,440), (480,440), (440,480),(480,480)]}
		self.feats = ['home','open','home_lane','star','square_num','square_cross']
		self.new_feature = {i:0 for i in self.feats}
		self.old_feature = {i:0 for i in self.feats}
		self.old_score = 0.0
		with open('weights.pickle', 'rb') as w_file:
			self.weights = pickle.load(w_file)
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
	def dump_weights(self):
		with open('weights.pickle','wb') as w_file:
			pickle.dump(self.weights, w_file)
	
	def draw_squares(self):
		self.canvas.create_rectangle(0,0,240,240,fill="red")
		self.canvas.create_rectangle(360,0,600,240,fill="green")
		self.canvas.create_rectangle(0,360,240,600,fill="blue")
		self.canvas.create_rectangle(360,360,600,600,fill="yellow")
		self.canvas.create_rectangle(240,240,360,360,fill="gray")
		self.canvas.create_rectangle(80,80,160,160,fill="white")
		self.canvas.create_rectangle(440,80,520,160,fill="white")
		self.canvas.create_rectangle(80,440,160,520,fill="white")
		self.canvas.create_rectangle(440,440,520,520,fill="white")
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
		self.draw_counters()
		# if self.colours[0]=='B':
		# 	for i in xrange(4):
		# 		self.draw_counter(self.home_squares['B'][i], "blue", i, self.canvas)
		# 		self.draw_counter(self.home_squares['G'][i], "green", i, self.canvas)
		# else:
		# 	for i in xrange(4):
		# 		self.draw_counter(self.home_squares['R'][i], "red", i, self.canvas)
		# 		self.draw_counter(self.home_squares['Y'][i], "yellow", i, self.canvas)
	def copy_board(self):
		c_board = Board(self.game_mode, self.player_id, False)
		c_board.colours = copy.deepcopy(self.colours)
		c_board.local_positions = copy.deepcopy(self.local_positions)
		# {i:self.local_positions[i] for  i in self.local_positions}
		c_board.global_positions = copy.deepcopy(self.global_positions)
		# {i:self.global_positions[i] for i in self.global_positions}
		return c_board
	
	def draw_counters(self):
		# Redraw all counters, keep updating board_objects
		if self.colours[0]=='B':
			for i in xrange(4):
				if self.global_positions['B'][i]==-1:
					self.draw_counter(self.home_squares['B'][i], "blue", i, self.canvas)
				elif self.global_positions['B'][i]!=0:
					g_pos = self.global_positions['B'][i]
					self.draw_counter((self.x_coord[g_pos],self.y_coord[g_pos]), "blue", i, self.canvas)
			for i in xrange(4):
				if self.global_positions['G'][i]==-1:
					self.draw_counter(self.home_squares['G'][i], "green", i, self.canvas)
				elif self.global_positions['G'][i]!=0:
					g_pos = self.global_positions['G'][i]
					self.draw_counter((self.x_coord[g_pos],self.y_coord[g_pos]), "green", i, self.canvas)
		else:
			for i in xrange(4):
				if self.global_positions['R'][i]==-1:
					self.draw_counter(self.home_squares['R'][i], "red", i, self.canvas)
				elif self.global_positions['R'][i]!=0:
					g_pos = self.global_positions['R'][i]
					self.draw_counter((self.x_coord[g_pos],self.y_coord[g_pos]), "red", i, self.canvas)
			for i in xrange(4):
				if self.global_positions['Y'][i]==-1:
					self.draw_counter(self.home_squares['Y'][i], "yellow", i, self.canvas)
				elif self.global_positions['Y'][i]!=0:
					g_pos = self.global_positions['Y'][i]
					self.draw_counter((self.x_coord[g_pos],self.y_coord[g_pos]), "yellow", i, self.canvas)

	def refresh_counters(self):
		# First delete all existing counters
		self.canvas.delete("all")
		sys.stderr.write("Deleted everything\n")
		self.draw_squares()
		self.draw_counters()

	def opp(self,c):
		''' Returns the other colour on the board'''
		if c not in self.colours: raise Exception("wrong colour input in opp function")
		elif c == self.colours[0]:
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
	def execute_move(self, player_id, move_str1):
		''' Executes a move on the board
		'''
		# move will be of form R1_5-> ['R','1','_','5']
		sys.stderr.write("execute_move\n")
		sys.stderr.write("initial config: "+ str(self.global_positions) +"\n")
		sys.stderr.write("move: "+ move_str1+"\n")
		if (move_str1=='NA'):
			return
		moves = move_str1.split('<next>')
		for move_str in moves:
			sys.stderr.write("initial config: "+ move_str +"\n")
			if move_str=='REPEAT':
				sys.stderr.write("execute_move_repeat\n")				
				continue
			move = list(move_str)
			colour = move[0]
			counter_no = int(move[1])
			movement = int(move[3])
			if self.local_positions[colour][counter_no] == -1: 
				if (movement == 1 or movement == 6):# Goti khul gayi varna kuch nhi chal skta/invalid move
					self.local_positions[colour][counter_no] = 1
					sys.stderr.write("execute_move : opened " +str(counter_no)+"\n")
					self.global_positions[colour][counter_no] = self.start_squares[colour]
			else:# Goti pehle se khuli thee
				self.local_positions[colour][counter_no] += movement
				current_local = self.local_positions[colour][counter_no]
				sys.stderr.write("execute_move" + str(counter_no)+"\n")
				self.global_positions[colour][counter_no] = self.local_to_global(current_local, colour)
				current_global = self.global_positions[colour][counter_no]
				if current_global not in self.safe_squares: 
					if current_global in self.global_positions[self.opp(colour)] and current_global !=0:# Goti kat gayi
							opp_colour = self.opp(colour)
							i = self.global_positions[opp_colour].index(current_global)
							self.global_positions[opp_colour][i] = -1
							self.local_positions[opp_colour][i] = -1
		
		sys.stderr.write("final config: "+ str(self.global_positions) +"\n")
		if (self.gui_enable):
			sys.stderr.write("Rendering the board again\n")
			self.refresh_counters()

	# TODO: Complete this method to double check we don't make a mistake
	def is_valid_move(self, move, player_id):
		'''Returns True is a given move is valid, False otherwise
		'''
	def filter_moves(self,moves):
		max_length = 0
		for i in moves:
			if (i=='NA'):
				continue
			t = i.split('<next>')
			if (len(t)>max_length):
				max_length = len(t)
		if max_length==0:
			return ['NA']
		else:
			filtered = []
			for i in moves:
				t = i.split('<next>')
				if len(t)==max_length and i!='NA':
					filtered.append(i)
			return filtered


	def gagan_get_best_move(self, player_id, dice):
		# Case when dice rolls 6,6,6 return NA
		if dice==[0]:
			return 'NA'
		self.update_weights(0)
		all_moves = self.get_all_moves(player_id, dice)
		filtered = self.filter_moves(all_moves)
		best_score = -100000000000
		best_move = 'NA'
		sys.stderr.write("List of moves is: "+str(filtered)+"\n")
		if filtered==['NA']:
			sys.stderr.write("No move found\n")
			return 'NA'
		else:
			for i in filtered:
				sys.stderr.write("Move "+i+" Check1")
				temp = self.copy_board()
				sys.stderr.write("Move "+i+" Check2")
				temp.execute_move(player_id,i)
				sys.stderr.write("Move "+i+" Check3")
				temp_score = temp.p_score(self.player_id)
				sys.stderr.write("Move "+i+" Check4")
				sys.stderr.write("Trying move: "+i+"\n")
				sys.stderr.write("Score is: "+str(filtered)+"\n")
				if temp_score>best_score:
					best_move = i
					best_score = temp_score
			sys.stderr.write("Move "+i+" Check5")
			return best_move


	def is_behind(self, square_num, player_id):
		sys.stderr.write("is_behind start\n")
		col = self.colours[1-player_id]
		global_p = self.global_positions[col]
		r_end = (square_num - 2)%52 +1
		r_start = (square_num - 8)%52+ 1
		i = r_start
		sys.stderr.write("value of square_num is: "+str(square_num)+"\n")
		sys.stderr.write("value of r_start is: "+str(r_start)+"\n")
		sys.stderr.write("value of r_end is: "+str(r_end)+"\n")
		it = 0
		while(i!=square_num):
			#sys.stderr.write("value of i is: "+str(i)+"\n")
			if i in global_p:
				return 0
			i = i%52 +1
		sys.stderr.write("is_behind end\n")
		return 1

	def feature_score(self, player_id):
		sys.stderr.write("Starting feature-score\n")
		col = self.colours[player_id]
		# A piece can have a max score of 100, when it is in home
		score = 0
		global_p = self.global_positions[col]
		local_p = self.local_positions[col]
		new_f = {}
		#to_store = (player_id==self.player_id)
		# No of pieces in home
		h = global_p.count(0)
		new_f['home'] = h
		score += self.weights['home']*h
		sys.stderr.write("Feature Score Check 1\n")
		# No of pieces open
		op = 4 - global_p.count(0) - global_p.count(-1)
		new_f['open'] = op
		score += self.weights['open']*op
		sys.stderr.write("Feature Score Check 2\n")
		# No of pieces in home lane
		home_piece = [i for i in local_p if (i>=52 and i<57)]
		hp = len(home_piece)
		new_f['home_lane'] = hp
		score+=self.weights['home_lane']*hp
		sys.stderr.write("Feature Score Check 3\n")
		# No of pieces on safe squares
		safe_pieces = [i for i in global_p if (i in self.safe_squares and i!=0)]
		sp = len(safe_pieces)
		new_f['star'] = sp
		score += self.weights['star']*sp
		sys.stderr.write("Feature Score Check 4\n")
		# Position of squares
		sn = 0
		sc = 0
		for i in xrange(4):
			sys.stderr.write("Feature Score Check 4.5."+str(i)+"\n")
			if local_p[i]!=-1 and global_p[i]!=0 and global_p[i]<53:
				sn += local_p[i]
				sc += self.is_behind(global_p[i], player_id)*local_p[i]
		sys.stderr.write("Feature Score Check 5\n")
		score += self.weights['square_num']*sn
		score += self.weights['square_cross']*sc
		new_f['square_num'] = sn
		new_f['square_cross'] = sc
		sys.stderr.write("Feature Score Check 6\n")
		return score,new_f


	def player_score(self, player_id):
		(x,y) = self.feature_score(player_id)
		(z,w) = self.feature_score(1-player_id)
		for i in y:
			self.new_feature[i] = y[i] - w[i]
		return x-z

	def p_score(self, player_id):
		(x,y) = self.feature_score(player_id)
		(z,w) = self.feature_score(1-player_id)
		return x - z

	def update_weights(self,reward=0):
		updated_score = self.player_score(self.player_id)
		for i in self.feats:
			self.weights[i] = self.weights[i] + 0.001*(reward+0.99*updated_score-self.old_score)*self.old_feature[i]
			if (i=='home'):
				if self.weights[i]<-250:
					self.weights[i] = 250
				if self.weights[i]>250:
					self.weights[i]=250
			else:
				if self.weights[i]<-50:
					self.weights[i]= -50
				if self.weights[i]>50:
					self.weights[i]=50
			self.old_feature[i] = self.new_feature[i]
		updated_score = self.player_score(self.player_id)
		self.old_score = updated_score
		self.dump_weights()

	def is_game_over(self):
		# Check if player 1 wins:
		c1 = self.colours[0]
		c2 = self.colours[1]
		global_positions1 = self.global_positions[c1]
		global_positions2 = self.global_positions[c2]
		if (global_positions1.count(0)==4 or global_positions2.count(0)==4):
			return True
		else:
			return False

	def can_opp_win(self, dice):
		pid = self.player_id
		pid = 1 - pid
		local_positions1 = self.local_positions[self.colours[pid]]
		sys.stderr.write('Calling can opp win\n'+str(local_positions1)+'\nDice moves: '+str(dice)+'\n')
		if len(dice)>=3:
			dice = dice[1:]
		if (len(dice)==1):
			if (local_positions1.count(57)==3):
				val = [i for i in local_positions1 if i!=57][0]
				if val+dice[0]==57:
					sys.stderr.write('***Can win****\n')
					return True
			return False
		if (len(dice)==2):
			if (local_positions1.count(57)==3):
				val = [i for i in local_positions1 if i!=57][0]
				if (val+dice[0]==57 or val+dice[1]==57):
					sys.stderr.write('***Can win****\n')
					return True
			elif (local_positions1.count(57)==2):
				val = [i for i in local_positions1 if i!=57]
				if ((val[0]+dice[0]==57 and val[1]+dice[1]==57) or (val[1]+dice[0]==57 and val[0]+dice[1]==57)):
					sys.stderr.write('***Can win****\n')
					return True
			return False

	def get_all_moves(self, player_id, dice, execute=False):
		''' Returns the best possible move
		'''
		moves_list = []
		if dice == [0]: 
			sys.stderr.write("dice rolled is 6 6 6\n")
			moves_list.append('NA')# if dice rolled is 666
			
		if len(dice)== 1: # i.e. single throw (in base form no 6)
			roll = dice[0]
			sys.stderr.write("dice: "+ str(roll)+"\n")
			player_col = self.colours[player_id]
			ini = self.local_positions[player_col]#initial positions
			ini_glob = self.global_positions[player_col]
			opp = self.global_positions[self.opp(player_col)]# opponent position
			# checking for cutting
			sys.stderr.write("Trying to cut"+"\n")
			for ctr_num in range(4):
				try:
					ini_c = ini_glob[ctr_num]
					if ini_c > 52 : continue # home lane
					if ini_c == 0:continue # completed
					if ini_c ==-1 : continue # unopened
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)	
					if poss_c in self.safe_squares: continue # person on safe sqaure
					if poss_c in opp: 
						str1 = player_col + str(ctr_num) + '_' + str(roll) #cutting....Scope: Case-Multiple cuttings..........
						if execute: self.execute_move(player_id,str1)#execution of cutting					
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0:
							moves_list.append(str1)
				except: 
					sys.stderr.write("Not possible: "+ str(ini_c) + " roll"+ str(roll)+"\n")
					continue
			# if my counter is ahead within 6 distance of opposition

			sys.stderr.write("Trying to defend (within 6)"+"\n")
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c > 52 : continue # home lane
				if ini_c == 0:continue # completed
				if ini_c ==-1 : continue # unopened
				try:
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)	
					if ini_c in self.safe_squares: continue # I am not in danger
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
							if poss_c in self.safe_squares: boolean = True # If I can reach safe square then good enough
							if boolean:
								str1 = player_col + str(ctr_num) + '_' + str(roll)
								if execute: self.execute_move(player_id,str1)
								if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0:
									moves_list.append(str1)
				except: continue
			# escaping with large number
			sys.stderr.write("Trying to escape"+"\n")
			if roll>6:
				for ctr_num in range(4):
					ini_c = ini_glob[ctr_num]
					if ini_c > 52 : continue # home lane
					if ini_c == 0 : continue # completed
					if ini_c ==-1 : continue # unopened
					try:
						poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
						if global_to_local(poss_c,player_id) > 27:
							boolean = True
							for opp_c in opp: 
								if opp_c == -1: continue # opponent unopened
								if opp_c >52:continue # opponent on home lane
								if opp_c == 0: continue # opponent counter completed
								if (poss_c - opp_c)%52<=6:
									boolean = False
									break
							if boolean:
								str1 = player_col + str(ctr_num) + '_' + str(roll)
								if execute: self.execute_move(player_id,str1)
								if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0:
									moves_list.append(str1)
					except: continue
			# open with 1
			sys.stderr.write("Trying to open with 1"+"\n")
			if roll == 1:
				for ctr_num in range(4):
					if ini_glob[ctr_num]==-1:
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						moves_list.append(str1)
			# if my predicted counter is behind within 6 distance of opposition
			sys.stderr.write("Trying to follow"+"\n")
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c > 52 : continue # home lane
				if ini_c == 0:continue # completed
				if ini_c ==-1 : continue # unopened
				try:
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
					for opp_c in opp: # doesnt matter if opponent is sitting on safe square, he has to move at some point
						# Scope: Check if this move decreases my own safety..........
						if opp_c == -1: continue # opponent unopened
						if opp_c >52:continue # opponent on home lane
						if opp_c == 0: continue # opponent counter completed
						if (opp_c - poss_c)%52 <= 6:
							str1 = player_col + str(ctr_num) + '_' + str(roll)
							if execute: self.execute_move(player_id,str1)
							if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0:
								moves_list.append(str1)
				except: continue
			# homing for extra move
			sys.stderr.write("Trying to get into final state"+"\n")
			for ctr_num in range(4):
				try: # if local_to_global gets input > 57 then exception case
					ini_l_c = ini[ctr_num]
					poss_c = self.local_to_global(ini_l_c+roll,player_col)
					if poss_c==0: 
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						moves_list.append(str1)
				except:
					continue
			# if my counter is ahead within 12 distance of opposition(no immediate danger but danger still)(only for local counters greater than 27)
			for ctr_num in range(4):
				if ini[ctr_num] <= 27: continue
				ini_c = ini_glob[ctr_num]
				if ini_c > 52: continue # home lane
				if ini_c == 0: continue # completed
				if ini_c ==-1: continue # unopened
				try: 
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
					if poss_c in self.safe_squares: # If I reach a safe square
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0:
							moves_list.append(str1)
					for opp_c in opp: 
						if opp_c == -1: continue     # opponent unopened
						if opp_c >  52: continue     # opponent on home lane
						if opp_c ==  0: continue     # opponent counter completed
						if (ini_c - opp_c)%52 <= 12: # Scope: If multiple counters are under threat......................
							str1 = player_col + str(ctr_num) + '_' + str(roll)
							if execute: self.execute_move(player_id,str1)
							if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : moves_list.append(str1)
				except:continue
			# opening with 6
			if roll == 6:
				for ctr_num in range(4):
					if ini_glob[ctr_num]==-1:
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : moves_list.append(str1)
			# safing
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c == -1: continue
				if ini_c == 0: continue				
				if ini_c > 52 : continue # home lane
				try:
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
					if poss_c in self.safe_squares: # If I reach a safe square
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : moves_list.append(str1)
				except:
					continue
			# forwardmost without endangering that
			def sort(l1,b):
				k = copy.copy(l1)
				k.sort(reverse=b)
				return k # copy.copy used as I dont want l1 to get changed, b is for descending
 			for c in sort(ini,True):
				ctr_num = ini.index(c)
				if c == 0: break
				if c == -1: break
				try:
					ini_c = ini_glob[ctr_num]
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
					if poss_c in self.safe_squares:
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0  or poss_c>52: moves_list.append(str1)
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
							if execute: self.execute_move(player_id,str1)
							if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0  or poss_c>52: moves_list.append(str1)
				except:
					continue
			# if all go in danger
			for c in sort(ini, False):
				ctr_num = ini.index(c)
				if c == 0: continue
				if c == -1: continue
				try:
					ini_c = ini_glob[ctr_num]
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)	
					str1 = player_col + str(ctr_num) + '_' + str(roll)
					if execute: self.execute_move(player_id,str1)
					if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : moves_list.append(str1)
				except:
					continue
			# if I cant move anything
			moves_list.append('NA')
		elif len(dice) == 2:# dice will be of the form [6,x]
			roll = dice[1]
			a,b = self.get_best_move(player_id, [roll])
			c,d = self.get_best_move(player_id, [6])
			e,f = self.get_best_move(player_id, [6+roll])
			temp = self.copy_board()
			if b<=d and b<=f:
				# temp = copy.deepcopy(self)
				temp.execute_move(player_id,a)
				g, h = temp.get_best_move(player_id,[6])
				str_1 = a +'<next>' +g
				if g == 'NA': str_1 = a
				moves_list.append(str_1)
			elif d<=b and d<=f:
				# temp = copy.deepcopy(self)
				temp.execute_move(player_id,c)
				g, h = temp.get_best_move(player_id,[roll])
				str_1 = c +'<next>' + g
				if g == 'NA': str_1 = c
				moves_list.append(str_1)
			else:# f<=b and f<=d
				move = e[:3]
				str_1 = move + '6' + '<next>' + move +str(roll)
				moves_list.append(str_1)
		else:#double 6
			roll = dice[2]
			a,b = self.get_best_move(player_id, [roll])
			c,d = self.get_best_move(player_id, [6])
			e,f = self.get_best_move(player_id, [6+roll])
			g,h = self.get_best_move(player_id, [12])
			i,j = self.get_best_move(player_id, [12+roll])
			temp = self.copy_board()
			if b == min([b,d,f,h,j]):
				# temp = copy.deepcopy(self)
				temp.execute_move(player_id,a)
				k, l = temp.get_best_move(player_id,[6,6])
				str_1 = a +'<next>' +k
				if k == 'NA' : str_1 = a
				moves_list.append(str_1)
			elif d == min([b,d,f,h,j]):
				# temp = copy.deepcopy(self)
				temp.execute_move(player_id,c)
				k, l = temp.get_best_move(player_id,[6,roll])
				str_1 = c +'<next>' + k
				if k == 'NA' : str_1 = c
				moves_list.append(str_1)
			elif f == min([b,d,f,h,j]):
				# temp = copy.deepcopy(self)
				move = e[:3]
				str_2 = move + '6' + '<next>' + move +str(roll)
				temp.execute_move(player_id,str_2)
				k, l = temp.get_best_move(player_id,[6])
				str_1 = str_2 +'<next>' + k
				if k == 'NA' : str_1 = str_2
				moves_list.append(str_1)
			elif h == min([b,d,f,h,j]):
				# temp = copy.deepcopy(self)
				move = g[:3]
				str_2 = move + '6' + '<next>' + move +'6'
				temp.execute_move(player_id,str_2)
				k, l = temp.get_best_move(player_id,[roll])
				str_1 = str_2 +'<next>' + k
				if k == 'NA' : str_1 = str_2
				moves_list.append(str_1)
			else:# f>=b and f>=d
				move = i[:3]
				str_1 = move + '6' + '<next>' + move + '6' + '<next>' + move +str(roll)
				moves_list.append(str_1)
		return moves_list



	def get_best_move(self, player_id, dice,execute = False):
		''' Returns the best possible move
		'''
		if dice == [0]: 
			sys.stderr.write("dice rolled is 6 6 6\n")
			return('NA',1)# if dice rolled is 666
			
		if len(dice)== 1: # i.e. single throw (in base form no 6)
			roll = dice[0]
			sys.stderr.write("dice: "+ str(roll)+"\n")
			player_col = self.colours[player_id]
			ini = self.local_positions[player_col]#initial positions
			ini_glob = self.global_positions[player_col]
			opp = self.global_positions[self.opp(player_col)]# opponent position
			# checking for cutting
			sys.stderr.write("Trying to cut"+"\n")
			for ctr_num in range(4):
				try:
					ini_c = ini_glob[ctr_num]
					if ini_c > 52 : continue # home lane
					if ini_c == 0:continue # completed
					if ini_c ==-1 : continue # unopened
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)	
					if poss_c in self.safe_squares: continue # person on safe sqaure
					if poss_c in opp: 
						str1 = player_col + str(ctr_num) + '_' + str(roll) #cutting....Scope: Case-Multiple cuttings..........
						if execute: self.execute_move(player_id,str1)#execution of cutting					
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : return (str1,1)
				except: 
					sys.stderr.write("Not possible: "+ str(ini_c) + " roll"+ str(roll)+"\n")
					continue
			# if my counter is ahead within 6 distance of opposition

			sys.stderr.write("Trying to defend (within 6)"+"\n")
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c > 52 : continue # home lane
				if ini_c == 0:continue # completed
				if ini_c ==-1 : continue # unopened
				try:
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)	
					if ini_c in self.safe_squares: continue # I am not in danger
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
							if poss_c in self.safe_squares: boolean = True # If I can reach safe square then good enough
							if boolean:
								str1 = player_col + str(ctr_num) + '_' + str(roll)
								if execute: self.execute_move(player_id,str1)
								if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : return (str1,2)
				except: continue
			# escaping with large number
			sys.stderr.write("Trying to escape"+"\n")
			if roll>6:
				for ctr_num in range(4):
					ini_c = ini_glob[ctr_num]
					if ini_c > 52 : continue # home lane
					if ini_c == 0 : continue # completed
					if ini_c ==-1 : continue # unopened
					try:
						poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
						if global_to_local(poss_c,player_id) > 27:
							boolean = True
							for opp_c in opp: 
								if opp_c == -1: continue # opponent unopened
								if opp_c >52:continue # opponent on home lane
								if opp_c == 0: continue # opponent counter completed
								if (poss_c - opp_c)%52<=6:
									boolean = False
									break
							if boolean:
								str1 = player_col + str(ctr_num) + '_' + str(roll)
								if execute: self.execute_move(player_id,str1)
								if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : return (str1,2.5)
					except: continue
			# open with 1
			sys.stderr.write("Trying to open with 1"+"\n")
			if roll == 1:
				for ctr_num in range(4):
					if ini_glob[ctr_num]==-1:
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						return (str1,3)
			# if my predicted counter is behind within 6 distance of opposition
			sys.stderr.write("Trying to follow"+"\n")
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c > 52 : continue # home lane
				if ini_c == 0:continue # completed
				if ini_c ==-1 : continue # unopened
				try:
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
					for opp_c in opp: # doesnt matter if opponent is sitting on safe square, he has to move at some point
						# Scope: Check if this move decreases my own safety..........
						if opp_c == -1: continue # opponent unopened
						if opp_c >52:continue # opponent on home lane
						if opp_c == 0: continue # opponent counter completed
						if (opp_c - poss_c)%52 <= 6:
							str1 = player_col + str(ctr_num) + '_' + str(roll)
							if execute: self.execute_move(player_id,str1)
							if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : return (str1,4)
				except: continue
			# homing for extra move
			sys.stderr.write("Trying to get into final state"+"\n")
			for ctr_num in range(4):
				try: # if local_to_global gets input > 57 then exception case
					ini_l_c = ini[ctr_num]
					poss_c = self.local_to_global(ini_l_c+roll,player_col)
					if poss_c==0: 
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						return (str1,5)
				except:
					continue
			# if my counter is ahead within 12 distance of opposition(no immediate danger but danger still)(only for local counters greater than 27)
			for ctr_num in range(4):
				if ini[ctr_num] <= 27: continue
				ini_c = ini_glob[ctr_num]
				if ini_c > 52: continue # home lane
				if ini_c == 0: continue # completed
				if ini_c ==-1: continue # unopened
				try: 
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
					if poss_c in self.safe_squares: # If I reach a safe square
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : return (str1,6)
					for opp_c in opp: 
						if opp_c == -1: continue     # opponent unopened
						if opp_c >  52: continue     # opponent on home lane
						if opp_c ==  0: continue     # opponent counter completed
						if (ini_c - opp_c)%52 <= 12: # Scope: If multiple counters are under threat......................
							str1 = player_col + str(ctr_num) + '_' + str(roll)
							if execute: self.execute_move(player_id,str1)
							if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : return (str1,7)
				except:continue
			# opening with 6
			if roll == 6:
				for ctr_num in range(4):
					if ini_glob[ctr_num]==-1:
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : return (str1,8)
			# safing
			for ctr_num in range(4):
				ini_c = ini_glob[ctr_num]
				if ini_c == -1: continue
				if ini_c == 0: continue				
				if ini_c > 52 : continue # home lane
				try:
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
					if poss_c in self.safe_squares: # If I reach a safe square
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : return (str1,9)
				except:
					continue
			# forwardmost without endangering that
			def sort(l1,b):
				k = copy.copy(l1)
				k.sort(reverse=b)
				return k # copy.copy used as I dont want l1 to get changed, b is for descending
 			for c in sort(ini,True):
				ctr_num = ini.index(c)
				if c == 0: break
				if c == -1: break
				try:
					ini_c = ini_glob[ctr_num]
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)
					if poss_c in self.safe_squares:
						str1 = player_col + str(ctr_num) + '_' + str(roll)
						if execute: self.execute_move(player_id,str1)
						if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0  or poss_c>52: return (str1,11)
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
							if execute: self.execute_move(player_id,str1)
							if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0  or poss_c>52: return (str1,12)
				except:
					continue
			# if all go in danger
			for c in sort(ini, False):
				ctr_num = ini.index(c)
				if c == 0: continue
				if c == -1: continue
				try:
					ini_c = ini_glob[ctr_num]
					poss_c = self.local_to_global(ini[ctr_num]+roll,player_col)	
					str1 = player_col + str(ctr_num) + '_' + str(roll)
					if execute: self.execute_move(player_id,str1)
					if poss_c not in ini_glob or poss_c in self.safe_squares or poss_c ==0 : return (str1,13)
				except:
					continue
			# if I cant move anything
			return ('NA',14)
		elif len(dice) == 2:# dice will be of the form [6,x]
			roll = dice[1]
			a,b = self.get_best_move(player_id, [roll])
			c,d = self.get_best_move(player_id, [6])
			e,f = self.get_best_move(player_id, [6+roll])
			temp = self.copy_board()
			if b<=d and b<=f:
				# temp = copy.deepcopy(self)
				temp.execute_move(player_id,a)
				g, h = temp.get_best_move(player_id,[6])
				str_1 = a +'<next>' +g
				if g == 'NA': str_1 = a
				return(str_1,min(b,h))
			elif d<=b and d<=f:
				# temp = copy.deepcopy(self)
				temp.execute_move(player_id,c)
				g, h = temp.get_best_move(player_id,[roll])
				str_1 = c +'<next>' + g
				if g == 'NA': str_1 = c
				return(str_1,min(d,h))
			else:# f<=b and f<=d
				move = e[:3]
				str_1 = move + '6' + '<next>' + move +str(roll)
				return(str_1,f)
		else:#double 6
			roll = dice[2]
			a,b = self.get_best_move(player_id, [roll])
			c,d = self.get_best_move(player_id, [6])
			e,f = self.get_best_move(player_id, [6+roll])
			g,h = self.get_best_move(player_id, [12])
			i,j = self.get_best_move(player_id, [12+roll])
			temp = self.copy_board()
			if b == min([b,d,f,h,j]):
				# temp = copy.deepcopy(self)
				temp.execute_move(player_id,a)
				k, l = temp.get_best_move(player_id,[6,6])
				str_1 = a +'<next>' +k
				if k == 'NA' : str_1 = a
				return(str_1,min(b,l))
			elif d == min([b,d,f,h,j]):
				# temp = copy.deepcopy(self)
				temp.execute_move(player_id,c)
				k, l = temp.get_best_move(player_id,[6,roll])
				str_1 = c +'<next>' + k
				if k == 'NA' : str_1 = c
				return(str_1,min(d,l))
			elif f == min([b,d,f,h,j]):
				# temp = copy.deepcopy(self)
				move = e[:3]
				str_2 = move + '6' + '<next>' + move +str(roll)
				temp.execute_move(player_id,str_2)
				k, l = temp.get_best_move(player_id,[6])
				str_1 = str_2 +'<next>' + k
				if k == 'NA' : str_1 = str_2
				return(str_1,min(f,l))
			elif h == min([b,d,f,h,j]):
				# temp = copy.deepcopy(self)
				move = g[:3]
				str_2 = move + '6' + '<next>' + move +'6'
				temp.execute_move(player_id,str_2)
				k, l = temp.get_best_move(player_id,[roll])
				str_1 = str_2 +'<next>' + k
				if k == 'NA' : str_1 = str_2
				return(str_1,min(h,l))
			else:# f>=b and f>=d
				move = i[:3]
				str_1 = move + '6' + '<next>' + move + '6' + '<next>' + move +str(roll)
				return(str_1,j)

		# order -> cutting(aggressive bot): done, defending(if any opponent near(within 6 steps)): done, 
		# escaping(if meri aadhi badi hui goti(>25) ko bhaga saku danger ke bahar(>6 distance) even if it is safe initially): will be case when roll > 6: done(numbered 2.5), 
		# opening with 1:done, pursuing (agar mere aage doosre ki goti h toh follow it but not cross)(if I reach within 6 steps) : done, 
		# homing:done, not completely out of danger aage vaali goti ko bhagao:done, opening with 6: done, 
		# safing:done, move inside home lane:done, forwardmost (if no danger), least significant (if all go in danger)

start_string = sys.stdin.readline().strip().split(' ')
start_string = [int(i) for i in start_string]

player_id = start_string[0] - 1 # Get player id to be 0 or 1
time_limit = start_string[1]
game_mode = start_string[2]
draw_board = start_string[3]

if draw_board==1:
	sys.stderr.write("GUI Mode on\n")
	board = Board(game_mode,player_id, True)
else:
	board = Board(game_mode,player_id, False)


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
		if (dice == 'YOU ROLLED 3 SIXES, AND THUS A DUCK'):
			dice = [0]
		else:
			dice = dice.split(' ')
			dice = [int(i) for i in dice[2:]]
		best_move = board.gagan_get_best_move(player_id, dice)
		# TODO: Find the best move for player_id, dice
		# and update this move on the board (Add the get_best_move method)
		#time.sleep(5)
		board.execute_move(player_id, best_move)
		if board.is_game_over():
			sys.stderr.write('*************\nGame Over\n*************\n')
			board.update_weights(1000)
		sys.stdout.write(best_move+'\n')
		sys.stdout.flush()

		# TODO: Check winning condition
		# Wait for opponents move
		dice = sys.stdin.readline().strip()
		if (dice=='REPEAT'):
			continue
		if (dice[9:] == 'ROLLED 3 SIXES, AND THUS A DUCK'):
			dice = [0]
		else:
			dice = dice.split(' ')
			dice = [int(i) for i in dice[3:]]
		if board.can_opp_win(dice):
			sys.stderr.write('*************\nGame Over\n*************\n')
			board.update_weights(-1000)
		move = sys.stdin.readline().strip()
		temp_move = move.split('<next>')
		while(temp_move[-1]=='REPEAT'):
			board.execute_move(1-player_id, move)
			dice = sys.stdin.readline().strip()
			if (dice[9:] == 'ROLLED 3 SIXES, AND THUS A DUCK'):
				dice = [0]
			else:
				dice = dice.split(' ')
				dice = [int(i) for i in dice[3:]]
			sys.stderr.write("Calling can win from REPEAT\n")
			if board.can_opp_win(dice):
				sys.stderr.write('*************\nGame Over\n*************\n')
				board.update_weights(-1000)
			move = sys.stdin.readline().strip()
			temp_move = move.split('<next>')
		board.execute_move(1-player_id, move)
		if board.is_game_over():
			sys.stderr.write('*************\nGame Over\n*************\n')


if (draw_board==1):
	Th = Thread(target = lambda : play_game(board))
	board.intialize_board()
	Th.start()
	board.tk_obj.mainloop()

else:
	play_game(board)

