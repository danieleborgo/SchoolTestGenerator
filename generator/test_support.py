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

from math import ceil
from pylatex import LongTable, NoEscape
from generator.enums import Modifier
import generator.sentences as sentences


class PointsData:
    """
        This class handle the data relative to points assignment, so the evaluation table
        and the total amount of the test points.
        This class creates a table useful to write earned points by a student
        in function of the exercise number. It can contains also some additional field,
        like an extra point for the order and others field defined in the apposite
        parameter in the JSON file.
        After having create the table, it can be injected several times in the document,
        using the apposite public method.
    """

    def __init__(self, total_points, number_of_questions, is_extra_enabled, additional_params):
        self.__total_points = total_points

        # Create the first row of the table
        questions_numbers = [sentences.OTHERS.EXTRA] if is_extra_enabled else []
        questions_numbers += additional_params + list(range(1, number_of_questions + 1))

        # Create the table string
        table_string = ('|c|' if is_extra_enabled else '|') + 'c|' * (len(additional_params) + number_of_questions)

        self.__create_table(table_string, questions_numbers)

    def __create_table(self, table_string, questions_numbers):
        self.__eval_table = LongTable(table_string, row_height=2.0, col_space='0.5cm')
        self.__eval_table.add_hline()
        self.__eval_table.add_row(questions_numbers)
        self.__eval_table.add_hline()
        self.__eval_table.add_empty_row()
        self.__eval_table.add_hline()

    def insert_eval_table(self, doc):
        doc.append(self.__eval_table)

    def get_total_points(self):
        return self.__total_points


class VotesData:
    """
        This class generates and handles the vote table, the one used to compute
        the vote, given the total earned points. It gets data from the apposite
        section in the JSON.
        It generates actually two tables:
        - The standard one, as specified in the JSON file;
        - The one for the students who have optional questions.
        With the apposite public method, it injects this table in the document,
        since it is able to insert it several times.
    """

    def __init__(self, votes_json, optional_count):
        min_vote = votes_json['min']['vote']
        min_required_points = votes_json['min']['up_to']
        max_vote = votes_json['max']['vote']
        max_required_points = votes_json['max']['from']

        # The first is the table string, the second the row containing earned points and the third the grades
        string_st, points_st, votes_st = self.__create_earned_votes_array(max_vote, max_required_points,
                                                                          min_vote, min_required_points)
        string_wo, points_wo, votes_wo = self.__create_earned_votes_array(max_vote, max_required_points-optional_count,
                                                                          min_vote, min_required_points)

        self.__standard_votes_table = self.__create_table(string_st, points_st, votes_st)
        self.__votes_with_opt_table = self.__create_table(string_wo, points_wo, votes_wo)

    def __create_earned_votes_array(self, max_vote, max_required_points, min_vote, min_required_points):
        table_string = '|c|c|c|' + 'c|' * (max_required_points - min_required_points - 1)

        points_row = [sentences.OTHERS.POINTS, NoEscape('$ \\leq ' + str(min_required_points) + ' $')]
        points_row += list(range(min_required_points + 1, max_required_points))
        points_row.append(NoEscape('$ ' + '\\geq ' + str(max_required_points) + ' $'))

        vote_step = (max_vote - min_vote) / (max_required_points - min_required_points)
        vote_acc = float(min_vote)
        votes_row = [sentences.EVALUATION.GRADE, min_vote]
        for i in range(min_required_points + 1, max_required_points):
            vote_acc += vote_step
            votes_row.append(self.VoteConverter.to_vote(vote_acc))
        votes_row.append(max_vote)

        return [table_string, points_row, votes_row]

    @staticmethod
    def __create_table(table_string, points, standard_votes):
        table = LongTable(table_string, row_height=1.5, col_space='0.5cm')
        table.add_hline()
        table.add_row(points)
        table.add_hline()
        table.add_row(standard_votes)
        table.add_hline()
        return table

    def insert_table(self, doc, has_optional_questions):
        if has_optional_questions:
            doc.append(self.__votes_with_opt_table)
        else:
            doc.append(self.__standard_votes_table)

    class VoteConverter:
        """
            This class is used to convert a float value in the closest upper grade.
        """
        __vote_table = ('0', '0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5',
                        '5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10')

        @staticmethod
        def to_vote(n):
            return VotesData.VoteConverter.__vote_table[ceil(n * 2)]
