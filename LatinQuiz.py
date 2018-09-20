#!/bin/usr/python3

"""
LatinQuiz.py - Game to help learn latin vocabulary.
               Displays a word and 4 choices for answers.
               Tracks the score of the user and shows how well they did

               Special thanks to Dickinson College for their
               Latin Core Vocabulary list, available at:
               http://dcc.dickinson.edu/latin-vocabulary-list

"""

import sys, random, os.path, csv, datetime

from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                             QVBoxLayout, QPushButton, QAction, QDialog,
                             QLabel, QStatusBar, QWidget, QGroupBox,
                             QLineEdit, QRadioButton, QToolTip,
                             QButtonGroup, QMessageBox, QCheckBox)

from PyQt5.QtCore import Qt

class LatinMainWindow(QMainWindow):

# TO DO:

# Finish the 'About' menu

# Finish the 'How To Play' menu

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

    previous_options = None
    # Holds the user's selected options for restarting the game

    def __init__(self):

        super().__init__()

        self.Quiz = LatinQuiz(self)
        # Creates an instance of LatinQuiz(), the cental widget
        # passes it the LatinMainWindow object reference to let the
        # QWidget buttons interact with the main window methods.

        self.initUI()

    def initUI(self):

        ### Menu Bar ###

        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')

        new_quiz = QAction('&New Quiz', self)
        new_quiz.setShortcut('Ctrl+N')
        new_quiz.triggered.connect(self.start_new_quiz)

        self.restart = QAction('&Restart', self)
        self.restart.setShortcut('Ctrl+r')
        self.restart.triggered.connect(self.restart_quiz)
        self.restart.setEnabled(False)
        # enabled once self.previous options are not None
        
        exit_game = QAction('&Exit', self)
        exit_game.setShortcut('Ctrl+Q')
        exit_game.triggered.connect(self.close)

        file_menu.addAction(new_quiz)
        file_menu.addAction(self.restart)
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

        self.setGeometry(300, 300, 800, 400)

        self.setWindowTitle('Latin Quiz')

        self.show()

    def start_new_quiz(self):

        # Collects the options and starts the Latin quiz

        options = self.start_quiz_options()

        # Opens a window to adjust game settings

        if options != None:

            self.previous_options = options[:]

            self.restart.setEnabled(True)
            
            self.start_quiz(options)

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

        about = QMessageBox()

        message_text = '''
        Software written by Patrick Coyle

        LatinWord CSV file obtained from Dickinson College at:
        http://dcc.dickinson.edu/latin-vocabulary-list

        Letter grades are those used at West Chester University.
        Obtained from:
        http://catalog.wcupa.edu/undergraduate/academic-policies-procedures/
        grading-information/

        Thanks for playing :)
        '''

        about.setText(message_text)

        about.setWindowTitle('About')

        about.exec_()

    def how_to_play(self):

        # Tells the user how to set the quiz up, the rules,
        # and what exactly this will do.

        howto = QMessageBox()

        message_text = '''
        First start a new game by selecting new game from the file
        menu or pressing CTRL + N.

        Then select your difficulty! The harder you select, the
        more infrequenly used the words being asked will be!

        You can also chose the number of questions! 25, 50 or
        ALL! All questions may take awhile.

        Your goal is to answer as many questions correctly
        as possible!

        You can click the buttons to chose your answers,
        or by pressing the letter on the button.

        You can also go to the next question by pressing the
        space bar.

        Once the quiz is complete you will be shown your score
        and the letter grade you would have received on a test.
        You can export the questions you got wrong to help you
        study!

        Thanks for playing and happy studying! :)
        '''

        howto.setText(message_text)

        howto.setWindowTitle('How To Play')

        howto.exec_()

    def start_quiz(self, options):

        # options: a tuple, the first value is the frequency, a lower frequency means less
        # common words are used in the quiz.
        # The second value is the q_number aka number of questions the quiz will have

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

            self.quiz()

    def import_words(self, frequency):

        # frequency: an int containing the frequeny value. A lower frequency means less
        # common words are used in the quiz.

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

        # possible_words: a list containing words used in the quiz.
        # q_number: an int, used to determine the number of questions

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

        # questions is a tuple that contains tupes. Each tuple in questions
        # contains 2 tuples arranged as:

        # ((word, its definition), (answer1, answer2, answer3, answer4))
        # one of the answers is == to the word's definition. These are
        # chosen randomly build_questions.

        return questions

    def quiz(self):

        # The question that is displayed is controlled by question_counter

        # Runs the quiz

        self.Quiz.next_question_button.setEnabled(False)

        if self.question_counter < len(self.questions):

            self.current_question = self.questions[self.question_counter][0]
            # Sets the current question, used by the question label
            # to display the word, and to check the player's answer

            build_style_sheet = 'font-weight:bold; font-size:{}px;'.format(
                self.calculate_font_size(self.current_question[0]))
    
            # calculate_font_size sets the style sheet for the current question
            # based on the lendth of the string.

            self.Quiz.word.setStyleSheet(build_style_sheet)

            self.Quiz.word.setText(self.current_question[0])

            labels = self.questions[self.question_counter][1]
            # labels holds the quesion answers, which is a tuple with 4 strings
            # that contains the correct answer and 3 wrong ones.

            self.Quiz.a_label.setText(labels[0])
            self.Quiz.b_label.setText(labels[1])
            self.Quiz.c_label.setText(labels[2])
            self.Quiz.d_label.setText(labels[3])

            self.Quiz.a_button.setEnabled(True)
            self.Quiz.b_button.setEnabled(True)
            self.Quiz.c_button.setEnabled(True)
            self.Quiz.d_button.setEnabled(True)

            self.update_status_bar()

            # Enables the quiz buttons

        else:

            self.finish_quiz()

    def question_answered(self):

        # When a button is pressed, the question's answer is checked against
        # what the user selected. The incorrect buttons become red and the
        # correct answer turns green. Something alerts the user if they were
        # correct or not

        self.Quiz.a_button.setEnabled(False)
        self.Quiz.b_button.setEnabled(False)
        self.Quiz.c_button.setEnabled(False)
        self.Quiz.d_button.setEnabled(False)

        sender = self.sender()
        # gets the name of the object that sent the signal to
        # question_answered, which are the buttons that the user
        # pressed.

        label_choice = {

            self.Quiz.a_button: self.Quiz.a_label.text(),
            self.Quiz.b_button: self.Quiz.b_label.text(),
            self.Quiz.c_button: self.Quiz.c_label.text(),
            self.Quiz.d_button: self.Quiz.d_label.text()

            }

        # the player's choice is used to get the text of the corresponding
        # label, which holds the definition

        self.Quiz.next_question_button.setEnabled(True)
        self.Quiz.next_question_button.setFocus(True)

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
                self.Quiz.a_label,
                self.Quiz.b_label,
                self.Quiz.c_label,
                self.Quiz.d_label
            )

        for label in labels:

            label.setStyleSheet('')

        self.question_counter += 1
        
        self.quiz()

    def update_status_bar(self):

        # Updates the status bar for the current question.

        self.status_bar_message.setText(
            'Question {}/{}, {} Correct Answers'.format(
                self.question_counter + 1, len(self.questions), self.total_correct_answers))

    def show_answers(self, correct, players_choice):

        # Places a green border around the correct answer, and if the user
        # chose an incorrect answer, a red border is placed around it

        labels = (
                self.Quiz.a_label,
                self.Quiz.b_label,
                self.Quiz.c_label,
                self.Quiz.d_label
            )

        for label in labels:

            if label.text() == correct:

                label.setStyleSheet('border: 3px solid green; font-weight:bold;')

            elif players_choice == label.text() and players_choice != correct:

                label.setStyleSheet('border: 3px solid red; font-weight:bold;')

    def finish_quiz(self):

        # At end of the quiz, this runs to let the user know it is finished,
        # and to give them options to start again with the same or new options,
        # export the words and definitions the user got wrong, and to show
        # the user's final score.

        # Export incorrect words should be a check box.

        finish_quiz = QDialog(None, Qt.WindowCloseButtonHint)
        # Qt.WindowCloseButtonHint Prevents the ? button from appearing
        # in the dialog window

        finish_quiz_layout = QVBoxLayout()
        finish_quiz_layout.setAlignment(Qt.AlignCenter)

        ### Final Score Display ###

        num_grade = self.total_correct_answers / len(self.questions)

        letter_grade = self.get_letter_grade(num_grade)

        score_message = 'Your final score is: {} / {} ({}%)'.format(
            self.total_correct_answers, len(self.questions), round(num_grade * 100, 2))

        score_display = QLabel(score_message)
        score_display.setAlignment(Qt.AlignCenter)
        score_display.setStyleSheet('font-size:18px;')
                               
        finish_quiz_layout.addWidget(score_display)

        letter_message = 'Your grade is: {}'.format(letter_grade)
                                                                    
        letter_grade_display = QLabel(letter_message)
        letter_grade_display.setStyleSheet('font-size:18px;')
        letter_grade_display.setAlignment(Qt.AlignCenter)
        
        finish_quiz_layout.addWidget(letter_grade_display)

        export_check_box = QCheckBox('Export Incorrect Answers', self)
        export_check_box.setStyleSheet('margin-left:50%; margin-right:50%;')
        export_check_box.setChecked(True)
        finish_quiz_layout.addWidget(export_check_box)
 
        ### Buttons ###
        
        # The following buttons use .done(int) instead of .accept or
        # .reject.
        # This is done for clarity, since I want these buttons to return
        # 0, 1, and 2 respectively even though accept and reject will
        # return 0 and 1.

        # Option 0 does no action
        # Option 1 restarts the quiz,
        # Option 2 lets the user pick new options and starts the quiz again

        button_layout = QHBoxLayout()

        restart_button = QPushButton('Restart This Quiz')
        restart_button.clicked.connect(lambda: finish_quiz.done(1))
        button_layout.addWidget(restart_button)

        # lambda used to pass a method with an argument to
        # QPushButton.clicked.connect

        new_quiz_button = QPushButton('New Quiz')
        new_quiz_button.clicked.connect(lambda: finish_quiz.done(2))
        button_layout.addWidget(new_quiz_button)

        close_button = QPushButton('Close')
        close_button.clicked.connect(lambda: finish_quiz.done(0))
        button_layout.addWidget(close_button)

        finish_quiz_layout.addLayout(button_layout)
        
        ### Misc Window Settings ###

        finish_quiz.setGeometry(400, 400, 200, 150)

        finish_quiz.setWindowTitle('Final Score')

        finish_quiz.setLayout(finish_quiz_layout)

        choice = finish_quiz.exec_()
        # Returns a number based on the user's choice.

        if export_check_box.isChecked() == True:

            # Exports the wrong answers to a text file to help the plyer study

            today = 'wrong_latin_vocab_answers-' + str(datetime.date.today()) + '.txt'
            # Creates the filename for the incorrect answers

            with open(today, mode='a', encoding='utf-8') as inc:

                if os.path.getsize(today) > 0:

                    inc.write('\n')
                    # inserts a blank line into the output if the incorrect answers
                    # file already has anything written in it.

                for incorrect in self.incorrect_answers:

                    # all items in incorrect_answers are stored as tuples
                    # that need to be unpacked before writing

                    inc.write(incorrect[0] + ' - ' + incorrect[1] + '\n')

                total_wrong = len(self.questions) - self.total_correct_answers

                inc.write('Incorrect Answers: {}\n'.format(total_wrong))

        # The following lines clear the held info from the previous quiz
        
        self.incorrect_answers.clear()

        self.question_counter = 0

        self.total_correct_answers = 0
        
        if choice == 0:

            # Closes this dialog and does no action

            return

        if choice == 1:

            # Restarts the quiz with the same options

            self.update_status_bar()

            self.restart_quiz()

        else:

            # restarts the quiz with the new option dialog

            self.update_status_bar()

            self.start_new_quiz()

    def restart_quiz(self):

        # restarts the quiz with the last used options. Used by the restart quiz menu
        # option and the restart quiz option at the end of the quiz.

        self.start_quiz(self.previous_options)

    def get_letter_grade(self, num_grade):

        # Emulates the letter grades given by West Chester University.
        # Grades pulled from:
        # http://catalog.wcupa.edu/undergraduate/academic-policies-procedures/grading-information/

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

    def calculate_font_size(self, current_q):

        lencq = len(current_q)

        # current_q is a string. It is the current question being asked.

        # takes the len of current_q and uses that to determine the size of
        # the font for the displayed question

        if lencq < 21:

            return '50'

        elif 21 < lencq < 41:

            return '25'

        else:

            return '18'

