from enum import Enum


class TYPE(Enum):
    STANDARD = 0,
    MORE_TIME = 1

    @staticmethod
    def translate_type(string):
        if 'more_time'.__eq__(string):
            return TYPE.MORE_TIME

        print("Warning: type "+string+" unknown")
        return TYPE.STANDARD
