#Model 
class Player:
	def __init__(self, name):
		self.name = name
		self.wins = 0
		self.losses = 0
		self.ties = 0

	def get_name(self):
		return self.name

	def set_name(self, name):
		self.name = name

	def get_score(self):
		return "Wins: " + self.wins + " Losses: " + self.losses

	def set_score(self, wins, ties, losses):
		self.wins = wins
		self.losses = losses
		self.ties = ties

	def increment_wins(self):
		self.wins += 1

	def increment_losses(self):
		self.losses += 1

	def increment_ties(self):
		self.ties += 1

	def get_wins(self):
		return self.wins

	def get_ties(self):
		return self.ties