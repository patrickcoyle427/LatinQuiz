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

# Give player the option to export questions they got wrong so they can study

# In the help or file menu, include way to see the source of the doc

# Finish the 'About' menu

class LatinQuiz(QWidget):

    questions = []
    # Once the questions are created, they are held here for the class methods to use

    question_counter = 0
    # Controls which question is displayed.
    
    current_question = None
    # Holds the current question being asked
    
    total_correct_answers = 0
    # Total number of correct answers the player has made
    
    incorrect_answers = []
    # Holds all the incorrect answers to help the user
    # study the questions they got wrong.

    def __init__(self, latin_window):

        super().__init__()

        self.latin_window = latin_window
        # Lets LatinQuiz update the status bar of LatinMainWindow

        self.initUI()

    def initUI(self):

        ### Window Widget Layout ###

        window_layout = QVBoxLayout()

        self.setLayout(window_layout)

        self.word = QLabel('', self)
        # self.word holds current question. It is set by quiz() below
        self.word.setAlignment(Qt.AlignCenter)
                      
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

        ### Next Button ###

        next_button_layout = QHBoxLayout()

        self.next_question_button = QPushButton('Next', self)
        self.next_question_button.setMaximumWidth(100)
        self.next_question_button.setEnabled(False)
        self.next_question_button.clicked.connect(self.next_question)

        next_button_layout.addWidget(self.next_question_button)

        window_layout.addLayout(next_button_layout)

        
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

        self.questions = self.build_questions(possible_words, q_number)
        # retuns a list containing tuples with the questions
        # and their possible answers.

        # Tuples in questions are structured as:

        # ((word, definition), (answer1, answer2, answer3, answer4))
        # one of the possible answers == definitiom

        self.update_status_bar()
        # Updates the main window's status bar with 

        self.quiz()

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

        self.question_counter = 0
        self.total_correct_answers = 0

        # Resets the question counter to 0 when a new quiz starts

        return questions

    def quiz(self):

        # questions is a tuple that contains tupes. Each tuple in questions
        # contains 2 tuples arranged as:

        # ((word, its definition), (answer1, answer2, answer3, answer4))
        # one of the answers is == to the word's definition. These are
        # chosen randomly build_questions.

        # The question that is displayed is controlled by
        # question_counter

        # Runs the quiz

        # TODO:

        # Make this work

        # How it should work:

        # Counter keeps track of what quesion is loaded.
        # The len of the list of question is stored
        # displays the initial question.
        # When a question is answered, the answer is displayed.
        # after the next question button is clicked, the counter
        # ticks up and the next question is displayed.

        self.next_question_button.setEnabled(False)

        if self.question_counter < len(self.questions):

            self.current_question = self.questions[self.question_counter][0]
            # Sets the current question, used by the question label
            # to display the word, and to check the player's answer

            self.word.setText(self.current_question[0])

            labels = self.questions[self.question_counter][1]
            # labels holds the quesion answers, which is a tuple with 4 strings
            # that contains the correct answer and 3 wrong ones.

            self.a_label.setText(labels[0])
            self.b_label.setText(labels[1])
            self.c_label.setText(labels[2])
            self.d_label.setText(labels[3])

            self.a_button.setEnabled(True)
            self.b_button.setEnabled(True)
            self.c_button.setEnabled(True)
            self.d_button.setEnabled(True)

            self.update_status_bar()

            # Enables the quiz buttons

        else:

            pass

            # should display final score?

    def question_answered(self):

        # When a button is pressed, the question's answer is checked against
        # what the user selected. The incorrect buttons become red and the
        # correct answer turns green. Something alerts the user if they were
        # correct or not

        # TODO:

        # Put a green border around the correct answser!
        # Some other indicator to let the user know they are
        # right or wrong.

        self.a_button.setEnabled(False)
        self.b_button.setEnabled(False)
        self.c_button.setEnabled(False)
        self.d_button.setEnabled(False)


        sender = self.sender()
        # gets the name of the object that sent the signal to
        # question_answered, which are the buttons that the user
        # pressed.

        label_choice = {

            self.a_button: self.a_label.text(),
            self.b_button: self.b_label.text(),
            self.c_button: self.c_label.text(),
            self.d_button: self.d_label.text()

            }

        # the player's choice is used to get the text of the corresponding
        # label, which holds the definition

        self.next_question_button.setEnabled(True)

        players_choice = label_choice[sender]

        if players_choice == self.current_question[1]:
        # self.current_question[1] is the definition of the word that
        # is displayed

            self.total_correct_answers += 1

        else:

            self.incorrect_answers.append(self.current_question)

        self.update_status_bar()

    def next_question(self):

        self.question_counter += 1
        self.quiz()

    def update_status_bar(self):

        # Updates the status bar of LatinMainWindow

        self.latin_window.status_bar_message.setText(
            'Question {}/{}, {} Correct Answers'.format(
                self.question_counter + 1, len(self.questions), self.total_correct_answers))
                
if __name__ == '__main__':

    print('Please run LatinQuizMainWindow')
    