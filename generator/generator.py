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

from os import mkdir, path

from pylatex import *
from pylatex.utils import bold

import generator.sentences as sentences
from generator.User import translate_students, translate_anonymous_user, Student
from generator.enums import Modifier
from generator.test.Test import Test
from generator.test.TestLogger import TestLogger
from generator.test.test_support import VotesData, PointsData


def generate_tests(test_json: dict, students_json: dict = None, anonymous_json: dict = None):
    """
        This is the function that generates all the test, with the due differences.
        It gets the two JSON objects, passed as parameters, and creates the array
        students and the Test instance. Then it sets some general parameter in the
        of LaTex document, generates all the tests, creates the final PDF and, in
        the end creates a JSON file containing all the used random values.
    """

    output_folder = get_and_prepare_output_path(test_json)
    single_file_flag = is_single_file(test_json)

    test_logger = TestLogger(students_json is not None)
    test = Test(test_json, test_logger)

    if students_json is not None:
        students = translate_students(students_json)
        generate_test_with_configuration(
            single_file_flag=single_file_flag,
            test=test,
            students=students,
            test_logger=test_logger,
            output_folder=output_folder
        )
    elif anonymous_json is not None:
        anonymous_users = translate_anonymous_user(anonymous_json)
        generate_test_with_configuration(
            single_file_flag=single_file_flag,
            test=test,
            anonymous_users=anonymous_users,
            test_logger=test_logger,
            output_folder=output_folder
        )
    else:
        raise Exception("No users defined for the test")

    with open(f"{output_folder}logger_{test.subtitle.replace(' ', '')}"
              f"_{test.test_class.replace(' ', '')}"
              f"_{'s' if students_json is not None else 'a'}.json", "w") as output:
        output.write(test_logger.get_json())
        print(f"Generated logger file: {output.name}")


def generate_test_with_configuration(single_file_flag: bool, test: Test,
                                     test_logger: TestLogger, output_folder: str,
                                     students: tuple = None, anonymous_users: tuple = None):

    if bool(students is None) == bool(anonymous_users is None):
        raise Exception("Parameters malformed: define only one between students and anonymous users")

    is_students_mode = students is not None
    users = students if is_students_mode else anonymous_users

    if not single_file_flag:
        doc = generate_doc_file(test.language.lower())
    else:
        doc = None

    print("Generating... [  0%]", end='', flush=True)
    n_tests_generated = 0
    for i in range(len(users)):
        user = users[i]
        if single_file_flag:
            doc = generate_doc_file(test.language.lower())

        generate_test_single_user(doc, is_students_mode, user, test, test_logger)

        if single_file_flag:
            doc.generate_pdf(
                output_folder + (
                    (user.surname + '_' + user.name).replace(' ', '_') if is_students_mode
                    else str(i + 1)
                ),
                clean_tex=True
            )

        n_tests_generated += + 1
        print('\b' * 5 + "{:>4.0%}]".format(float(n_tests_generated) / len(users)), end='', flush=True)

    print()

    if not single_file_flag:
        doc.generate_pdf(
            output_folder + (test.subtitle + "_" + test.test_class).replace(' ', '') +
            ("_s" if is_students_mode else "_a"),
            clean_tex=True
        )
        print(f"Generated the PDF file with {len(users)} tests.")
    else:
        print(f"Generated {len(users)} tests")


def generate_doc_file(language: str) -> Document:
    """
        This function prepares a LaTeX file for containing all the information.
        These are general settings that can be specified once.
    """
    doc = Document(documentclass='article')
    doc.packages.append(Package('fancyhdr'))
    doc.packages.append(Package('babel', language))
    doc.packages.append(Package('titlesec'))
    doc.preamble.append(Command('titlelabel', NoEscape('\\thetitle\\enspace')))
    doc.append(Command('fontsize', arguments=['9', '9']))
    doc.packages.append(Package('geometry', 'top=2.5cm, left=3cm, right=3cm, bottom=2cm'))
    doc.packages.append(Package('enumitem'))
    return doc


def generate_test_single_user(doc: Document, is_for_a_student: bool, student: Student,
                              test: Test, test_logger: TestLogger):
    """
        This function generates a test for the passed student in the given document.
        It prints these things:
        - Header and footer
        - The two initial images
        - The student's name and surname
        - The title
        - The rules
        - The votes table
        - The earned points table
        - The result space
        - The questions
        It also returns the used random values, in order to allow the caller to collect them.
    """

    reset_page_counter(doc)
    reset_section_counter(doc)  # Useless but useful for extensions

    set_header_and_footer(
        doc=doc,
        date=test.date,
        test_class=test.test_class,
        years=test.years,
        register_number=student.register_number if is_for_a_student else None
    )

    print_logo(
        doc=doc,
        logo_path=test.logo_img_path
    )

    if is_for_a_student:
        print_student_name(
            doc=doc,
            name=student.name,
            surname=student.surname
        )
    else:
        print_student_name(doc=doc)

    print_title(
        doc=doc,
        subject=test.subject,
        subtitle=test.subtitle
    )

    doc.append(Command('section*', sentences.SECTIONS.REGULATION))
    print_rules(
        doc=doc,
        duration=test.get_duration(student.do_you_need(Modifier.MORE_TIME)),
        is_extra_enabled=test.is_extra_enabled(),
        is_open_book=test.is_open_book(),
        has_allow_notes=student.do_you_need(Modifier.ALLOW_NOTES)
    )

    doc.append(Command('section*', sentences.SECTIONS.EVALUATION))
    print_evaluation_rule_exercise(doc)
    print_points_to_vote_table(
        doc=doc,
        votes_data=test.votes_data,
        has_optional_questions=student.do_you_need(Modifier.OPTIONAL_QUESTIONS)
    )
    print_earned_points_table(
        doc=doc,
        points_data=test.points_data
    )

    new_page(doc)

    used_randoms, orders = print_questions_returning_randoms_and_orders(
        doc=doc,
        arguments=test.arguments,
        has_optional_questions=student.do_you_need(Modifier.OPTIONAL_QUESTIONS)
    )

    if is_for_a_student:
        test_logger.log_student_test(student, orders, used_randoms)
    else:
        test_logger.log_anonymous_test(orders, used_randoms)

    new_page(doc)


