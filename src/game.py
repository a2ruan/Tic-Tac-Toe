#Model
class Game:
	# Constructor
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.player1_moves = {-1}
		self.player2_moves = {-1}

	# Set player piece based on location
	def set_piece(self,player,location):
		#print(location)
		if not location in range(1,10):
			print("Invalid location")
		elif location in self.player1_moves or location in self.player2_moves:
			print("Location in use.  Please select another location") 
		elif player == 1:
			self.player1_moves.add(location)
		elif player == -1:
			self.player2_moves.add(location)
		else:
			print("Player does not exist")

	# Get winner based on current board status.  Returns (int)0 if no winner found.
	def get_winner(self):
		win_cases = [
		{1,2,3},{4,5,6},{7,8,9},
		{1,4,7},{2,5,8},{3,6,9},
		{1,5,9},{3,5,7}
		]
		for win_case in win_cases:
			#print(win_case)
			if win_case.issubset(self.player1_moves):
				return self.player1
			elif win_case.issubset(self.player2_moves):
				return self.player2
			elif len(self.player1_moves) == 6 or len(self.player2_moves) == 6:
				return 3  # tie condition
		return 0

	# Get winning combination
	def get_win_combo(self):
		win_cases = [
		{1,2,3},{4,5,6},{7,8,9},
		{1,4,7},{2,5,8},{3,6,9},
		{1,5,9},{3,5,7}
		]
		for win_case in win_cases:
			#print(win_case)
			if win_case.issubset(self.player1_moves):
				return win_case
			elif win_case.issubset(self.player2_moves):
				return win_case
			elif len(self.player1_moves) == 6 or len(self.player2_moves) == 6:
				return 3  # tie condition
		return 0

	# Prints out current board
	def get_board(self):
		pieces = ["-"]*9

		for i in range(len(pieces)):
			if i+1 in self.player1_moves:
				pieces[i] = "x"
			elif i+1 in self.player2_moves:
				pieces[i] = "o"
		print(" ")
		print(pieces[0],pieces[1],pieces[2])
		print(pieces[3],pieces[4],pieces[5])
		print(pieces[6],pieces[7],pieces[8])

	# Reset game by resetting player move lists
	def reset_board(self):
		self.player1_moves = {-1}
		self.player2_moves = {-1}