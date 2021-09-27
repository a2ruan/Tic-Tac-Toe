from game import *
from player import *
from gui import *
import sys, time
from threading import Thread 

class ControllerThread(QThread):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.exiting = False

        self.p1 = Player("Player 1")
        self.p2 = Player("Player 2")
        self.g1 = Game(self.p1,self.p2)

    def on_source(self, lineftxt):
        self.source_text = lineftxt

    def run(self): 
        self.running = True
        while self.running:
            time.sleep(1)
            print(self.widget.get_board()) 

    def restart_game(self):
        print("Restart Game")

    def reset_score(self):
        print("Reset Score")

    def set_score(self, score):
        self.widget.set_score(score)

    def get_score(self):
        return self.widget.get_score()

    def set_piece(self, player, location):
        pass #self.g1.set_piece(plauer)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = Widget(app)
    w1.show()
    #ex.resize(400, 280)
    sys.exit(app.exec_())
