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


class User:
    def __init__(self, modifiers):
        self.__modifiers = tuple(modifiers)

    def do_you_need(self, modifier):
        return modifier in self.__modifiers


class Student(User):
    """
        This class represents a single student through these:
        - A register number
        - A name
        - A surname
        - A type for describe students needs
    """

    def __init__(self, register_number, name, surname, modifiers):
        super().__init__(modifiers)
        self.__register_number = register_number
        self.__name = name
        self.__surname = surname

    @property
    def register_number(self):
        return self.__register_number

    @property
    def name(self):
        return self.__name

    @property
    def surname(self):
        return self.__surname


class AnonymousUser(User):
    def __init__(self, modifiers):
        super().__init__(modifiers)


def translate_students(students_json):
    """
        This function translates an array of JSON students in an array
        of instances of Student, properly filled with data.
    """
    students = []

    for i in range(len(students_json)):
        students.append(
            Student(
                register_number=i + 1,
                name=students_json[i]['name'],
                surname=students_json[i]['surname'],
                modifiers=extract_mods(students_json[i])
            )
        )

    return tuple(students)


def translate_anonymous_user(anonymous_user):
    return tuple([
        AnonymousUser(extract_mods(user_json)) for user_json in anonymous_user
    ])


def extract_mods(user_json):
    if 'mod' in user_json:
        if isinstance(user_json['mod'], list):
            return [Modifier.translate(mod) for mod in user_json['mod']]
        return [Modifier.translate(user_json['mod'])]
    return []
