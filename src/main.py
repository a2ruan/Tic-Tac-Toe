from game import *
from player import *
from gui import *
import sys, time

class ControllerThread(QThread):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.exiting = False

        self.player_1 = Player("Player 1")
        self.player_2 = Player("Player 2")
        self.game = Game(self.player_1,self.player_2)

    def on_source(self, lineftxt):
        self.source_text = lineftxt

    def run(self): 
        self.running = True
        while self.running:
            if self.game.get_winner() == 0:
                pass
            elif self.game.get_winner() == 3:
                self.player_1.increment_ties()
                self.player_2.increment_ties()

                self.widget.set_score([self.player_1.get_wins(),self.player_1.get_ties(),self.player_2.get_wins()])
                self.game.reset_board()
                self.widget.restart_game()

            else:
                print(self.game.get_winner().get_name())
                self.game.get_winner().increment_wins()
                self.widget.set_score([self.player_1.get_wins(),self.player_1.get_ties(),self.player_2.get_wins()])

                self.widget.flash_winner(self.game.get_win_combo())
                time.sleep(2)
                self.game.reset_board()
                self.widget.restart_game()

            time.sleep(1)
            #print(self.widget.get_board()) 

    def restart_game(self):
        self.game.reset_board()

    def reset_score(self):
        self.game.reset_board()
        self.player_1.set_score(0,0,0)
        self.player_2.set_score(0,0,0)

    def get_score(self):
        return self.widget.get_score()

    def set_piece(self, player, location):
        self.game.set_piece(player, location)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = Widget(app)
    w1.show()
    sys.exit(app.exec_())