def set_header_and_footer(doc: Document, date: str, test_class: str, years: str,
                          register_number: str = None):
    doc.append(Command('fancyhf', ''))
    doc.append(Command('pagestyle', 'fancy'))
    if register_number is not None:
        doc.append(Command('lhead', NoEscape(bold(register_number))))
        doc.append(Command('chead', test_class + ' (' + years + ')'))
    else:
        doc.append(Command('lhead', test_class + ' (' + years + ')'))
    doc.append(Command('rhead', date))
    doc.append(Command('cfoot', Command('thepage')))


def print_logo(doc: Document, logo_path: str):
    if logo_path is None:
        return
    with doc.create(Figure(position='h!')) as logo_figure:
        logo_figure.add_image(logo_path, width=NoEscape(r'0.3\textwidth'))


def print_student_name(doc: Document, name: str = None, surname: str = None):
    with doc.create(LongTable('l l', col_space='0.6cm', row_height=2.0)) as name_table:
        surname_to_print = 20 * '_' if surname is None else surname.upper()
        name_to_print = 20 * '_' if name is None else name.upper()
        name_table.add_row([sentences.NAMING.SURNAME, bold(surname_to_print)])
        name_table.add_row([sentences.NAMING.NAME, bold(name_to_print)])


def print_title(doc: Document, subject: str, subtitle: str):
    # Using Latex title would have limited the program
    with doc.create(Center()) as center:
        center.append(Command('large'))
        center.append(bold(subject.upper()))
    with doc.create(Center()) as center:
        center.append(subtitle)


def print_rules(doc: Document, duration: str, is_extra_enabled: bool,
                is_open_book: bool, has_allow_notes: bool):
    with doc.create(Itemize()) as itemize:
        itemize.add_item(
            sentences.RULES.TIME_PREFIX + ' ' + str(duration) + ' ' + sentences.RULES.TIME_POSTFIX
        )

        for rule in sentences.RULES.USER_RULES:
            itemize.add_item(rule)

        if is_open_book:
            itemize.add_item(sentences.RULES.OPEN_BOOK)
        else:
            if has_allow_notes:
                itemize.add_item(sentences.RULES.YES_NOTES)
            else:
                itemize.add_item(sentences.RULES.NO_NOTES)

        if is_extra_enabled:
            itemize.add_item(sentences.RULES.EXTRA_POINT)


def print_evaluation_rule_exercise(doc: Document):
    doc.append(sentences.EVALUATION.TABLE_CAPTION + ':')
    with doc.create(LongTable(
            NoEscape('p{0.05\\textwidth}|p{0.81\\textwidth}'), row_height=1.5)
    ) as ex_table:
        ex_table.add_row([bold('100%'), sentences.EVALUATION.P100])
        ex_table.add_row([bold('75%'), sentences.EVALUATION.P75])
        ex_table.add_row([bold('50%'), sentences.EVALUATION.P50])
        ex_table.add_row([bold('25%'), sentences.EVALUATION.P25])


def print_points_to_vote_table(doc: Document, votes_data: VotesData, has_optional_questions: bool):
    votes_data.insert_table(doc, has_optional_questions)
    doc.append(Command('vspace', NoEscape('-0.5em')))


def print_earned_points_table(doc: Document, points_data: PointsData):
    points_data.insert_eval_table(doc)
    doc.append(Command('vspace', NoEscape('-1em')))

    with doc.create(LongTable('l l', row_height=2.5, col_space='0.5cm')) as eval_table:
        eval_table.add_row(
            [sentences.EVALUATION.GAINED_POINTS +
             ' (' + str(points_data.total_points) + '): ', '_'*10]
        )
        eval_table.add_row([sentences.EVALUATION.GRADE + ': ', '_'*10])


def print_questions_returning_randoms_and_orders(doc: Document, arguments: tuple,
                                                 has_optional_questions: bool):
    first = True
    used_randoms = []
    doc.append(sentences.EVALUATION.BEFORE_EX_NOTE)

    orders = []
    for argument in arguments:
        doc.append(Command('section*', argument.name))
        if argument.do_you_have_arg_text():
            doc.append(NoEscape(argument.argument_text))

        order = argument.get_question_order()
        for question_index in order:
            if first:
                options = ''
                first = False
            else:
                options = 'resume'

            with doc.create(Enumerate(options=options)) as enum:
                to_print, random = argument \
                    .get_question(question_index) \
                    .print_question_ret_randoms(has_optional_questions)
                used_randoms += random
                enum.add_item(NoEscape(to_print))
        orders.append(order)
    return used_randoms, orders


def reset_page_counter(doc: Document):
    doc.append(Command('setcounter', ['page', 1]))


def reset_section_counter(doc: Document):
    doc.append(Command('setcounter', ['section', 0]))


def new_page(doc: Document):
    doc.append(NewPage())


def get_and_prepare_output_path(json_test: dict):
    if 'out_folder' in json_test:
        output_path = json_test['out_folder'] + '/'
        if not path.isdir(output_path):
            mkdir(output_path)
        return output_path
    return ''


def is_single_file(test_json: dict):
    return test_json['single_files'] if 'single_files' in test_json else False
