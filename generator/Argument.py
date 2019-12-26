from random import randint, uniform, choice
from pylatex import NoEscape
from generator.enums import QuestionType, StudentType

# This is the token that will represent a random value in the JSON text representation
RANDOM_NUMBER_TOKEN = '%n'

# This is how break line characters are represented in the JSON text
NEW_LINE_TOKEN = '\n'

# This is how break lines are in Latex
NEW_LINE_LATEX = '\\\\ '


class Argument:
    """
        This class represents an argument, so a group of questions with a name.
        It is also used to keep track of the points.
    """

    def __init__(self, argument_json):
        self.__name = argument_json['argument_name']
        self.__questions = []
        self.__total_points = 0
        self.__optionals_points = 0

        # Import questions and computes the argument points and the number of optional questions
        for i in range(len(argument_json['questions'])):
            question = Question(argument_json['questions'][i])
            self.__total_points += question.get_points()
            self.__optionals_points += question.get_points() if question.is_optional() else 0
            self.__questions.append(question)
        self.__questions = tuple(self.__questions)

    def get_name(self):
        return self.__name

    def get_number_of_questions(self):
        return len(self.__questions)

    def get_questions(self):
        return self.__questions

    def get_points(self):
        return self.__total_points

    def get_optionals_count(self):
        return self.__optionals_points


class Question:
    """
        This class contains a single question with all its related data:
        - type
        - points
        - optionality
        - text with all the random values generator, the objects able to handle random generation
    """

    def __init__(self, question_json):
        self.__type = QuestionType.translate_type(question_json['type'])
        self.__points = question_json['points'] if 'points' in question_json else 1
        self.__is_optional = question_json['optional'] if 'optional' in question_json else False

        if self.__type == QuestionType.NO_SPACED_QUESTION:
            self.__extract_standard_question(question_json)
            self.__print_question = self.__print_no_space_question_ret_randoms
            return

        if self.__type == QuestionType.SPACED_QUESTION:
            self.__extract_standard_question(question_json)
            self.__appendix = NEW_LINE_LATEX * (1 + question_json['rows'])
            self.__print_question = self.__print_spaced_question_ret_randoms
            return

    def __extract_standard_question(self, question_json):
        """
            This method extracts all the necessary parameters for a simple standard question.
            It is composed by a text that could have some random values inside of it.
        """

        # Text extraction
        if 'array' in question_json and question_json['array']:
            self.__text = ''.join(iter(question_json['text']))
        else:
            self.__text = question_json['text']
        self.__text = self.__text.replace(NEW_LINE_TOKEN, NEW_LINE_LATEX)

        # Random values handlers creation
        n_occurrences = self.__text.count(RANDOM_NUMBER_TOKEN)
        if 'values' in question_json:
            self.__random_handlers = self.__extract_random_handlers(question_json['values'], n_occurrences)
        else:
            if n_occurrences > 0:
                raise Exception("There are some tokens in the string but no random values were provided")
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
            raise Exception("Warning: the number of specified random generator doesn't coincide with the " +
                            RANDOM_NUMBER_TOKEN + " found in:" + self.__text)

        return random_handlers

    @staticmethod
    def __substitute_random_values_returning(text, random_handlers):
        random_nums = []
        for i in range(len(random_handlers)):
            random_nums.insert(i, random_handlers[i].get_random())
            text = text.replace(RANDOM_NUMBER_TOKEN, str(random_nums[i]), 1)
        return [text, random_nums]

    def get_points(self):
        return self.__points

    def is_optional(self):
        return self.__is_optional

    def __print_no_space_question_ret_randoms(self, enum, student_type, appendix=''):
        [text, used_randoms] = self.__substitute_random_values_returning(self.__text, self.__random_handlers)
        to_print = '(' + str(self.__points) + \
                   (', facoltativa' if self.__is_optional and student_type == StudentType.OPTIONAL_QUESTIONS else '') \
                   + ') ' + text + appendix
        enum.add_item(NoEscape(to_print))

        return used_randoms

    def __print_spaced_question_ret_randoms(self, enum, student_type):
        return self.__print_no_space_question_ret_randoms(enum, student_type, self.__appendix)

    def print_question_ret_randoms(self, enum, student_type):
        return self.__print_question(enum, student_type)


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
            self.__random_generator = self.__get_from_set
            return

        if 'float'.__eq__(rand_type):
            self.__import_min_max(random_json)
            self.__size = 2
            self.__random_generator = self.__get_limited_float
            return

        if 'int'.__eq__(rand_type):
            self.__import_min_max(random_json)
            self.__random_generator = self.__get_limited_int
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
        return self.__random_generator()
