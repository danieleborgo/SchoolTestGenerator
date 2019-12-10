import json
from generator.Student import translate_students
from pylatex import Document, Command, Package, NoEscape, NewPage
from pylatex.utils import bold


def generate_tests(students_file, test_file):
    students = translate_students(json.load(open(students_file)))
    test_json = json.load(open(test_file))

    doc = Document(documentclass='article')
    doc.preamble.append(Package('fancyhdr'))
    doc.packages.append(Package('titling'))
    doc.packages.append(Package('babel', test_json['language'].lower()))

    for student in students:
        parse_student(doc, student, test_json['date'])

    doc.generate_pdf(test_json['subtitle'] + '_' + test_json['class'], clean_tex=False)


def parse_student(doc, student, date):
    reset_page_counter(doc)
    reset_section_counter(doc)
    set_header_and_footer(doc, date, student.get_surname(), student.get_name())

    doc.append(student.get_name())
    new_page(doc)


def set_header_and_footer(doc, date, surname, name):
    doc.append(Command('pagestyle', 'fancy'))
    doc.append(Command('fancyhf', ''))
    doc.append(Command('lhead', NoEscape('Cognome: ' + surname.upper() + ' Nome ' + name.upper())))
    doc.append(Command('rhead', date))
    doc.append(Command('cfoot', NoEscape('\\thepage')))


def reset_page_counter(doc):
    doc.append(Command('setcounter', ['page', 1]))


def reset_section_counter(doc):
    doc.append(Command('setcounter', ['section', 0]))


def new_page(doc):
    doc.append(NewPage())
