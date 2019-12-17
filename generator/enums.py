from enum import Enum


class STUDENT_TYPE(Enum):
    STANDARD = 0
    MORE_TIME = 1
    ALLOW_NOTES = 2
    OPTIONAL_QUESTIONS = 3

    @staticmethod
    def translate_type(string):
        if 'more_time'.__eq__(string):
            return STUDENT_TYPE.MORE_TIME

        if 'allow_notes'.__eq__(string):
            return STUDENT_TYPE.ALLOW_NOTES

        if 'optional_questions'.__eq__(string):
            return STUDENT_TYPE.OPTIONAL_QUESTIONS

        print("Warning: type "+string+" unknown")
        return STUDENT_TYPE.STANDARD


class QUESTION_TYPE(Enum):
    UNDEFINED = 0
    NO_SPACED_QUESTION = 1

    @staticmethod
    def translate_type(string):
        if 'no_space_question'.__eq__(string):
            return QUESTION_TYPE.NO_SPACED_QUESTION

        print("Warning: type " + string + " unknown")
        return QUESTION_TYPE.UNDEFINED
