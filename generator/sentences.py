"""
    Copyright (C) 2021  Borgo Daniele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
    SECTIONS = Sections(parser['Sections'])
    NAMING = Naming(parser['Naming'])
    RULES = Rules(parser['GeneralRules'], parser['UserRules'])
    EVALUATION = Evaluation(parser['Evaluation'])
    OTHERS = Others(parser['Others'])


def generate_file_name(language):
    return 'languages/' + language.lower().capitalize() + '.properties'


class Sections:
    def __init__(self, parser_sections):
        self.REGULATION = parser_sections['regulation'].capitalize()
        self.EVALUATION = parser_sections['evaluation'].capitalize()


class Naming:
    def __init__(self, parser_naming):
        self.NAME = parser_naming['name'].capitalize()
        self.SURNAME = parser_naming['surname'].capitalize()


class Rules:
    def __init__(self, parser_gen_rules, parser_us_rules):
        self.TIME_PREFIX = parser_gen_rules['time_prefix']
        self.TIME_POSTFIX = parser_gen_rules['time_postfix']
        self.OPEN_BOOK = parser_gen_rules['open_book']
        self.NO_NOTES = parser_gen_rules['no_notes']
        self.YES_NOTES = parser_gen_rules['yes_notes']
        self.EXTRA_POINT = parser_gen_rules['extra_point']

        self.USER_RULES = []
        for key in parser_us_rules:
            self.USER_RULES.append(parser_us_rules[key])
        self.USER_RULES = tuple(self.USER_RULES)


class Evaluation:
    def __init__(self, parser_evaluation):
        self.TABLE_CAPTION = parser_evaluation['table_caption']
        self.P100 = parser_evaluation['100%']
        self.P75 = parser_evaluation['75%']
        self.P50 = parser_evaluation['50%']
        self.P25 = parser_evaluation['25%']
        self.GAINED_POINTS = parser_evaluation['gained_points'].capitalize()
        self.GRADE = parser_evaluation['grade'].capitalize()
        self.BEFORE_EX_NOTE = parser_evaluation['before_ex_note']


class Others:
    def __init__(self, parser_others):
        self.OPTIONAL = parser_others['optional_question']
        self.EXTRA = parser_others['extra'].capitalize()
        self.POINTS = parser_others['points'].capitalize()
