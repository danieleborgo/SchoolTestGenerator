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

import json
from generator.User import Student


class TestLogger:
    """
        This class is used to store all the data needed for generating a logger file.
    """

    def __init__(self, is_student_mode):
        self.__data = {
            'mode': 'students' if is_student_mode else 'anonymous',
            'questions': {},
            'tests': []
        }

        if is_student_mode:
            self.log_student_test = self.__log_student_test
        else:
            self.log_anonymous_test = self.__log_anonymous_test

    def log_pure_questions(self, argument: str, texts):
        self.__data['questions'][argument] = texts

    def __log_student_test(self, student: Student, orders, random_samples):
        self.__data['tests'].append({
            'type': 'student',
            'surname': student.surname,
            'name': student.name,
            'orders': orders,
            'random': random_samples
        })

    def __log_anonymous_test(self, orders, random_samples):
        self.__data['tests'].append({
            'type': 'anonymous',
            'orders': orders,
            'random': random_samples
        })

    def get_json(self):
        return json.dumps(self.__data, indent=4)
