#!/bin/usr/python3

"""
LatinQuizWidget.py - The meat of LatinQuiz. Creates and displays questions,
                     Keeps track of questions answers and controls what is
                     shown in LatinQuizMainWindow.

                     This is imported into LatinQuizMain window and is not
                     meant to be run by itself.

"""

# TODO:

# Finish the layout of the game UI

#   In questions_answered:
#       Add some way to show which quesion is right and which is wrong,
#       as well as some indication of which question the user chose.
#       The idea so far is the correct answer will have a green border
#       and should say correct answer as well for color blind people.
#       if the incorrect answer is chosen that will have a red border and
#       say wrong answer.
#

# QDialog in quiz to show your final score and give
# player the option to export questions they got wrong
# so they can study. QUIZ NEEDS A WAY TO KNOW IT'S DONE!

# Keyboard shortcuts for answering questions.
# should be able to press A, B, C, D, or 1 2 3 4 for question answers
# and enter to advance to the next question.

import sys, random, os.path, csv, datetime

from PyQt5.QtWidgets import (QApplication, QHBoxLayout,
                             QVBoxLayout, QPushButton, QDialog,
                             QLabel, QWidget, QGroupBox,
                             QLineEdit, QRadioButton, QToolTip,
                             QButtonGroup, QMessageBox, QCheckBox)

from PyQt5.QtCore import Qt

