from generator.enums import TYPE


class Test:
    def __init__(self, json):
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
        self.__order_point = json['order_point']
        self.__points_data = PointsData()
        self.__votes_data = VotesData()

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
        if student_type == TYPE.MORE_TIME:
            return self.__more_time_duration
        return self.__duration

    def is_order_point_set(self):
        return self.__order_point

    def get_points_data(self):
        return self.__points_data

    def get_votes_data(self):
        return self.__votes_data


class PointsData:
    def __init__(self):
        # TODO fix this
        self.__questions_numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.__points_by_question = (1, 1, 1, 2, 1, 1, 1, 1, 1)
        self.__table_string = '|c|c|c|c|c|c|c|c|c|'

    def get_questions_numbers(self):
        return self.__questions_numbers

    def get_points_by_question(self):
        return self.__points_by_question

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
