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

from argparse import ArgumentParser
from json import load as json_load
from generator.generator import generate_tests


def import_json(file_name):
    if file_name is None:
        return None
    with open(file_name) as json_source:
        return json_load(json_source)


if __name__ == '__main__':
    print("SCHOOL TEST GENERATOR\nCopyright (C) 2021  Borgo Daniele\n")

    parser = ArgumentParser(description='This program generates school tests')
    parser.add_argument('test_path', type=str, nargs=1,
                        help='The path of the JSON test file')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--students', dest='students_path',
                       help='Add the path of named students JSON file')
    group.add_argument('-a', '--anonymous', dest='users_path',
                       help='Add the path of anonymous students JSON file')

    args = parser.parse_args()

    test_json = import_json(args.test_path[0])
    students_json = import_json(args.students_path)
    anonymous_users_json = import_json(args.users_path)

    generate_tests(
        test_json=test_json,
        students_json=students_json,
        anonymous_json=anonymous_users_json
    )