class LatinQuiz(QWidget):

    questions = []
    # Once the questions are created, they are held here for the class methods to use

    question_counter = 0
    # Controls which question is displayed.
    
    current_question = None
    # Holds the current question being asked. These questions are tuples,
    # with current_question[0] being the vocab word
    # and current_question[1] being the definition of that word.
    
    total_correct_answers = 0
    # Total number of correct answers the player has made
    
    incorrect_answers = []
    # Holds all the incorrect answers to help the user study the questions they got wrong.
    # All incorrect answers are from current_question, as such incorrect_answers
    # stores tuples that follow the same format as current_question, with [0] being
    # the word and [1] being the definition
    
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
        self.a_button.setShortcut('A')
        self.a_button.setEnabled(False)
        self.a_button.clicked.connect(self.question_answered)
        
        self.b_button = QPushButton('B', self)
        self.b_button.setMaximumWidth(50)
        self.b_button.setShortcut('B')
        self.b_button.setEnabled(False)
        self.b_button.clicked.connect(self.question_answered)
        
        self.c_button = QPushButton('C', self)
        self.c_button.setMaximumWidth(50)
        self.c_button.setShortcut('C')
        self.c_button.setEnabled(False)
        self.c_button.clicked.connect(self.question_answered)
        
        self.d_button = QPushButton('D', self)
        self.d_button.setMaximumWidth(50)
        self.d_button.setShortcut('D')
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
        self.next_question_button.setShortcut('N')
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

        possible_words = self.import_words(frequency)
        # returns a list of words used for the quiz

        if possible_words != None:

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

            self.import_words_error()

            return None

    def import_words_error(self):

        # Holds the error message which is displayed if no word file is found

        words_not_found = QMessageBox()

        words_not_found.setIcon(QMessageBox.Critical)

        error_message = '''
                        Word file not found! Please make sure a file named
                        latin_vocabulary_list.csv is present in the same file
                        as latinquiz.py
                        '''
    

        words_not_found.setText(error_message)

        words_not_found.setWindowTitle('Words Not Found')
    
        words_not_found.exec_()


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

            self.finish_quiz()

            # should display final score?
            # Change the text on the next button to end quiz?

    def question_answered(self):

        # When a button is pressed, the question's answer is checked against
        # what the user selected. The incorrect buttons become red and the
        # correct answer turns green. Something alerts the user if they were
        # correct or not

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
        self.next_question_button.setFocus(True)

        players_choice = label_choice[sender]

        if players_choice == self.current_question[1]:
        # self.current_question[1] is the definition of the word that
        # is displayed, and is stored as an object variable

            self.total_correct_answers += 1

        else:

            self.incorrect_answers.append(self.current_question)

        self.show_answers(self.current_question[1], players_choice)
        # Changes the border around the correct and incorrect answers

        self.update_status_bar()

    def next_question(self):

        # Sets up the next question, and removes the borders
        # from correct/incorrect answers.

        labels = (
                self.a_label,
                self.b_label,
                self.c_label,
                self.d_label
            )

        for label in labels:

            label.setStyleSheet('')

        self.question_counter += 1
        
        self.quiz()

    def update_status_bar(self):

        # Updates the status bar of LatinMainWindow

        self.latin_window.status_bar_message.setText(
            'Question {}/{}, {} Correct Answers'.format(
                self.question_counter + 1, len(self.questions), self.total_correct_answers))

    def show_answers(self, correct, players_choice):

        # Places a green border around the correct answer, and if the user
        # chose an incorrect answer, a red border is placed around it

        labels = (
                self.a_label,
                self.b_label,
                self.c_label,
                self.d_label
            )

        for label in labels:

            if label.text() == correct:

                label.setStyleSheet('border: 3px solid green')

            elif players_choice == label.text() and players_choice != correct:

                label.setStyleSheet('border: 3px solid red')

    def finish_quiz(self):

        # At end of the quiz, this runs to let the user know it is finished,
        # and to give them options to start again with the same or new options,
        # export the words and definitions the user got wrong, and to show
        # the user's final score.

        # Export incorrect words should be a check box.

        finish_quiz = QDialog(None, Qt.WindowCloseButtonHint)
        # Qt.WindowCloseButtonHint Prevents the ? button from appearing
        # in the dialog window
        # Need to prevent the close button as well.

        finish_quiz_layout = QVBoxLayout()

        ### Final Score Display ###

        num_grade = self.total_correct_answers / len(self.questions)

        letter_grade = self.get_letter_grade(num_grade)

        score_message = 'Your final score is: {} / {} ({}%)'.format(
            self.total_correct_answers, len(self.questions), round(num_grade * 100, 2))

        score_display = QLabel(score_message)
                               
        finish_quiz_layout.addWidget(score_message)
                                                                    
        letter_message = Qlabel('Your grade is', letter_grade)
        finish_quiz_layout.addWidget(letter_message)

        export_check_box = QCheckBox('Export Incorrect Answers', self)
        export_check_box.setChecked(True)
        finish_quiz_layout.addWidget(export_check_box)

        ### Buttons ###
        
        # The following buttons use .done(int) instead of .accept or
        # .reject.
        # This is done for clarity, since I want these buttons to return
        # 0, 1, and 2 respectively even though accept and reject will
        # return 0 and 1.

        button_layout = QHBoxLayout()

        restart_button = QPushButton('Restart This Quiz')
        restart_button.clicked.connect(finish_quiz.done(1))
        # Connect this to something that restarts the quiz

        new_quiz_button = QPushButton('New Quiz')
        new_quiz_button.clicked.connect(finish_quiz.done(2))
        button_layout.addWidget(new_quiz_button)

        close_button = QPushButton('Close')
        close_button.clicked.connect(finish_quiz.done(0))
        
        button_layout.addWidget(close_button)

        # Save for if statement later
        # self.latin_window.start_new_quiz
        
        ### Misc Window Settings ###

        finish_quiz.setGeometry(300, 500, 150, 150)

        finish_quiz.setWindowTitle('Final Score')

        finish_quiz.setLayout(finish_quiz_layout)

        choice = final_score.exec_()
        # Returns a number based on the user's choice.

        if export_check_box.isChecked() == True:

            # Exports the wrong answers to a text file
            # to help the player study

            today = 'wrong_latin_vocab_answers-' + str(datetime.date.today()) + '.txt'
            # Creates the filename for the incorrect answers

            with open(today, mode='a') as inc:

                if os.path.getsize(today) > 0:

                    inc.write('\n')
                    # inserts a blank line into the output if the incorrect answers
                    # file already has anything written in it.

                for incorrect in incorrect_answers:

                    # all items in incorrect_answers are stored as tuples
                    # that need to be unpacked before writing

                    inc.write(incorrect[0] + ' - ' + incorrect[1])

        # The followin lines clear the held info from the previous quiz

        del self.questions[:]

        self.question_counter = 0

        self.total_correct_answers = 0

        del self.incorrect_answers[:]
        
        if choice == 0:

            # Closes this dialog and does no action

            return

        if choice == 1:

            # Restarts the quiz with the current settings

            pass

        else:

            pass

    def get_letter_grade(self, num_grade):

        # Emulates the letter grades given by West Chester University.
        # Grades pulled from: http://catalog.wcupa.edu/undergraduate/academic-policies-procedures/grading-information/

        letter_grade = ''

        if num_grade > .92:

            letter_grade = 'A+'

        elif .89 < num_grade < .93:

            letter_grade = 'A-'

        elif .86 < num_grade < .9:

            letter_grade = 'B+'

        elif .82 < num_grade < .87:

            letter_grade = 'B'

        elif .79 < num_grade < .83:

            letter_grade = 'B-'

        elif .76 < num_grade < .8:

            letter_grade = 'C+'

        elif .72 < num_grade < .77:

            letter_grade = 'C'

        elif .69 < num_grade < .73:

            letter_grade = 'C-'

        elif .66 < num_grade < .7:

            letter_grade = 'D+'

        elif .64 < num_grade < .67:

            letter_grade = 'D'

        elif .59 < num_grade < .65:

            letter_grade = 'D-'

        else:

            letter_grade = 'F'

        return letter_grade

        

                
if __name__ == '__main__':

    print('Please run LatinQuizMainWindow')
    
