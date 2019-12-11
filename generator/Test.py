

class Test:
    def __init__(self, json):
        self.__subject = json['subject']
        self.__subtitle = json['subtitle']
        self.__language = json['language']
        self.__class = json['class']
        self.__date = json['date']
        self.__duration = json['duration']

    def get_output_file_name(self):
        return self.__subtitle + '_' + self.__class

    def get_subject(self):
        return self.__subject

    def get_subtitle(self):
        return self.__subtitle

    def get_language(self):
        return self.__language

    def get_subtitle(self):
        return self.__subtitle

    def get_class(self):
        return self.__class

    def get_date(self):
        return self.__date
