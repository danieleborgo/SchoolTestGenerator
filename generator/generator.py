import json
from generator.Student import translate_students
from generator.Test import Test
from pylatex import Document, Command, Package, NoEscape, NewPage
from pylatex.utils import bold


def generate_tests(students_file, test_file):
    students = translate_students(json.load(open(students_file)))
    test = Test(json.load(open(test_file)))

    doc = Document(documentclass='article')
    doc.packages.append(Package('fancyhdr'))
    doc.packages.append(Package('babel', test.get_language().lower()))
    doc.packages.append(Package('titlesec'))
    doc.preamble.append(Command('titlelabel', NoEscape('\\thetitle\\enspace')))

    for student in students:
        parse_student(doc, student, test)

    doc.generate_pdf(test.get_output_file_name(), clean_tex=False)


def parse_student(doc, student, test):
    reset_page_counter(doc)
    reset_section_counter(doc)

    set_header_and_footer(doc, test.get_date(), student)
    print_title(doc, test)

    doc.append(student.get_name())
    new_page(doc)


def set_header_and_footer(doc, date, student):
    doc.append(Command('fancyhf', ''))
    doc.append(Command('pagestyle', 'fancy'))
    doc.append(Command('lhead', NoEscape(bold(student.get_n()) + ' '
                                         + student.get_surname().upper() + ' ' + student.get_name().upper())))
    doc.append(Command('rhead', date))
    doc.append(Command('cfoot', Command('thepage')))


def print_title(doc, test):
    pass
    # TODO


def reset_page_counter(doc):
    doc.append(Command('setcounter', ['page', 1]))


def reset_section_counter(doc):
    doc.append(Command('setcounter', ['section', 0]))


def new_page(doc):
    doc.append(NewPage())
