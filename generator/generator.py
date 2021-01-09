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

from json import load as json_load
from pylatex import *
from pylatex.utils import bold
import csv
from generator.Student import translate_students
from generator.Test import Test
from generator.enums import Modifier
import generator.sentences as sentences


def generate_tests(students_file_name, test_file_name):
    """
        This is the function that generates all the test, with the due differences.
        It imports the two JSON files, passed as parameters, and creates the array
        of students and the Test instance. Then it sets some general parameter in
        the LaTex document, generates all the tests, creates the final PDF and, in
        the end, if necessary, creates a file containing all the used random values.
    """

    try:
        students_file = open(students_file_name)
    except IOError:
        raise Exception("The file " + students_file_name + " doesn't exist")
    students = translate_students(json_load(students_file))
    students_file.close()
    del students_file

    try:
        test_file = open(test_file_name)
    except IOError:
        raise Exception("The file " + test_file_name + " doesn't exist")
    test = Test(json_load(test_file))
    test_file.close()
    del test_file

    if not test.is_single_files():
        doc = generate_doc_file(test.get_language().lower())
    else:
        doc = None

    used_randoms_bucket = []
    for student in students:
        if test.is_single_files():
            doc = generate_doc_file(test.get_language().lower())

        generate_test_single_student(doc, student, test, used_randoms_bucket)

        if test.is_single_files():
            doc.generate_pdf(
                test.get_out_path() + (student.get_surname() + '_' + student.get_name()).replace(' ', '_'),
                clean_tex=True
            )

    print("Generated " + str(len(students)) + " tests")

    if not test.is_single_files():
        doc.generate_pdf(test.get_out_path() + test.get_output_file_name(), clean_tex=False)
    print("Generated the PDF file")

    if generate_used_randoms_file_if_necessary(
            used_randoms_bucket, test.get_out_path() + test.get_bucket_name()):
        print("Generated random values used file")


def generate_doc_file(language):
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


def generate_test_single_student(doc, student, test, used_randoms_bucket):
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
        date=test.get_date(),
        test_class=test.get_test_class(),
        years=test.get_years(),
        register_number=student.get_register_number()
    )

    print_figures(doc)

    print_student_name(
        doc=doc,
        name=student.get_name(),
        surname=student.get_surname()
    )

    print_title(
        doc=doc,
        subject=test.get_subject(),
        subtitle=test.get_subtitle()
    )

    doc.append(Command('section*', sentences.SECTIONS.REGULATION))
    print_rules(
        doc=doc,
        duration=test.get_duration(student.do_you_want(Modifier.MORE_TIME)),
        is_extra_enabled=test.is_extra_enabled(),
        is_open_book=test.is_open_book(),
        has_allow_notes=student.do_you_want(Modifier.ALLOW_NOTES)
    )

    doc.append(Command('section*', sentences.SECTIONS.EVALUATION))
    print_evaluation_rule_exercise(doc)
    print_points_to_vote_table(
        doc=doc,
        votes_data=test.get_votes_data(),
        has_optional_questions=student.do_you_want(Modifier.OPTIONAL_QUESTIONS)
    )
    print_earned_points_table(
        doc=doc,
        points_data=test.get_points_data()
    )

    new_page(doc)

    used_randoms = print_questions_returning_randoms(
        doc=doc,
        arguments=test.get_arguments(),
        has_optional_questions=student.do_you_want(Modifier.OPTIONAL_QUESTIONS)
    )
    used_randoms.insert(0, student.get_surname())
    used_randoms_bucket.append(used_randoms)

    new_page(doc)


def set_header_and_footer(doc, date, test_class, years, register_number):
    doc.append(Command('fancyhf', ''))
    doc.append(Command('pagestyle', 'fancy'))
    doc.append(Command('lhead', NoEscape(bold(register_number))))
    doc.append(Command('chead', test_class + ' (' + years + ')'))
    doc.append(Command('rhead', date))
    doc.append(Command('cfoot', Command('thepage')))


def print_figures(doc):
    with doc.create(Figure(position='h!')):
        with doc.create(SubFigure(
                position='b',
                width=NoEscape(r'0.5\linewidth'))) as left_figure:
            left_figure.add_image('../images/school_logo.png')
        with doc.create(SubFigure(
                position='b',
                width=NoEscape(r'0.5\linewidth'))) as right_figure:
            right_figure.add_image('../images/school_data.png')


def print_student_name(doc, name, surname):
    with doc.create(LongTable('l l', col_space='0.6cm', row_height=2.0)) as name_table:
        name_table.add_row([sentences.NAMING.SURNAME, bold(surname.upper())])
        name_table.add_row([sentences.NAMING.NAME, bold(name.upper())])


def print_title(doc, subject, subtitle):
    # Using Latex title would have limited the program
    with doc.create(Center()) as center:
        center.append(Command('large'))
        center.append(bold(subject.upper()))
    with doc.create(Center()) as center:
        center.append(subtitle)


def print_rules(doc, duration, is_extra_enabled, is_open_book, has_allow_notes):
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


def print_evaluation_rule_exercise(doc):
    doc.append(sentences.EVALUATION.TABLE_CAPTION + ':')
    with doc.create(LongTable(NoEscape('p{0.05\\textwidth}|p{0.81\\textwidth}'), row_height=1.5)) as ex_table:
        ex_table.add_row([bold('100%'), sentences.EVALUATION.P100])
        ex_table.add_row([bold('75%'), sentences.EVALUATION.P75])
        ex_table.add_row([bold('50%'), sentences.EVALUATION.P50])
        ex_table.add_row([bold('25%'), sentences.EVALUATION.P25])


def print_points_to_vote_table(doc, votes_data, has_optional_questions):
    votes_data.insert_table(doc, has_optional_questions)
    doc.append(Command('vspace', NoEscape('-0.5em')))


def print_earned_points_table(doc, points_data):
    points_data.insert_eval_table(doc)
    doc.append(Command('vspace', NoEscape('-1em')))

    with doc.create(LongTable('l l', row_height=2.5, col_space='0.5cm')) as eval_table:
        eval_table.add_row(
            [sentences.EVALUATION.GAINED_POINTS +
             ' (' + str(points_data.get_total_points()) + '): ', '__________']
        )
        eval_table.add_row([sentences.EVALUATION.GRADE + ': ', '__________'])


def print_questions_returning_randoms(doc, arguments, has_optional_questions):
    first = True
    used_randoms = []
    doc.append(sentences.EVALUATION.BEFORE_EX_NOTE)

    for argument in arguments:
        doc.append(Command('section*', argument.get_name()))
        if argument.do_you_have_arg_text():
            doc.append(NoEscape(argument.get_argument_text()))

        for question in argument.get_questions():
            if first:
                options = ''
                first = False
            else:
                options = 'resume'
            with doc.create(Enumerate(options=options)) as enum:
                used_randoms += question.print_question_ret_randoms(enum, has_optional_questions)
    return used_randoms


def generate_used_randoms_file_if_necessary(used_randoms_bucket, name):
    if len(used_randoms_bucket[0]) > 1:
        with open(f'{name}.csv', mode='w') as bucket_file:
            bucket_writer = csv.writer(bucket_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for list in used_randoms_bucket:
                bucket_writer.writerow(list)
        return True
    return False


def reset_page_counter(doc):
    doc.append(Command('setcounter', ['page', 1]))


def reset_section_counter(doc):
    doc.append(Command('setcounter', ['section', 0]))


def new_page(doc):
    doc.append(NewPage())
