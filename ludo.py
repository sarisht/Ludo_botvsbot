import sys

class Board(object):
	"""Class for storing the current state of the game and moves"""
	def __init__(self, game_mode):
		self.start_squares = {'G':1, 'Y':14, 'B':27, 'R':40}
		self.walk_start_squares = {'G':53, 'Y':58, 'B':63, 'R':68}
		self.safe_squares = [1,9,14,22,27,35,40,48]
		if game_mode==0:
			self.colours = ['R','Y']
			self.local_positions = {'R':[-1,-1,-1,-1], 'Y':[-1,-1,-1,-1]}
			self.global_positions = {'R':[-1,-1,-1,-1], 'Y':[-1,-1,-1,-1]}
		else:
			self.colours = ['B', 'G']
			self.local_positions = {'B':[-1,-1,-1,-1], 'G':[-1,-1,-1,-1]}
			self.global_positions = {'B':[-1,-1,-1,-1], 'G':[-1,-1,-1,-1]}

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
		if (i==-1):
			return -1
		elif(i<=0):
			raise Exception("Input given to Board.local_to_global is <=0 and not = -1")
		elif (i>56):
			raise Exception("Input given to Board.local_to_global is > 56")			
		elif (i<52):
			return (i+self.start_squares[c]-2)%52 + 1
		else:
			return (i-52 + self.walk_start_squares[c])

	def global_to_local(self, i, c):
		''' Converts a global board position to a local board position w.r.t a colour
		'''
		# TODO: Add a check for squares not reachable by a colour. (Eg: Sq 52 cannot be reached by yellow)
		if (i==-1):
			return -1
		elif (i<=0):
			raise Exception("Input given to Board.global_to_local is <=0 and not = -1")
		elif (i>72):
			raise Exception("Input given to Board.global_to_local is > 72")			
		elif (i<53):
			return (i - self.start_squares[c])%52 + 1
		else:
			return (i-self.walk_start_squares[c] + 52)

	# TODO: Complete this method		I think this should handle execution except for case where multiple dices are thrown example (6,3)
	# In that case what will be the input like? one at a time followed by <\n> should handled
	def exceute_move(self, player_id, move_str):
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

	# TODO: Complete this method to double check we don't make a mistake
	def is_valid_move(self, move, player_id):
		'''Returns True is a given move is valid, False otherwise
		'''
	# TODO: Complete this method
	def get_best_move(self, player_id, dice):
		''' Returns the best possible move
		'''
		# order -> cutting(aggressive bot), defending(if any opponent near(within 12 steps)), escaping(if meri aadhi badi hui goti(>24) ko bhaga saku danger ke bahar even if it is safe initially), pursuing(agar mere aage doosre ki goti h toh follow it but not cross), opening, frowardmost (if no danger), safing, least in danger


start_string = sys.stdin.readline().strip().split(' ')
start_string = [int(i) for i in start_string]

player_id = start_string[0] - 1
time_limit = start_string[1]
game_mode = start_string[2]

board = Board(game_mode)

# Wait for first move from the other player (only if player_id is 1 (You are player 2))
if player_id==1:
	dice = sys.stdin.readline().strip()
	move = sys.stdin.readline().strip()
	board.exceute_move(0, move)

while(True):
	sys.stdout.write('<THROW>\n')
	sys.stdout.flush()
	dice = sys.stdin.readline().strip()
	best_move = board.get_best_move(player_id, dice)
	# TODO: Find the best move for player_id, dice
	# and update this move on the board (Add the get_best_move method)
	sys.stdout.write(best_move)
	sys.stdout.flush()
	board.exceute_move(player_id, best_move)
	# TODO: Check winning condition
	# Wait for opponents move
	# TODO: Dealing with REPEAT 
	dice = sys.stdin.readline().strip()
	move = sys.stdin.readline().strip()
	board.exceute_move(1-player_id, move)
