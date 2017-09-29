import sys

class Board(object):
	"""Class for storing the current state of the game and moves"""
	def __init__(self, game_mode):
		self.start_squares = {'G':1, 'Y':14, 'B':27, 'R':40}
		self.walk_start_squares = {'G':53, 'Y':58, 'B':63, 'R':68}
		if game_mode==0:
			self.colours = ['R','Y']
			self.local_positions = {'R':[-1,-1,-1,-1], 'Y':[-1,-1,-1,-1]}
			self.global_positions = {'R':[-1,-1,-1,-1], 'Y':[-1,-1,-1,-1]}
		else:
			self.colours = ['B', 'G']
			self.local_positions = {'B':[-1,-1,-1,-1], 'G':[-1,-1,-1,-1]}
			self.global_positions = {'B':[-1,-1,-1,-1], 'G':[-1,-1,-1,-1]}
	
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

	# TODO: Complete this method		
	def exceute_move(self, player_id, move):
		''' Executes a move on the board
		'''
		# Look at the local position of the counter, and update it.
		# Find the global position using local_to_global
		# Update Global position as well

	# TODO: Complete this method
	def get_best_move(self, player_id, dice):
		''' Returns the best possible move
		'''


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