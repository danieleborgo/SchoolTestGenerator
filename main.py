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

import sys
from generator.generator import generate_tests

if __name__ == '__main__':
    print("SCHOOL TEST GENERATOR\nCopyright (C) 2020  Borgo Daniele\n")

    if len(sys.argv) < 2:
        raise Exception("Two parameters are requested")
    else:
        generate_tests(
            students_file_name=sys.argv[1],
            test_file_name=sys.argv[2]
        )
