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

from enum import Enum


class Modifier(Enum):
    """
        This enum is used to describes the different needs of students,
        defining several types, according to the school decided.
    """

    # This is the modifier for who needs more time
    MORE_TIME = 1

    # This is the modifier for who needs the permission to use notes
    ALLOW_NOTES = 2

    # This is the modifier for who needs optional questions
    OPTIONAL_QUESTIONS = 3

    # This is the modifier for increasing font size
    BIGGER_FONT = 4

    @staticmethod
    def translate(string):
        """
            This method translates a string representing the type in
            an enum value.
        """

        if 'more_time'.__eq__(string):
            return Modifier.MORE_TIME

        if 'allow_notes'.__eq__(string):
            return Modifier.ALLOW_NOTES

        if 'optional_questions'.__eq__(string):
            return Modifier.OPTIONAL_QUESTIONS

        if 'bigger_font'.__eq__(string):
            return Modifier.BIGGER_FONT

        raise Exception("Type " + string + " unknown.")


class QuestionType(Enum):
    """
        This class is used to define different types of questions in term of
        visualization in the final document.
    """

    # This type describes a question represented by only a question, without adding extra space
    NO_SPACED_QUESTION = 0

    # This type defines a question with a space for the answer
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
