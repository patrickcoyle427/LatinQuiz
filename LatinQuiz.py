#!/bin/usr/python3

"""
LatinQuiz.py - Game to help learn latin vocabulary.
               Displays a word and 4 choices for answers.
               Tracks the score of the user and shows how well they did

               Special thanks to Dickinson College for their
               Latin Core Vocabulary list, available at:
               http://dcc.dickinson.edu/latin-vocabulary-list

"""

import sys, random, os.path, csv

from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                             QVBoxLayout, QPushButton, QAction, QDialog,
                             QLabel, QStatusBar, QWidget, QGroupBox,
                             QLineEdit, QRadioButton, QToolTip,
                             QButtonGroup)

from PyQt5.QtCore import Qt

# TODO:

# Finish the layout of the game UI

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

        #TODO:

        # Make this work

        pass

    def start_quiz(self, options):

        # Runs the functions related to starting the quiz,
        # This includes import_words and build_questions

        frequency, q_number = options

        # Loads the options into two variables that are used by
        # each of the functions below.

        #TODO:

        # Create another function that uses the questions
        # to make the quiz functional.

        possible_words = self.import_words(frequency)
        # returns a list of words used for the quiz

        questions = self.build_questions(possible_words, q_number)
        # retuns a list containing tuples with the questions
        # and their possible answers.

        # Tuples in questions are structured as:

        # ((word, definition), (answer1, answer2, answer3, answer4))
        # one of the possible answers == definitiom

        self.quiz(questions)

    def import_words(self, frequency):

        # Imports the csv file holding the words and returns a list
        # containing the words the quiz uses.

        if os.path.exists('latin_vocabulary_list.csv'):

            with open('latin_vocabulary_list.csv', encoding='utf-8',
                      newline='') as to_load:

                latin_csv = csv.reader(to_load)

                all_words = [row for row in latin_csv]

            possible_words = [(word[0], word[1]) for word in all_words[1:]
                                    if int(word[4]) <= frequency]

            # Builds a list that contains tuples for word + definition pairs, based
            # on the difficulty option (aka the word frequency) when the user is starting
            # their quiz.

            # word[0] is the actual word
            # word[1] is the definition
            # word[4] is the frequency rank. It is stored as a str,
            # so it is converted to int

            return possible_words

        else:

            pass
            #TODO:

            # Put an error message if file not found

    def build_questions(self, possible_words, q_number):

        # Creates and returns a list containing tuples of a word, its correct
        # answer and three random incorrect answers.

        questions = []

        random.shuffle(possible_words)
        # randomizes the list of words so the order changes each time the
        # game is played.

        for word_and_def in possible_words:

            chosen_words = random.sample(possible_words, 3)
            # Chooses 3 words to use as wrong answers.

            while word_and_def in chosen_words:

                chosen_words = random.sample(possible_words, 3)
                # If random.sample happens to select the current word,
                # the wrong answers are redrawn.

            chosen_words.append(word_and_def)
            # Adds the current word in the for loop to the chosen_words list

            random.shuffle(chosen_words)

            question_answers = []

            for word_pair in chosen_words:

                question_answers.append(word_pair[1])
                # Appends just the word definitions to the questions_answered
                # list. These will appear as the possible question choices

            questions.append((word_and_def, tuple(question_answers)))
            # Appends the word and it's definition, followed by
            # The list of possible answers converted to a tuple.

            if len(questions) == q_number:

                # Breaks this for loop when it either hits the q_number,
                # or reaches the end of the possible_words list

                break

        return questions

    def quiz(self, questions):

        # Runs the quiz

        # TODO:

        # Make this work

        # How it should work:

        # Counter keeps track of what quesion is loaded.
        # The len of the list of question is stored
        # displays the initial question.
        # When a question is answered, the answer is displayed.
        # after the next question button is clicked, the counter
        # ticks up and the next question is displayed

        self.a_button.setEnabled(True)
        self.b_button.setEnabled(True)
        self.c_button.setEnabled(True)
        self.d_button.setEnabled(True)

        # Enables the quiz buttons

class LatinMainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.Quiz = LatinQuiz()
        # Creates an instance of LatinQuiz()

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
        # Container for the last choosen settings, used for restarting a quiz

        self.setGeometry(300, 300, 300, 400)

        self.setWindowTitle('Latin Quiz')

        self.show()

    def start_new_quiz(self):

        options = self.start_quiz_options()

        # Opens a window to adjust game settings

        if options != None:

            self.Quiz.start_quiz(options)

    def start_quiz_options(self):

        # Builds the window that displays when a new quiz begins

        ### Initial Setup ###

        start_quiz_window = QDialog(None, Qt.WindowCloseButtonHint)
        # Qt.WindowCloseButtonHint Prevents the ? button from appearing
        # in the dialog window

        options_layout = QHBoxLayout()
        # Holds the radio button options for starting a game.

        difficulty = { 0: 50,
                       1: 100,
                       2: 250,
                       3: 500,
                       4: 1000 }

        questions = { 0: 25,
                      1: 50,
                      2: 1000}

        # These dicts hold the what each option below corresponds to
        # The difficulty is how many words will be chosen for questions
        # the questions will be how many questions the quiz contains

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

        start_quiz_window.setGeometry(300, 300, 150, 150)

        start_quiz_window.setWindowTitle('Start New Quiz')

        start_quiz_window.setLayout(start_quiz_layout)

        choice = start_quiz_window.exec_()
        # Returns a number corresponding to the user's choice.
        # 1 = Accept (Hit the ok button)
        # 0 = Reject (Hit the cancel button)

        if choice == 1:

            return (difficulty[set_difficulty_group.checkedId()],
                    questions[no_of_q_group.checkedId()])

        else:

            return

    def about(self):

        # TODO:
        
        # Credits Dickinson College for their amazing
        # .csv file that this is built on.

        # plus a little credit screen for me.

        pass

    def how_to_play(self):

        #TODO:

        # Tells the user how to set the quiz up, the rules,
        # and what exactly this will do.

        pass
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    latin = LatinMainWindow()
    sys.exit(app.exec_())
