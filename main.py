from game import *
from player import *
from gui import *
import sys, time
from threading import Thread

class Backend(Thread):
	def __init__(self, gui):
		super().__init__()
		self.gui = gui

	def run(self):
		while self.gui.running:
			print("Hello")
			time.sleep(1)	

class GUI(Thread):
	def __init__(self):
		super().__init__()
		self.running = True

	def run(self):
		self.app = QApplication(sys.argv)
		self.w1 = Widget(self.app)
		self.w1.show()
		print(self.w1.get_board())
		self.app.exec_()
		#Once GUI is closed, close backend
		self.running = False
		sys.exit(self.app.exec_())

if __name__ == '__main__':
	thread_gui = GUI()
	thread_backend = Backend(thread_gui)
	thread_backend.start()
	thread_gui.start()


"""
p1 = Player("Cindy")
p2 = Player("Andy")
g1 = Game(p1,p2)
g1.get_board()
g1.set_piece(p1,9)
g1.set_piece(p1,5)
g1.set_piece(p1,1)
print(g1.player1_moves)
print(g1.player2_moves)
g1.get_board()
print(g1.player1_moves)
print(g1.get_winner())
"""