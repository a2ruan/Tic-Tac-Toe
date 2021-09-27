#View 

#Libaries
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
from qt_material import apply_stylesheet 
from PyQt5 import QtCore
from main import *

class Widget(QWidget):
    #Global constants
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = WINDOW_WIDTH
    WINDOW_MARGIN = 130
    LINE_THICKNESS = 2
    ELEMENT_THICKNESS = 4
    BUTTON_MARGIN = 20

    #Theme constants
    FONT_SIZE = 15 #px
    PRIMARY_COLOR = "#1de9b6"
    SECONDARY_COLOR = "#1976D2"
    TERTIARY_COLOR = "#018786"
    LOSER_COLOR = "#D3D3D3"

    #Constructor
    def __init__(self, app):
        # Set up threading protocol for ascynchronous communication w/ Controller.
        # Input of constructor is a pointer to (self), to access all instance variables
        self.thread = ControllerThread(self)
        self.thread.start()

        # Instance variables
        self.scores = [0,0,0]
        #Set up grid contents for paintEvent. 0 = empty.  1 = player 1.  2 = player 2
        self.grid_content=[0]*9
        self.player_turn = 1 

        # Initialize Application
        super().__init__()
        self.app = app
        self.set_gui_size(self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        
        # Format GUI
        apply_stylesheet(self.app,theme="dark_teal.xml")
        self.setWindowTitle("TIC TAC TOE | MATERIAL EDITION")
        self.k = 0
        self.set_widgets()

        self.winner_indicator = False

    def connect_and_emit_trigger(self):
        self.trigger.connect(self.handle_trigger)

    def handle_trigger(self):
        print("trigger signal recieved")

    #Trigger on mouse click
    def mousePressEvent(self, QMouseEvent):
        x_pos = QMouseEvent.pos().x()
        y_pos = QMouseEvent.pos().y()

        # Check if mouse click is within grid bounds
        if self.WINDOW_MARGIN <= x_pos <= self.WINDOW_WIDTH - self.WINDOW_MARGIN \
            and self.WINDOW_MARGIN <= y_pos <= self.WINDOW_HEIGHT - self.WINDOW_MARGIN:
            # Identify click area based on mouse position on 3x3 grid, then draw shape
            for i in range(1,4):
                if  y_pos <= self.get_click_limit(i):
                    if x_pos <= self.get_click_limit(1):
                        if self.grid_content[(i-1)*3] == 0:
                            self.player_turn = self.player_turn*(-1) # Change player turn
                            self.grid_content[(i-1)*3] = self.player_turn # Update player moves
                            self.thread.set_piece(self.player_turn, (i-1)*3+1)
                            #print(str(1+(i-1)*3))
                        break
                    elif x_pos <= self.get_click_limit(2):
                        #print(str(2+(i-1)*3))
                        if self.grid_content[1+(i-1)*3] == 0:
                            self.player_turn = self.player_turn*(-1)
                            self.grid_content[1+(i-1)*3] = self.player_turn
                            self.thread.set_piece(self.player_turn, (i-1)*3+2)
                        break
                    else:
                        #print(str(3+(i-1)*3))
                        if self.grid_content[2+(i-1)*3] == 0:
                            self.player_turn = self.player_turn*(-1)
                            self.grid_content[2+(i-1)*3] = self.player_turn
                            self.thread.set_piece(self.player_turn, (i-1)*3+3)
                        break
            self.update() # Update GUI Painter, to display X or O on grid
        #print(self.grid_content)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    #Calculate grid size based on height and width of current window
    def get_click_limit(self, row):
        #
        return self.WINDOW_MARGIN+row*(self.WINDOW_WIDTH-2*self.WINDOW_MARGIN)/3
    
    #Initialize widget elements
    def set_widgets(self):
        # Buttons
        self.bt_restart = QPushButton()
        self.bt_restart.setText('Restart Game')
        self.bt_restart.clicked.connect(self.restart_game)
        self.bt_restart.clicked.connect(self.thread.restart_game)
        self.bt_restart.move(self.WINDOW_MARGIN,int(self.WINDOW_MARGIN/3))

        self.bt_reset_score = QPushButton()
        self.bt_reset_score.setText('Reset Score')
        self.bt_reset_score.clicked.connect(self.reset_score)
        self.bt_reset_score.clicked.connect(self.thread.reset_score)
        self.bt_reset_score.move(self.WINDOW_WIDTH-self.WINDOW_MARGIN-self.bt_reset_score.size().width()-self.BUTTON_MARGIN,\
            int(self.WINDOW_MARGIN/3))

        # Scoring Labels
        self.l_player1_wins = QLabel()
        self.l_player1_wins.setText("Wins: "+ str(self.scores[0]))
        self.l_player1_wins.setFont(QFont('AnyStyle',self.FONT_SIZE))
        self.l_player1_wins.setStyleSheet("color: " + self.PRIMARY_COLOR)
        
        self.l_player2_wins = QLabel()
        self.l_player2_wins.setText("Wins: "+ str(self.scores[2]))
        self.l_player2_wins.setFont(QFont('AnyStyle',self.FONT_SIZE))
        self.l_player2_wins.setStyleSheet("color: " + self.SECONDARY_COLOR)

        
        self.l_ties = QLabel()
        self.l_ties.setText("Ties: "+ str(self.scores[1]))
        self.l_ties.setFont(QFont('AnyStyle',self.FONT_SIZE))
        self.l_ties.setStyleSheet("color: " + self.TERTIARY_COLOR)

        # Grid Layout Top
        self.layout = QVBoxLayout()
        self.top_menu = QHBoxLayout()
        self.top_menu.addWidget(self.bt_restart)
        self.top_menu.addWidget(self.bt_reset_score)
        self.top_menu.setContentsMargins(self.WINDOW_MARGIN,int(self.WINDOW_MARGIN/3),self.WINDOW_MARGIN,0)
        self.layout.addLayout(self.top_menu)

        # Grid Layout Bottom
        self.score_menu = QHBoxLayout()
        self.score_menu.addWidget(self.l_player1_wins)
        self.score_menu.addWidget(self.l_ties)
        self.score_menu.addWidget(self.l_player2_wins)
        self.score_menu.setContentsMargins(self.WINDOW_MARGIN,0,self.WINDOW_MARGIN,0)
        self.layout.addStretch()
        self.layout.addLayout(self.score_menu)
        self.layout.setContentsMargins(10,0,10,int(self.WINDOW_MARGIN/2))
        self.setLayout(self.layout)

    #Initialize GUI with specified width and height (px)
    def set_gui_size(self, width, height):
        #Get screen size to center the application
        self.screen = self.app.primaryScreen()
        self.size = self.screen.size()
        self.resize(width, height)
        widget_size = self.frameGeometry()
        #Recenter GUI based on screen size and widget size
        self.move(int((self.size.width() - widget_size.width())/2), \
            int((self.size.height()-widget_size.height())/2))

    #Restart game by resetting player moves and updating painter
    def restart_game(self):
        self.grid_content = [0]*9
        self.winner_indicator = False
        self.update()

    #Restart game and reset all player scores
    def reset_score(self):
        #print("resetting score")
        self.restart_game()
        self.scores = [0,0,0]
        self.update_labels()

    def set_score(self,score):
        self.scores = score
        #print("setting score")
        #print(self.score)
        self.update_labels()

    def update_labels(self):
        self.l_player1_wins.setText("Wins: "+ str(self.scores[0]))
        self.l_ties.setText("Ties: "+ str(self.scores[1]))
        self.l_player2_wins.setText("Wins: "+ str(self.scores[2]))

        self.l_player1_wins.update()
        self.l_player2_wins.update()
        self.l_ties.update()

    def flash_winner(self, win_case):
        self.winner_indicator = True
        for i in range(len(self.grid_content)):
            if i+1 in (win_case):
                self.grid_content[i] *= 2
        print(self.grid_content)
        self.update()

    def get_board(self):
        return self.grid_content

    #Paint drawing elements to GUI
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.gray)

        # Grid Painting
        for i in range(1,3):
            painter.fillRect(int((self.WINDOW_WIDTH-2*self.WINDOW_MARGIN)/3*i-self.LINE_THICKNESS/2+self.WINDOW_MARGIN),\
                self.WINDOW_MARGIN,self.LINE_THICKNESS,\
                self.WINDOW_HEIGHT-2*self.WINDOW_MARGIN, Qt.gray)

            painter.fillRect(self.WINDOW_MARGIN,\
                int((self.WINDOW_HEIGHT-2*self.WINDOW_MARGIN)/3*i-self.LINE_THICKNESS/2+self.WINDOW_MARGIN),\
                self.WINDOW_WIDTH-2*self.WINDOW_MARGIN,self.LINE_THICKNESS, Qt.gray)

        # Player Pieces Painting
        grid_size = int((self.WINDOW_WIDTH-2*self.WINDOW_MARGIN)/3)
        circle_size = int(grid_size*0.75/2)
        cross_size = int(grid_size*0.6)
        kk = int(grid_size*0.15)

        # Update piece colors if winner detected
        if self.winner_indicator:
            player_1_color = self.LOSER_COLOR
            player_2_color = self.LOSER_COLOR
        else:
            player_1_color = self.PRIMARY_COLOR
            player_2_color = self.SECONDARY_COLOR


        # Update grid based on player moves matrix => grid_content
        for i in range(3):
            for j in range(3):
                grid_center_point = QPointF(self.WINDOW_MARGIN+grid_size*(i+0.5),self.WINDOW_MARGIN+grid_size*(j+0.5))
                if self.grid_content[i+j*3]==1:
                    painter.setPen(QPen(QColor(player_1_color),self.ELEMENT_THICKNESS,Qt.SolidLine))
                    painter.drawEllipse(grid_center_point,circle_size,circle_size)
                if self.grid_content[i+j*3]==2:
                    print("2")
                    painter.setPen(QPen(QColor(self.PRIMARY_COLOR),self.ELEMENT_THICKNESS+6,Qt.SolidLine))
                    painter.drawEllipse(grid_center_point,circle_size,circle_size)
                if self.grid_content[i+j*3]==-1:
                    painter.setPen(QPen(QColor(player_2_color),self.ELEMENT_THICKNESS,Qt.SolidLine))
                    painter.drawLine(self.WINDOW_MARGIN+kk+grid_size*(i),self.WINDOW_MARGIN+grid_size*(j+1)-kk,\
                        self.WINDOW_MARGIN-kk+grid_size*(i+1),self.WINDOW_MARGIN+grid_size*(j)+kk)
                    painter.drawLine(self.WINDOW_MARGIN+kk+grid_size*(i),self.WINDOW_MARGIN+grid_size*(j)+kk,\
                        self.WINDOW_MARGIN-kk+grid_size*(i+1),self.WINDOW_MARGIN+grid_size*(j+1)-kk)
                if self.grid_content[i+j*3]==-2:
                    print("-2")
                    painter.setPen(QPen(QColor(self.SECONDARY_COLOR),self.ELEMENT_THICKNESS+6,Qt.SolidLine))
                    painter.drawLine(self.WINDOW_MARGIN+kk+grid_size*(i),self.WINDOW_MARGIN+grid_size*(j+1)-kk,\
                        self.WINDOW_MARGIN-kk+grid_size*(i+1),self.WINDOW_MARGIN+grid_size*(j)+kk)
                    painter.drawLine(self.WINDOW_MARGIN+kk+grid_size*(i),self.WINDOW_MARGIN+grid_size*(j)+kk,\
                        self.WINDOW_MARGIN-kk+grid_size*(i+1),self.WINDOW_MARGIN+grid_size*(j+1)-kk)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = Widget(app)
    w1.show()
    #ex.resize(400, 280)
    sys.exit(app.exec_())