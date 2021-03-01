"""
    Copyright (C) 2021  Borgo Daniele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from random import shuffle
from generator.test.Question import Question, NEW_LINE_TOKEN, NEW_LINE_LATEX, QuestionsTextsBucket
from generator.test.TestLogger import TestLogger


class Argument:
    """
        This class represents an argument, so a group of questions with a name.
        It is also used to keep track of the points.
    """

    def __init__(self, argument_json, test_logger: TestLogger):
        self.__name = argument_json['argument_name']
        self.__questions = []
        self.__total_points = 0
        self.__optionals_points = 0
        self.__shuffle = argument_json['shuffle'] if 'shuffle' in argument_json else False

        if 'argument_text' in argument_json:
            self.__argument_text = argument_json['argument_text'].replace(
                NEW_LINE_TOKEN, NEW_LINE_LATEX)
        else:
            self.__argument_text = None

        texts_bucket = QuestionsTextsBucket()

        # Import questions and computes the argument points and the number of optional questions
        for question_text in argument_json['questions']:
            question = Question(question_text, texts_bucket)
            self.__total_points += question.points
            self.__optionals_points += question.points if question.is_optional() else 0
            self.__questions.append(question)
        self.__questions = tuple(self.__questions)
        self.__default_order = tuple(range(len(self.__questions)))

        test_logger.log_pure_questions(self.__name, texts_bucket.get_questions_texts())

    def do_you_have_arg_text(self):
        return self.__argument_text is not None

    def get_question(self, index):
        return self.__questions[index]

    def get_question_order(self):
        if not self.__shuffle:
            return self.__default_order

        to_return = list(self.__default_order)
        shuffle(to_return)
        return tuple(to_return)

    @property
    def name(self):
        return self.__name

    @property
    def argument_text(self):
        return self.__argument_text

    @property
    def number_of_questions(self):
        return len(self.__questions)

    @property
    def total_points(self):
        return self.__total_points

    @property
    def optionals_count(self):
        return self.__optionals_points
