from generator.enums import QuestionType
from random import randint, uniform, choice

RANDOM_NUMBER_TOKEN = '%n'
NEW_LINE_TOKEN = '\n'
NEW_LINE_LATEX = '\\\\ '


class Argument:
    """
        This class is supposed to represent an argument, so a group of
        questions.
    """

    def __init__(self, argument_json):
        self.__name = argument_json['argument_name']
        self.__questions = []
        self.__points = 0
        self.__optionals_count = 0

        for i in range(len(argument_json['questions'])):
            question = Question(argument_json['questions'][i])
            self.__points += question.get_points()
            self.__optionals_count += 1 if question.is_optional() else 0
            self.__questions.append(question)
        self.__questions = tuple(self.__questions)

    def get_name(self):
        return self.__name

    def get_number_of_questions(self):
        return len(self.__questions)

    def get_questions(self):
        return self.__questions

    def get_points(self):
        return self.__points

    def get_optionals_count(self):
        return self.__optionals_count


class Question:
    """
        This class contains a single question with all the related data.
    """

    def __init__(self, question_json):
        self.__type = QuestionType.translate_type(question_json['type'])
        self.__points = question_json['points'] if 'points' in question_json else 1
        self.__optional = question_json['optional'] if 'optional' in question_json else False

        if 'array' in question_json and question_json['array']:
            self.__text = ''.join(iter(question_json['text']))
        else:
            self.__text = question_json['text']

        self.__text = self.__text.replace(NEW_LINE_TOKEN, NEW_LINE_LATEX)

        self.__random_handlers = []
        n_occurrences = self.__text.count(RANDOM_NUMBER_TOKEN)
        if n_occurrences > 0:
            for random_json in question_json['values']:
                self.__random_handlers.append(RandomHandler(random_json))
            if n_occurrences != len(self.__random_handlers):
                raise Exception("Warning: the number of specified random generator doesn't coincide with the " +
                                RANDOM_NUMBER_TOKEN + " found in:" + self.__text)

    def get_text_filled(self):
        text = self.__text
        random_nums = []
        for i in range(len(self.__random_handlers)):
            random_nums.insert(i, self.__random_handlers[i].get_random())
            text = text.replace(RANDOM_NUMBER_TOKEN, str(random_nums[i]), 1)
        return [text, random_nums]

    def get_type(self):
        return self.__type

    def get_points(self):
        return self.__points

    def is_optional(self):
        return self.__optional


class RandomHandler:
    """
        This class handles the random number generation for a single token.
        It contains all its configuration parameters.
    """

    def __init__(self, random_json):
        rand_type = random_json['type']

        if 'set'.__eq__(rand_type):
            self.__set = tuple(random_json['set'])
            self.__random_generator = self.__get_from_set
            return

        if 'float'.__eq__(rand_type):
            self.__size = 2
            self.__start = random_json['min']
            self.__end = random_json['max']
            self.__random_generator = self.__get_limited_float
            return

        if 'int'.__eq__(rand_type):
            self.__start = random_json['min']
            self.__end = random_json['max']
            self.__random_generator = self.__get_limited_int
            return

        raise Exception("Unknown random value type: " + rand_type)

    def __get_from_set(self):
        return choice(self.__set)

    def __get_limited_int(self):
        return randint(self.__start, self.__end)

    def __get_limited_float(self):
        return round(uniform(self.__start, self.__end), self.__size)

    def get_random(self):
        return self.__random_generator()
