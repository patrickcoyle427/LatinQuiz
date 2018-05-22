#!/bin/usr/python3

"""
LatinQuiz.py - Game to help learn latin vocabulary.
               Displays a word and 4 choices for answers.
               Tracks the score of the user and shows how well they did

               Special thanks to Dickinson College for their
               Latin Core Vocabulary list, available at:
               http://dcc.dickinson.edu/latin-vocabulary-list

"""

import sys, random, os.path

import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                             QVBoxLayout, QPushButton, QAction, QDialog,
                             QLabel, QStatusBar, QWidget, QGroupBox)

from PyQt5.QtCore import Qt

# TODO:

# Finish the layout of the game UI

# Add a way to restart the game with your current settings

# In the help or file menu, include way to see the source of the doc

class LatinQuiz(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        # Window Widget Layout

        window_layout = QVBoxLayout()

        self.setLayout(window_layout)

        self.word = QLabel('Test', self)
        self.word.setAlignment(Qt.AlignCenter)
        self.word.setStyleSheet('font-family: "Arial Black";')
                      
        window_layout.addWidget(self.word)
        
class LatinMainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        ### Menu Bar ###

        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')

        new_game = QAction('&New Game', self)
        new_game.setShortcut('Ctrl+N')
        new_game.triggered.connect(self.start_new_game)
        
        exit_game = QAction('&Exit', self)
        exit_game.setShortcut('Ctrl+Q')
        exit_game.triggered.connect(self.close)

        file_menu.addAction(new_game)
        file_menu.addAction(exit_game)
        
        help_menu = menubar.addMenu('&Help')

        about_game = QAction('&About', self)
        about_game.triggered.connect(self.about)
        
        teach_me = QAction('&How To Play', self)
        teach_me.setShortcut('Ctrl+H')
        teach_me.triggered.connect(self.how_to_play)

        help_menu.addAction(about_game)
        help_menu.addAction(teach_me)

        ### Status Bar Settings ###

        self.status_bar_message = QLabel('Click File, then New Game to start!')

        self.statusBar().addWidget(self.status_bar_message)
         
        ### Misc Window Settings ###

        self.setCentralWidget(LatinQuiz())

        self.setGeometry(300, 300, 300, 400)

        self.setWindowTitle('Latin Quiz')

        self.show()

    def start_new_game(self):

        # Opens a window to adjust game settings

        pass

    def about(self):
        
        # Credits Dickinson College for their amazing
        # xml document that this is built on.

        # plus A little credit screen for me.

        pass

    def how_to_play(self):

        # Tells the user how to set the game up, the rules,
        # and what exactly this will do.

        pass
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    latin = LatinMainWindow()
    sys.exit(app.exec_())
