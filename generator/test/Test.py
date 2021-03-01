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

from random import seed
from warnings import warn
from generator.test.Argument import Argument
from generator.test.test_support import PointsData, VotesData
import generator.sentences as sentences


class Test:
    """
        This is the most important class of the generator and it's responsible for optimizing
        the generation of the test, integrating the JSON file with some further information.
        Its first operations are supposed to extract simple data from the JSON, like subject,
        subtitle, language and so on. Then it extracts all the arguments and their relative
        questions, storing them in apposite object. In the end, it creates an instance of
        VotesData and one of PointsData, in order to optimize the generation of these two
        tables.
    """

    def __init__(self, test_json, test_logger):
        self.__extract_parameters(test_json, test_logger)
        seed(self.__generate_seed())

    def __extract_parameters(self, test_json, test_logger):
        self.__subject = test_json['subject']
        self.__subtitle = test_json['subtitle']
        self.__language = test_json['language'].capitalize()
        self.__class = test_json['class'] if 'class' in test_json else None
        self.__years = test_json['years']
        self.__date = test_json['date']
        self.__logo_img_path = test_json['logo'] if 'logo' in test_json else None
        self.__duration = test_json['duration']
        self.__extra_point_en = test_json['extra_point'] if 'extra_point' in test_json else False
        self.__is_open_book = test_json['open_book'] if 'open_book' in test_json else False

        sentences.import_sentences(self.__language)

        if 'more_time_duration' in test_json:
            self.__more_time_duration = test_json['more_time_duration']

            if self.__more_time_duration < self.__duration:
                warn("The quantity specified as more_time_duration are lower than normal duration")
        else:
            self.__more_time_duration = self.__duration

        total_points = self.__extract_arguments_and_points(test_json['test'], test_logger)
        self.__votes_data = VotesData(test_json['votes'], self.__optionals_count)

        self.__points_data = PointsData(
            total_points=total_points,
            number_of_questions=self.__number_of_questions,
            is_extra_enabled=self.__extra_point_en,
            additional_params=test_json['extra_params'] if 'extra_params' in test_json else [],
        )

    def __extract_arguments_and_points(self, arguments_json, test_logger):
        self.__arguments = []
        self.__number_of_questions = 0
        self.__optionals_count = 0
        total_points = 1 if self.__extra_point_en else 0

        for single_argument_json in arguments_json:
            argument = Argument(single_argument_json, test_logger)

            self.__number_of_questions += argument.number_of_questions
            total_points += argument.total_points
            self.__optionals_count += argument.optionals_count

            self.__arguments.append(argument)

        self.__arguments = tuple(self.__arguments)
        return total_points

    def __generate_seed(self):
        # This should be unique for each test in each class
        return self.__subject + self.__subtitle + self.__class + self.__years

    def get_duration(self, has_more_time_mod):
        if has_more_time_mod:
            return self.__more_time_duration
        return self.__duration

    def is_extra_enabled(self):
        return self.__extra_point_en

    def is_open_book(self):
        return self.__is_open_book

    @property
    def subject(self):
        return self.__subject

    @property
    def subtitle(self):
        return self.__subtitle

    @property
    def language(self):
        return self.__language

    @property
    def test_class(self):
        return self.__class

    @property
    def years(self):
        return self.__years

    @property
    def date(self):
        return self.__date

    @property
    def logo_img_path(self):
        return self.__logo_img_path

    @property
    def points_data(self):
        return self.__points_data

    @property
    def votes_data(self):
        return self.__votes_data

    @property
    def arguments(self):
        return self.__arguments
