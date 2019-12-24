from pylatex import LongTable


class PointsData:
    """
        This class is used to support the generation of the earned point table.
    """

    def __init__(self, total_points, number_of_questions, is_extra_enabled, extra_params):
        self.__total_points = total_points

        questions_numbers = ['Extra'] if is_extra_enabled else []
        questions_numbers += extra_params + list(range(1, number_of_questions+1))

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
        self.__points = ['Punti']
        self.__votes = ['Voto']
        self.__table_string = '|c|c|c|'

        min_vote = votes_json['min']['vote']
        min_required_points = votes_json['min']['up_to']

        max_vote = votes_json['max']['vote']
        max_required_points = votes_json['max']['from']

        int_en = votes_json['int']

        vote_step = (max_vote - min_vote) / (max_required_points - min_required_points)

        vote = float(min_vote)

        self.__points.append('Fino a ' + str(min_required_points))
        self.__votes.append(min_vote)
        for i in range(min_required_points + 1, max_required_points):
            vote += vote_step
            self.__points.append(i)
            self.__votes.append(round(vote, 1) if not int_en else int(vote))
            self.__table_string += 'c|'
        self.__points.append('Da ' + str(max_required_points))
        self.__votes.append(max_vote)

    def get_points(self):
        return self.__points

    def get_votes(self):
        return self.__votes

    def get_table_string(self):
        return self.__table_string
