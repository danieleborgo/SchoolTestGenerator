from math import ceil
from pylatex import LongTable, NoEscape
from generator.enums import StudentType


class PointsData:
    """
        This class is used to support the generation of the earned point table.
    """

    def __init__(self, total_points, number_of_questions, is_extra_enabled, extra_params):
        self.__total_points = total_points

        questions_numbers = ['Extra'] if is_extra_enabled else []
        questions_numbers += extra_params + list(range(1, number_of_questions + 1))

        table_string = '|c|' if is_extra_enabled else '|'
        table_string += 'c|' * (len(extra_params) + number_of_questions)

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
        This class supports the generation of the vote tables.
    """

    def __init__(self, votes_json, optional_count):
        min_vote = votes_json['min']['vote']
        min_required_points = votes_json['min']['up_to']
        max_vote = votes_json['max']['vote']
        max_required_points = votes_json['max']['from']

        string_st, points_st, votes_st = self.__create_earned_votes_array(max_vote, max_required_points,
                                                                          min_vote, min_required_points)
        string_wo, points_wo, votes_wo = self.__create_earned_votes_array(max_vote, max_required_points-optional_count,
                                                                          min_vote, min_required_points)

        self.__standard_votes_table = self.__create_table(string_st, points_st, votes_st)
        self.__votes_with_opt_table = self.__create_table(string_wo, points_wo, votes_wo)

    def __create_earned_votes_array(self, max_vote, max_required_points, min_vote, min_required_points):
        table_string = '|c|c|c|' + 'c|' * (max_required_points - min_required_points - 1)

        points_row = ['Punti', NoEscape('$ \\leq ' + str(min_required_points) + ' $')]
        points_row += list(range(min_required_points + 1, max_required_points))
        points_row.append(NoEscape('$ ' + '\\geq ' + str(max_required_points) + ' $'))

        vote_step = (max_vote - min_vote) / (max_required_points - min_required_points)
        vote_acc = float(min_vote)
        votes_row = ['Voto', min_vote]
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

    def insert_table(self, doc, student_type):
        if StudentType.OPTIONAL_QUESTIONS == student_type:
            doc.append(self.__votes_with_opt_table)
        else:
            doc.append(self.__standard_votes_table)

    class VoteConverter:
        __vote_table = ('0', '0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5',
                        '5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10')

        @staticmethod
        def to_vote(n):
            return VotesData.VoteConverter.__vote_table[ceil(n * 2) % 20]
