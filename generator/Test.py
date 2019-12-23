from generator.enums import StudentType, QuestionType
from random import randint, uniform, choice

RANDOM_NUMBER_TOKEN = '%n'
NEW_LINE_TOKEN = '\n'
NEW_LINE_LATEX = '\\\\ '


class Test:
    """
        This class is supposed to optimize the file generation, reducing the
        amount of computation avoiding to calculate same things.
    """

    def __init__(self, test_json):
        self.__extract_parameters(test_json)

    def __extract_parameters(self, test_json):
        self.__subject = test_json['subject']
        self.__subtitle = test_json['subtitle']
        self.__language = test_json['language']
        self.__class = test_json['class']
        self.__years = test_json['years']
        self.__date = test_json['date']
        self.__duration = test_json['duration']
        self.__extra_point_en = test_json['extra_point'] if 'extra_point' in test_json else False
        self.__project_en = test_json['project'] if 'project' in test_json else False
        self.__votes_data = VotesData(test_json['votes'])

        if 'more_time_duration' in test_json:
            self.__more_time_duration = test_json['more_time_duration']
        else:
            self.__more_time_duration = self.__duration

        total_points = self.__extract_arguments(test_json['test'])

        self.__points_data = PointsData(
            total_points=total_points,
            number_of_questions=self.__number_of_questions,
            is_extra_enabled=self.__extra_point_en,
            extra_params=test_json['extra_params'] if 'extra_params' in test_json else []
        )

    def __extract_arguments(self, arguments_json):
        self.__arguments = []
        self.__number_of_questions = 0
        total_points = 1 if self.__extra_point_en else 0

        for i in range(len(arguments_json)):
            argument = Argument(arguments_json[i])
            self.__number_of_questions += argument.get_number_of_questions()
            total_points += argument.get_points()
            self.__arguments.append(argument)
        self.__arguments = tuple(self.__arguments)
        return total_points

    def get_output_file_name(self):
        return self.__subtitle + '_' + self.__class

    def get_subject(self):
        return self.__subject

    def get_subtitle(self):
        return self.__subtitle

    def get_language(self):
        return self.__language

    def get_test_class(self):
        return self.__class

    def get_years(self):
        return self.__years

    def get_date(self):
        return self.__date

    def get_duration(self, student_type):
        if student_type == StudentType.MORE_TIME:
            return self.__more_time_duration
        return self.__duration

    def get_points_data(self):
        return self.__points_data

    def get_votes_data(self):
        return self.__votes_data

    def get_arguments(self):
        return self.__arguments

    def is_extra_enabled(self):
        return self.__extra_point_en

    def get_bucket_name(self):
        return 'used_randoms_bucket_' + self.__class + '.txt'


class Argument:
    """
        This class is supposed to represent an argument, so a group of
        questions.
    """

    def __init__(self, argument_json):
        self.__name = argument_json['argument_name']
        self.__questions = []
        self.__points = 0

        for i in range(len(argument_json['questions'])):
            question = Question(argument_json['questions'][i])
            self.__points += question.get_points()
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


class PointsData:
    """
        This class is used to support the generation of the earned point table.
    """

    def __init__(self, total_points, number_of_questions, is_extra_enabled, extra_params):
        self.__total_points = total_points
        self.__questions_numbers = ['Extra'] if is_extra_enabled else []
        self.__table_string = '|c|' if is_extra_enabled else '|'

        self.__questions_numbers += extra_params
        self.__table_string += 'c|' * len(extra_params)

        for i in range(number_of_questions):
            self.__questions_numbers.append(str(i + 1))
            self.__table_string += 'c|'
        self.__questions_numbers = tuple(self.__questions_numbers)

    def get_questions_numbers(self):
        return self.__questions_numbers

    def get_table_string(self):
        return self.__table_string

    def get_total_points(self):
        return self.__total_points


class VotesData:
    """
        This class supports the generation of the vote tables.
    """

    def __init__(self, votes_json):
        self.__points = ['Punti']
        self.__votes = ['Voto']
        self.__table_string = '|c|c|c|'

        min_vote = votes_json['min']['vote']
        up_to_this = votes_json['min']['up_to']
        max_vote = votes_json['max']['vote']
        from_this = votes_json['max']['from']
        int_en = votes_json['int']

        vote_step = (max_vote - min_vote) / (from_this - up_to_this)
        vote = float(min_vote)

        self.__points.append('Fino a ' + str(up_to_this))
        self.__votes.append(min_vote)
        for i in range(up_to_this + 1, from_this):
            vote += vote_step
            self.__points.append(i)
            self.__votes.append(round(vote, 1) if not int_en else int(vote))
            self.__table_string += 'c|'
        self.__points.append('Da ' + str(from_this))
        self.__votes.append(max_vote)

    def get_points(self):
        return self.__points

    def get_votes(self):
        return self.__votes

    def get_table_string(self):
        return self.__table_string
