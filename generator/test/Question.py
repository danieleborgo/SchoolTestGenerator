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

from random import randint, uniform, choice
from generator import sentences
from generator.enums import QuestionType

# This is the token that will represent a random value in the JSON text representation
RANDOM_VALUE_TOKEN = '%n'

# This is how break line characters are represented in the JSON text
NEW_LINE_TOKEN = '\n'

# This is how break lines are in Latex
NEW_LINE_LATEX = '\\\\ '


class Question:
    """
        This class contains a single question with all its related data:
        - type
        - points
        - optionality
        - text with all the random values generator, the objects able to handle random generation
    """

    def __init__(self, question_json, text_bucket):
        self.__type = QuestionType.translate_type(question_json['type'])
        self.__points = question_json['points'] if 'points' in question_json else 1
        self.__is_optional = question_json['optional'] if 'optional' in question_json else False
        self.__extract_standard_question(question_json)

        text_bucket.add(self.__text)

        if self.__type == QuestionType.NO_SPACED_QUESTION:
            self.__print_question = self.__print_no_space_question_ret_randoms
            return

        if self.__type == QuestionType.SPACED_QUESTION:
            self.__appendix = NEW_LINE_LATEX * (1 + question_json['rows'])
            self.__print_question = self.__print_spaced_question_ret_randoms
            return

    def __extract_standard_question(self, question_json):
        """
            This method extracts all the necessary parameters for a simple standard question.
            It is composed by a text that could have some random values inside of it.
        """

        # Text extraction
        if isinstance(question_json['text'], list):
            self.__text = ''.join(iter(question_json['text']))
        else:
            self.__text = question_json['text']
        self.__text = self.__text.replace(NEW_LINE_TOKEN, NEW_LINE_LATEX)

        # Random values handlers creation
        n_occurrences = self.__text.count(RANDOM_VALUE_TOKEN)
        if 'values' in question_json:
            self.__random_handlers = self.__extract_random_handlers(
                question_json['values'],
                n_occurrences
            )
        else:
            if n_occurrences > 0:
                raise Exception(
                    "There are some tokens in the string but no random values were provided"
                )
            self.__random_handlers = []

    def __extract_random_handlers(self, values_json, expected_n_values):
        """
            This method extracts the data related on how generate randoms values and creates
            proper objects to handle them.
        """

        random_handlers = []

        for random_json in values_json:
            random_handlers.append(RandomHandler(random_json))

        if expected_n_values != len(random_handlers):
            raise Exception(
                "Warning: the number of specified random generator doesn't coincide with the " +
                RANDOM_VALUE_TOKEN + " found in:" + self.__text
            )

        return random_handlers

    @staticmethod
    def __substitute_random_values_returning(text, random_handlers):
        random_nums = []
        for i in range(len(random_handlers)):
            random_nums.insert(i, random_handlers[i].get_random())
            text = text.replace(RANDOM_VALUE_TOKEN, str(random_nums[i]), 1)
        return text, random_nums

    def is_optional(self):
        return self.__is_optional

    def __print_no_space_question_ret_randoms(self, has_optional_questions, appendix=''):
        text, used_randoms = self.__substitute_random_values_returning(
            self.__text,
            self.__random_handlers
        )

        to_print = '(' + str(self.__points) + \
                   (', ' + sentences.OTHERS.OPTIONAL
                    if self.__is_optional and has_optional_questions else '') \
                   + ') ' + text + appendix

        return to_print, used_randoms

    def __print_spaced_question_ret_randoms(self, has_optional_questions):
        return self.__print_no_space_question_ret_randoms(has_optional_questions, self.__appendix)

    def print_question_ret_randoms(self, has_optional_questions):
        return self.__print_question(has_optional_questions)

    @property
    def points(self):
        return self.__points


class QuestionsTextsBucket:
    def __init__(self):
        self.__bucket = []

    def add(self, text: str):
        self.__bucket.append(text)

    def get_questions_texts(self):
        return tuple(self.__bucket)


class RandomHandler:
    """
        This class handles the random number generation for a single token.
        It contains all its configuration parameters and supports three configurations:
        - int: pick an integer element from an interval;
        - float: pick a float value in an interval with the specified precision;
        - set: pick an element from a set.
        It can be easily extended to support more.
        Using more precise parent-son paradigm would have complicated uselessly the structure.
    """

    def __init__(self, random_json):
        rand_type = random_json['type']

        if 'set'.__eq__(rand_type):
            self.__set = tuple(random_json['set'])
            self.__generate_random = self.__get_from_set
            return

        if 'float'.__eq__(rand_type):
            self.__import_min_max(random_json)
            self.__size = 2
            self.__generate_random = self.__get_limited_float
            return

        if 'int'.__eq__(rand_type):
            self.__import_min_max(random_json)
            self.__generate_random = self.__get_limited_int
            return

        raise Exception("Unknown random value type: " + rand_type)

    def __import_min_max(self, random_json):
        self.__start = random_json['min']
        self.__end = random_json['max']

    def __get_from_set(self):
        return choice(self.__set)

    def __get_limited_int(self):
        return randint(self.__start, self.__end)

    def __get_limited_float(self):
        return round(uniform(self.__start, self.__end), self.__size)

    def get_random(self):
        return self.__generate_random()
