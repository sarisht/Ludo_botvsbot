try:
	import Tkinter
except:
	import tkinter as Tkinter
# Width Of All Boxes
S_WIDTH=36



# Height Of All Boxes
S_HEIGHT=36

# Number Of Boxes
AREA = 15


# =================================================
# 				Colors Settings
# =================================================
#
# Track Color
C_0_A = "SkyBlue3" # When Active
C_0_D = "SkyBlue2" # when Deactive

# TEAM 
C_1 = "Blue"			# Default
C_1_A = "RoyalBlue2"	# When Active
C_1_D = "RoyalBlue1"	# When Deactive


C_2 = "red"
C_2_A = "firebrick2"	
C_2_D = "firebrick1"


C_3 = "green"
C_3_A = "green2"	
C_3_D = "green1"


C_4 = "yellow"
C_4_A = "yellow2"	
C_4_D = "yellow1"


# List Of Active Colors
COLOR = [C_1_A, C_2_A, C_3_A, C_4_A]

#from models import *
def tracks(s, r):
	return [s.format(i) for i in r]

# Creating Main Track Square Boxes
TRACK = []
TRACK+= tracks("6.{}", range(6))[::-1]
TRACK+= ['7.0']
TRACK+= tracks("8.{}", range(6))
TRACK+= tracks("{}.6", range(9,15))
TRACK+= ['14.7']
TRACK+= tracks("{}.8", range(9,15))[::-1]
TRACK+= tracks("8.{}", range(9,15))
TRACK+= ['7.14']
TRACK+= tracks("6.{}", range(9,15))[::-1]
TRACK+= tracks("{}.8", range(6))[::-1]
TRACK+= ['0.7']
TRACK+= tracks("{}.6", range(6))




# Creating Ending Tracks
F_TRACK=[]
F_TRACK.append(tracks("7.{}", range(1,7)))
F_TRACK.append(tracks("{}.7", range(8,14))[::-1])
F_TRACK.append(tracks("7.{}", range(8,14))[::-1])
F_TRACK.append(tracks("{}.7", range(1,7)))

# Now Creating Roots
TRAIN_1=TRACK[8:]+TRACK[:7]+F_TRACK[0]+['7.6']	 # ROOT One
TRAIN_2=TRACK[21:]+TRACK[:20]+F_TRACK[1]+['8.7'] # Root Two
TRAIN_3=TRACK[34:]+TRACK[:33]+F_TRACK[2]+['7.8'] # Root Three
TRAIN_4=TRACK[47:]+TRACK[:46]+F_TRACK[3]+['6.7'] # Root Four

# Station
STATIONS=[]
STATIONS.append(['11.2','12.2','11.3','12.3'])
STATIONS.append(['11.11','12.11','11.12','12.12'])
STATIONS.append(['2.11','3.11','2.12','3.12'])
STATIONS.append(['2.2','3.2','2.3','3.3'])

# TEAM A COINS
TEAM = []
TEAM.append(["C{}".format(i) for i in STATIONS[0]]+["C{}".format(i) for i in STATIONS[3]])
TEAM.append(["C{}".format(i) for i in STATIONS[1]]+["C{}".format(i) for i in STATIONS[2]])
#print TEAM

OVALS = [
(TRAIN_1, STATIONS[0], C_1, "A"),
(TRAIN_2, STATIONS[1], C_2, "B"),
(TRAIN_3, STATIONS[2], C_3, "B"),
(TRAIN_4, STATIONS[3], C_4, "A"),
]



# Stops
STOPS = [
'8.1',
'12.6',
'13.8',
'8.12',
'6.13',
'2.8',
'1.6',
'6.2',
]



# Main Class For Canvas Widget
class Board(Tkinter.Canvas):
	def __init__(self, *args, **kwargs):
		Tkinter.Canvas.__init__(self, *args, **kwargs)
		self.create_squares()
		self.highlight()
		self.configure(width=S_WIDTH*AREA, height=S_HEIGHT*AREA)


	# Filling Colors In Boxes
	def highlight(self):

		# Main Tracks
		for c in TRACK:
			self.itemconfigure(c, fill=C_0_D, activewidth=2, activefill=C_0_A, activeoutline="black")

		# Ending Tracks
		for n,k in enumerate(F_TRACK):
			for j in k:
				self.itemconfigure(j, fill=COLOR[n], activewidth=2, activeoutline='black')


		# Stations
		for n,s in enumerate(STATIONS):
			for j,c in enumerate(s):
				self.itemconfigure(c, fill=COLOR[n], activewidth=2)
				coordinates = self.coords(c)
				#store=self.create_oval(*coordinates, fill=COLOR[n], width=3, tag="COIN{}{}".format(n,j))
				#self.tag_bind(store,"<Enter>",self.coin_bind)
#				print n,s,j,c
		
		# Stops
		for s in STOPS:
			self.itemconfigure(s, fill="gray58", activefill="gray70", activewidth=3, activeoutline="gray10")
		return

	# Creating Square Boxes
	def create_squares(self):
		for i in range(AREA):
			for j in range(AREA):
				self.create_rectangle(S_WIDTH*i, S_HEIGHT*j, (S_WIDTH*i)+S_WIDTH,(S_HEIGHT*j)+S_HEIGHT, tag="{}.{}".format(i,j), outline='white', fill="ivory")
#				self.create_text(S_WIDTH*i+20, S_HEIGHT*j+20, text="{}.{}".format(i,j))
		return


# main Trigger
if __name__=="__main__":
	root = Tkinter.Tk()
	c = Board(root, width=S_WIDTH*AREA, height=S_HEIGHT*AREA)
	c.pack(expand=True, fill="both")
	root.mainloop()