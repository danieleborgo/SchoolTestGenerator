from generator.enums import STUDENT_TYPE, QUESTION_TYPE


class Test:
    def __init__(self, json):
        self.__extract_parameters(json)
        self.__extract_arguments(json['test'], json['order_point'])

        # Todo move these
        self.__votes_data = VotesData()

    def __extract_parameters(self, json):
        self.__subject = json['subject']
        self.__subtitle = json['subtitle']
        self.__language = json['language']
        self.__class = json['class']
        self.__years = json['years']
        self.__date = json['date']
        self.__duration = json['duration']
        if 'more_time_duration' in json:
            self.__more_time_duration = json['more_time_duration']
        else:
            self.__more_time_duration = self.__duration

    def __extract_arguments(self, arguments, is_order_point_enabled):
        self.__arguments = []
        self.__number_of_questions = 0
        self.__total_points = 0

        for i in range(len(arguments)):
            argument = Argument(arguments[i])
            self.__number_of_questions += argument.get_number_of_questions()
            self.__total_points += argument.get_points()
            self.__arguments.append(argument)
        self.__arguments = tuple(self.__arguments)

        self.__points_data = PointsData(self.__number_of_questions, is_order_point_enabled)

    def get_output_file_name(self):
        return self.__subtitle + '_' + self.__class

    def get_subject(self):
        return self.__subject

    def get_subtitle(self):
        return self.__subtitle

    def get_language(self):
        return self.__language

    def get_class(self):
        return self.__class

    def get_years(self):
        return self.__years

    def get_date(self):
        return self.__date

    def get_duration(self, student_type):
        if student_type == STUDENT_TYPE.MORE_TIME:
            return self.__more_time_duration
        return self.__duration

    def get_points_data(self):
        return self.__points_data

    def get_votes_data(self):
        return self.__votes_data

    def get_arguments(self):
        return self.__arguments


class Argument:
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
    def __init__(self, question_json):
        self.__type = QUESTION_TYPE.translate_type(question_json['type'])
        self.__text = question_json['text']

        if 'points' in question_json:
            self.__points = question_json['points']
        else:
            self.__points = 1

    def get_text(self):
        return self.__text

    def get_type(self):
        return self.__type

    def get_points(self):
        return self.__points


class PointsData:
    def __init__(self, n, is_order_enabled):
        self.__questions_numbers = ['Ordine'] if is_order_enabled else []
        self.__table_string = '|c|' if is_order_enabled else '|'

        for i in range(n):
            self.__questions_numbers.append(i+1)
            self.__table_string += 'c|'
        self.__questions_numbers = tuple(self.__questions_numbers)

    def get_questions_numbers(self):
        return self.__questions_numbers

    def get_table_string(self):
        return self.__table_string


class VotesData:
    def __init__(self):
        # TODO fix this
        self.__points = ('Punti', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.__votes = ('Voto', 3, 3, 3, 4, 5, 6, 7, 8, 9, 10)
        self.__table_string = '|c|c|c|c|c|c|c|c|c|c|c|'

    def get_points(self):
        return self.__points

    def get_votes(self):
        return self.__votes

    def get_table_string(self):
        return self.__table_string
