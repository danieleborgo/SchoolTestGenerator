"""
    Copyright (C) 2020  Borgo Daniele

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

from enum import Enum


class StudentType(Enum):
    """
        This enum is used to describes the different needs of students,
        defining several types, according to the school decided.
    """

    # This is the student's type of who hasn't it specified
    STANDARD = 0

    # This is the student's type of who needs more time
    MORE_TIME = 1

    # This is the student's type of who needs the permission to use notes
    ALLOW_NOTES = 2

    # This is the student's type of who needs optional questions
    OPTIONAL_QUESTIONS = 3

    @staticmethod
    def translate_type(string):
        """
            This method translates a string representing the type in
            an enum value.
        """

        if 'standard'.__eq__(string):
            return StudentType.STANDARD

        if 'more_time'.__eq__(string):
            return StudentType.MORE_TIME

        if 'allow_notes'.__eq__(string):
            return StudentType.ALLOW_NOTES

        if 'optional_questions'.__eq__(string):
            return StudentType.OPTIONAL_QUESTIONS

        raise Exception("Type "+string+" unknown.")


class QuestionType(Enum):
    """
        This class is used to define different types of questions in term of
        visualization in the final document.
    """

    # This type describes a question represented by only a question, without adding extra space
    NO_SPACED_QUESTION = 0

    SPACED_QUESTION = 1

    @staticmethod
    def translate_type(string):
        """
            This method translates a string representing the type in
            an enum value.
        """

        if 'no_space_question'.__eq__(string):
            return QuestionType.NO_SPACED_QUESTION

        if 'spaced_question'.__eq__(string):
            return QuestionType.SPACED_QUESTION

        raise Exception("Type " + string + " unknown.")
