#!/bin/usr/python3

"""
LatinQuiz.py - Game to help learn latin vocabulary.
               Displays a word and 4 choices for answers.
               Tracks the score of the user and shows how well they did

               Special thanks to Dickinson College for their
               Latin Core Vocabulary list, available at:
               http://dcc.dickinson.edu/latin-vocabulary-list

"""

# TO DO:

# Add a way to restart the game with your current settings

# Finish the 'About' menu

# Finish the 'How To Play' menu

import sys, LatinQuizWidget

from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                             QVBoxLayout, QPushButton, QAction, QDialog,
                             QLabel, QStatusBar, QGroupBox,
                             QRadioButton, QToolTip, QButtonGroup)

from PyQt5.QtCore import Qt

class LatinMainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.Quiz = LatinQuizWidget.LatinQuiz(self)
        # Creates an instance of LatinQuiz()
        # Passes the object instance to LatinQuiz so it can access
        # objects in the main window.

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

        self.setCentralWidget(self.Quiz)
        # Makes LatinQuiz() the widget that the main window uses

        self.previous_settings = []
        # Container for the last chosen settings, used for restarting a quiz

        self.setGeometry(300, 300, 700, 400)

        self.setWindowTitle('Latin Quiz')

        self.show()

    def start_new_quiz(self):

        # Collects the options and starts the Latin quiz

        options = self.start_quiz_options()

        # Opens a window to adjust game settings

        if options != None:

            self.Quiz.start_quiz(options)

            # Calls the start_quiz function from LatinQuizWidget

    def start_quiz_options(self):

        # Builds the window that displays when a new quiz begins

        ### Initial Setup ###

        difficulty = (50, 100, 250, 500, 1000)

        questions = (25, 50, 1000)
        
        # These tuples hold the what each option below corresponds to
        # The difficulty is how many words will be chosen for questions
        # the questions will be how many questions the quiz contains

        start_quiz_window = QDialog(None, Qt.WindowCloseButtonHint)
        # Qt.WindowCloseButtonHint Prevents the ? button from appearing
        # in the dialog window

        options_layout = QHBoxLayout()
        # Holds the radio button options for starting a game.

        ### Difficulty Selection ###

        start_quiz_layout = QVBoxLayout()

        set_difficulty_container = QGroupBox('Question Difficulty')
        set_difficulty_container.setToolTip('Choose how many words will be in the question pool.\n' +
                                            'Easy: 50 Most common words used.\n' +
                                            'Normal: 100 Most common words used.\n' +
                                            'Hard: 250 Most common words used.\n' +
                                            'Very Hard: 500 Most common words used.\n' +
                                            'Everything: ALL 1000 words used')

        start_quiz_layout.addLayout(options_layout)

        set_difficulty_layout = QVBoxLayout()

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

            # This loop adds all the buttons to the set_difficulty_group,
            # Gives them an ID number, and adds them to the GroupBox's layout

            set_difficulty_group.addButton(button)
            set_difficulty_group.setId(button, id_num)

            id_num += 1

            set_difficulty_layout.addWidget(button)

        self.difficulty_buttons[0].setChecked(True)
        # Makes Easy Mode selected by default

        set_difficulty_container.setLayout(set_difficulty_layout)

        options_layout.addWidget(set_difficulty_container)

        ### Number of Questions ###

        no_of_q_layout = QVBoxLayout()

        no_of_q_container = QGroupBox('Number of Questions')
        no_of_q_container.setToolTip('Choose the number of questions. If "All" is chosen,\n' +
                                     'each word will have a question!\n' +
                                     'CAUTION: This can make for a long quiz!')
                                     

        no_of_q_group = QButtonGroup()

        self.no_of_q_buttons = (QRadioButton('25'), QRadioButton('50'), QRadioButton('All'))

        id_num = 0

        for button in self.no_of_q_buttons:

            no_of_q_group.addButton(button)
            no_of_q_group.setId(button, id_num)

            id_num += 1

            no_of_q_layout.addWidget(button)

        self.no_of_q_buttons[0].setChecked(True)

        no_of_q_container.setLayout(no_of_q_layout)

        options_layout.addWidget(no_of_q_container)

        ### Start and Cancel Buttons ###

        button_layout = QHBoxLayout()

        start_button = QPushButton('Start')
        start_button.clicked.connect(start_quiz_window.accept)
        # When clicked, returns a 1

        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(start_quiz_window.reject)
        # When clicked returns a 0

        button_layout.addStretch(1)

        button_layout.addWidget(start_button)
        button_layout.addWidget(cancel_button)

        start_quiz_layout.addLayout(button_layout)

        ### Misc Window Settings ###

        start_quiz_window.setGeometry(400, 400, 150, 150)

        start_quiz_window.setWindowTitle('Start New Quiz')

        start_quiz_window.setLayout(start_quiz_layout)

        choice = start_quiz_window.exec_()
        # Returns a number corresponding to the user's choice.

        if choice == 1:

            return (difficulty[set_difficulty_group.checkedId()],
                    questions[no_of_q_group.checkedId()])

        else:

            return

    def about(self):

        # Tells the user about where the csv file that this quiz pulls in
        # is from along with a link to it and a little credit for myself too.

        pass

    def how_to_play(self):

        # Tells the user how to set the quiz up, the rules,
        # and what exactly this will do.

        pass
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    latin = LatinMainWindow()
    sys.exit(app.exec_())