class LatinQuiz(QWidget):

    def __init__(self, main_window):

        # main_window is a reference to LatinMainWindow, allowing the widget
        # to interact with certain methods of the main window.

        super().__init__()

        self.main_window = main_window

        self.initUI()

    def initUI(self):

        ### Window Widget Layout ###

        window_layout = QVBoxLayout()

        self.setLayout(window_layout)

        self.word = QLabel('', self)
        # self.word holds current question. It is set by LatinMainWindow.quiz()
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
        self.a_button.clicked.connect(self.main_window.question_answered)
        
        self.b_button = QPushButton('B', self)
        self.b_button.setMaximumWidth(50)
        self.b_button.setShortcut('B')
        self.b_button.setEnabled(False)
        self.b_button.clicked.connect(self.main_window.question_answered)
        
        self.c_button = QPushButton('C', self)
        self.c_button.setMaximumWidth(50)
        self.c_button.setShortcut('C')
        self.c_button.setEnabled(False)
        self.c_button.clicked.connect(self.main_window.question_answered)
        
        self.d_button = QPushButton('D', self)
        self.d_button.setMaximumWidth(50)
        self.d_button.setShortcut('D')
        self.d_button.setEnabled(False)
        self.d_button.clicked.connect(self.main_window.question_answered)

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
        self.next_question_button.clicked.connect(self.main_window.next_question)

        next_button_layout.addWidget(self.next_question_button)

        window_layout.addLayout(next_button_layout)
        
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    latin = LatinMainWindow()
    sys.exit(app.exec_())

