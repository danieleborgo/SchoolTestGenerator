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

from generator.enums import Modifier


class Student:
    """
        This class represents a single student through these:
        - A register number
        - A name
        - A surname
        - A type for describe students needs
    """
    def __init__(self, register_number, name, surname, modifiers):
        self.__register_number = register_number
        self.__name = name
        self.__surname = surname
        self.__modifiers = tuple(modifiers)

    def get_register_number(self):
        return self.__register_number

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_modifiers(self):
        return self.__modifiers

    def do_you_want(self, modifier):
        return modifier in self.__modifiers


def translate_students(students_json):
    """
        This function translates an array of JSON students in an array
        of instances of Student, properly filled with data.
    """
    students = []

    for i in range(len(students_json)):

        if 'mod' in students_json[i]:
            if isinstance(students_json[i]['mod'], list):
                modifiers = [Modifier.translate(mod) for mod in students_json[i]['mod']]
            else:
                modifiers = [Modifier.translate(students_json[i]['mod'])]
        else:
            modifiers = []

        students.append(
            Student(
                register_number=i+1,
                name=students_json[i]['name'],
                surname=students_json[i]['surname'],
                modifiers=modifiers
            )
        )

    return students
