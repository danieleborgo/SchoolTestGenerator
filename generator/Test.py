from random import seed
from warnings import warn
from generator.enums import StudentType
from generator.Argument import Argument
from generator.test_support import PointsData, VotesData


class Test:
    """
        This class is supposed to optimize the file generation, reducing the
        amount of computation avoiding to calculate same things.
    """

    def __init__(self, test_json):
        self.__extract_parameters(test_json)
        seed(self.__generate_seed())

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

        if 'more_time_duration' in test_json:
            self.__more_time_duration = test_json['more_time_duration']

            if self.__more_time_duration < self.__duration:
                warn("The quantity specified as more_time_duration are lower than normal duration")
        else:
            self.__more_time_duration = self.__duration

        total_points = self.__extract_arguments(test_json['test'])
        self.__votes_data = VotesData(test_json['votes'], self.__optionals_count)

        self.__points_data = PointsData(
            total_points=total_points,
            number_of_questions=self.__number_of_questions,
            is_extra_enabled=self.__extra_point_en,
            extra_params=test_json['extra_params'] if 'extra_params' in test_json else [],
        )

    def __extract_arguments(self, arguments_json):
        self.__arguments = []
        self.__number_of_questions = 0
        self.__optionals_count = 0
        total_points = 1 if self.__extra_point_en else 0

        for i in range(len(arguments_json)):
            argument = Argument(arguments_json[i])

            self.__number_of_questions += argument.get_number_of_questions()
            total_points += argument.get_points()
            self.__optionals_count += argument.get_optionals_count()

            self.__arguments.append(argument)

        self.__arguments = tuple(self.__arguments)
        return total_points

    def __generate_seed(self):
        # This should be unique for each test in each class
        return self.__subject + self.__subtitle + self.__class + self.__years

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
