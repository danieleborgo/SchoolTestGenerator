from enum import Enum


class StudentType(Enum):
    STANDARD = 0
    MORE_TIME = 1
    ALLOW_NOTES = 2
    OPTIONAL_QUESTIONS = 3

    @staticmethod
    def translate_type(string):
        if 'standard'.__eq__(string):
            return StudentType.STANDARD

        if 'more_time'.__eq__(string):
            return StudentType.MORE_TIME

        if 'allow_notes'.__eq__(string):
            return StudentType.ALLOW_NOTES

        if 'optional_questions'.__eq__(string):
            return StudentType.OPTIONAL_QUESTIONS

        print("Warning: type "+string+" unknown")
        return StudentType.STANDARD


class QuestionType(Enum):
    UNDEFINED = 0
    NO_SPACED_QUESTION = 1

    @staticmethod
    def translate_type(string):
        if 'no_space_question'.__eq__(string):
            return QuestionType.NO_SPACED_QUESTION

        print("Warning: type " + string + " unknown")
        return QuestionType.UNDEFINED
