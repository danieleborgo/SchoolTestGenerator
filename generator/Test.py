from generator.enums import TYPE


class Test:
    def __init__(self, json):
        self.__subject = json['subject']
        self.__subtitle = json['subtitle']
        self.__language = json['language']
        self.__class = json['class']
        self.__date = json['date']
        self.__duration = json['duration']
        if 'more_time_duration' in json:
            self.__more_time_duration = json['more_time_duration']
        else:
            self.__more_time_duration = self.__duration

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

    def get_date(self):
        return self.__date

    def get_duration(self, student_type):
        if student_type == TYPE.MORE_TIME:
            return self.__more_time_duration
        return self.__duration
