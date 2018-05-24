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
                             QLabel, QStatusBar, QWidget, QGroupBox,
                             QLineEdit, QRadioButton, QToolTip,
                             QButtonGroup)

from PyQt5.QtCore import Qt

# TODO:

# Finish the layout of the game UI
# Continue working on start new quiz dialog

# Add a way to restart the game with your current settings

# Record questions the user got wrong to help them study?

# In the help or file menu, include way to see the source of the doc

class LatinQuiz(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        ### Window Widget Layout ###

        window_layout = QVBoxLayout()

        self.setLayout(window_layout)

        self.word = QLabel('', self)
        # self.word holds current question. It is set by ___ below
        self.word.setAlignment(Qt.AlignCenter)
        self.word.setStyleSheet('font-family: "Arial Black";')
                      
        window_layout.addWidget(self.word)

        self.answer_group = QGroupBox()
        # Container for the answers

        ### Buttons to Answer Questions ###

        # Each button is enabled when the quiz is started. Their labels will
        # have the possible answers the to displayed question.

        self.a_button = QPushButton('A', self)
        self.a_button.setMaximumWidth(50)
        self.a_button.setEnabled(False)
        self.a_button.clicked.connect(self.question_answered)
        
        self.b_button = QPushButton('B', self)
        self.b_button.setMaximumWidth(50)
        self.b_button.setEnabled(False)
        self.b_button.clicked.connect(self.question_answered)
        
        self.c_button = QPushButton('C', self)
        self.c_button.setMaximumWidth(50)
        self.c_button.setEnabled(False)
        self.c_button.clicked.connect(self.question_answered)
        
        self.d_button = QPushButton('D', self)
        self.d_button.setMaximumWidth(50)
        self.d_button.setEnabled(False)
        self.d_button.clicked.connect(self.question_answered)

        self.a_label = QLabel('', self)
        self.a_label.setAlignment(Qt.AlignCenter)
        
        self.b_label = QLabel('', self)
        self.b_label.setAlignment(Qt.AlignCenter)
        
        self.c_label = QLabel('', self)
        self.c_label.setAlignment(Qt.AlignCenter)
        
        self.d_label = QLabel('', self)
        self.d_label.setAlignment(Qt.AlignCenter)

        a_layout = QHBoxLayout()
        a_layout.addWidget(self.a_button)
        a_layout.addWidget(self.a_label)

        b_layout = QHBoxLayout()
        b_layout.addWidget(self.b_button)
        b_layout.addWidget(self.b_label)

        c_layout = QHBoxLayout()
        c_layout.addWidget(self.c_button)
        c_layout.addWidget(self.c_label)

        d_layout = QHBoxLayout()
        d_layout.addWidget(self.d_button)
        d_layout.addWidget(self.d_label)

        answer_group_layout = QVBoxLayout()
        answer_group_layout.addLayout(a_layout)
        answer_group_layout.addLayout(b_layout)
        answer_group_layout.addLayout(c_layout)
        answer_group_layout.addLayout(d_layout)

        self.answer_group.setLayout(answer_group_layout)

        window_layout.addWidget(self.answer_group)

    def question_answered(self):

        # When a button is pressed, the question's answer is checked against
        # what the user selected. The incorrect buttons become red and the
        # correct answer turns green. Something alerts the user if they were
        # correct or not

        pass

        
class LatinMainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        ### Menu Bar ###

        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')

        new_quiz = QAction('&New Quiz', self)
        new_quiz.setShortcut('Ctrl+N')
        new_quiz.triggered.connect(self.start_new_quiz)
        
        exit_game = QAction('&Exit', self)
        exit_game.setShortcut('Ctrl+Q')
        exit_game.triggered.connect(self.close)

        file_menu.addAction(new_quiz)
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

        self.status_bar_message = QLabel('Click File, then New Quiz to start!')

        self.statusBar().addWidget(self.status_bar_message)
         
        ### Misc Window Settings ###

        Quiz = LatinQuiz()
        # Creates an instance of LatinQuiz()

        self.setCentralWidget(Quiz)
        # Makes LatinQuiz() the widget that the main window uses

        self.previous_settings = []
        # Container for the last choosen settings, used for restarting a quiz

        self.setGeometry(300, 300, 300, 400)

        self.setWindowTitle('Latin Quiz')

        self.show()

    def start_new_quiz(self):

        options = self.start_quiz_options()

        # Opens a window to adjust game settings

    def start_quiz_options(self):

        # Builds the window that displays when a new quiz begins

        start_quiz_window = QDialog(None, Qt.WindowCloseButtonHint)
        # Qt.WindowCloseButtonHint Prevents the ? button from appearing
        # in the dialog window

        start_quiz_layout = QVBoxLayout()

        set_difficulty_container = QGroupBox()

        set_difficulty_layout = QHBoxLayout()

        set_difficulty_group = QButtonGroup()
        # Groups the difficulty Radio Buttons together

        self.difficulty_buttons = (QRadioButton('Easy'), QRadioButton('Normal'), QRadioButton('Hard'),
                              QRadioButton('Very Hard'), QRadioButton('Everything'))

        # Difficulties correspond to how common the words in the questions occur in Latin
        # Easy: 50 Most Common Words
        # Normal: 100 Most Common Words
        # Hard: 250 Most Common Words
        # Very Hard: 500 Most Common Words
        # Everything: All 1000(ish) Words

        id_num = 0

        for button in self.difficulty_buttons:

            set_difficulty_group.addButton(button)
            set_difficulty_group.setId(button, id_num)

            id_num += 1

            set_difficulty_layout.addWidget(button)

        set_difficulty_container.setLayout(set_difficulty_layout)


        start_quiz_layout.addWidget(set_difficulty_container)

        start_quiz_window.setGeometry(300, 300, 200, 300)

        start_quiz_window.setWindowTitle('Start New Quiz')

        start_quiz_window.setLayout(start_quiz_layout)

        start_quiz_window.exec_()

    def about(self):
        
        # Credits Dickinson College for their amazing
        # xml document that this is built on.

        # plus a little credit screen for me.

        pass

    def how_to_play(self):

        # Tells the user how to set the quiz up, the rules,
        # and what exactly this will do.

        pass
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    latin = LatinMainWindow()
    sys.exit(app.exec_())
