from configparser import ConfigParser

SECTIONS = None
NAMING = None
RULES = None
EVALUATION = None
OTHERS = None


def import_sentences(language):
    """
    This function import from the file properties the sentences.

    :param language: the language of the test to create
    :return:
    """
    parser = ConfigParser()
    parser.read(generate_file_name(language))

    global SECTIONS, NAMING, RULES, EVALUATION, OTHERS
    SECTIONS = Sections(parser)
    NAMING = Naming(parser)
    RULES = Rules(parser)
    EVALUATION = Evaluation(parser)
    OTHERS = Others(parser)


def generate_file_name(language):
    return 'languages/' + language.lower().capitalize() + '.properties'


class Sections:
    def __init__(self, parser):
        self.REGULATION = parser.get('Sections', 'regulation').capitalize()
        self.EVALUATION = parser.get('Sections', 'evaluation').capitalize()


class Naming:
    def __init__(self, parser):
        self.NAME = parser.get('Naming', 'name').capitalize()
        self.SURNAME = parser.get('Naming', 'surname').capitalize()


class Rules:
    def __init__(self, parser):
        self.TIME_PREFIX = parser.get('Rules', 'time_prefix')
        self.TIME_POSTFIX = parser.get('Rules', 'time_postfix')
        self.NO_SMART_PHONES = parser.get('Rules', 'no_smart_phones')
        self.NO_STAND_UP = parser.get('Rules', 'no_stand_up')
        self.NO_NOTES = parser.get('Rules', 'no_notes')
        self.YES_NOTES = parser.get('Rules', 'yes_notes')
        self.EXTRA_POINT = parser.get('Rules', 'extra_point')


class Evaluation:
    def __init__(self, parser):
        self.TABLE_CAPTION = parser.get('Evaluation', 'table_caption')
        self.P100 = parser.get('Evaluation', '100%')
        self.P75 = parser.get('Evaluation', '75%')
        self.P50 = parser.get('Evaluation', '50%')
        self.P25 = parser.get('Evaluation', '25%')
        self.GAINED_POINTS = parser.get('Evaluation', 'gained_points').capitalize()
        self.GRADE = parser.get('Evaluation', 'grade').capitalize()
        self.BEFORE_EX_NOTE = parser.get('Evaluation', 'before_ex_note')


class Others:
    def __init__(self, parser):
        self.OPTIONAL = parser.get('Others', 'optional_question')
        self.EXTRA = parser.get('Others', 'extra').capitalize()
        self.POINTS = parser.get('Others', 'points').capitalize()
