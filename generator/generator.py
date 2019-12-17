import json
from generator.Student import translate_students
from generator.Test import Test
from generator.enums import TYPE
from pylatex import *
from pylatex.utils import bold


def generate_tests(students_file, test_file):
    students = translate_students(json.load(open(students_file)))
    test = Test(json.load(open(test_file)))

    doc = Document(documentclass='article')
    doc.packages.append(Package('fancyhdr'))
    doc.packages.append(Package('babel', test.get_language().lower()))
    doc.packages.append(Package('titlesec'))
    doc.preamble.append(Command('titlelabel', NoEscape('\\thetitle\\enspace')))
    doc.append(Command('fontsize', arguments=['9', '9']))
    doc.packages.append(Package('geometry', 'top=3cm, left=3cm, right=3cm, bottom=2cm'))

    for student in students:
        parse_student(doc, student, test)

    doc.generate_pdf(test.get_output_file_name(), clean_tex=False)


def parse_student(doc, student, test):
    reset_page_counter(doc)
    reset_section_counter(doc)

    set_header_and_footer(doc, test.get_date(), test.get_class(), test.get_years(), student.get_n())
    print_figures(doc)
    print_student_name(doc, student)
    print_title(doc, test)

    doc.append(Command('section*', 'Regolamento'))
    print_rules(doc, test.get_duration(student.get_student_type()), student.get_student_type())

    doc.append(Command('section*', 'Valutazione'))
    print_evaluation_rule_exercise(doc)
    print_points_to_vote_table(doc, test.get_votes_data())
    print_earned_points_table(doc, test.get_points_data())

    new_page(doc)


def set_header_and_footer(doc, date, test_class, years, n):
    doc.append(Command('fancyhf', ''))
    doc.append(Command('pagestyle', 'fancy'))
    doc.append(Command('lhead', NoEscape(bold(n))))
    doc.append(Command('chead', test_class + ' (' + years + ')'))
    doc.append(Command('rhead', date))
    doc.append(Command('cfoot', Command('thepage')))


def print_figures(doc):
    with doc.create(Figure(position='h!')) as figure:
        with doc.create(SubFigure(
                position='b',
                width=NoEscape(r'0.5\linewidth'))) as left_figure:
            left_figure.add_image('./img/logo.png')
        with doc.create(SubFigure(
                position='b',
                width=NoEscape(r'0.5\linewidth'))) as right_figure:
            right_figure.add_image('./img/pon.png')


def print_student_name(doc, student):
    with doc.create(LongTable('l l', col_space='0.6cm', row_height=2.0)) as table:
        table.add_row(['Cognome', bold(student.get_surname().upper())])
        table.add_row(['Nome', bold(student.get_name().upper())])


def print_title(doc, test):
    # Using Latex title would have limited the program
    with doc.create(Center()) as center:
        center.append(Command('large'))
        center.append(bold(test.get_subject().upper()))
    with doc.create(Center()) as center:
        center.append(test.get_subtitle())


def print_rules(doc, duration, type):
    with doc.create(Itemize()) as itemize:
        itemize.add_item("Il tempo a disposizione è di " + str(duration) + " minuti.")
        itemize.add_item("Non è permesso l'uso di dispositivi elettronici al di fuori della calcolatrice.")
        itemize.add_item("Non è permesso parlare o alzarsi durante la verifica.")
        if type != TYPE.ALLOW_NOTES:
            itemize.add_item("Non è permesso l'uso degli appunti o del libro.")
        else:
            itemize.add_item("Lo studente è autorizzato ad usare i suoi appunti ma non il libro.")


def print_evaluation_rule_exercise(doc):
    doc.append('Tabella di valutazione degli esercizi:')
    with doc.create(LongTable(NoEscape('p{0.05\\textwidth}|p{0.81\\textwidth}'), row_height=1.5)) as ex_table:
        ex_table.add_row([bold('100%'), 'Lo svolgimento è completo e corretto, con linguaggio pertinente.'])
        ex_table.add_row([bold('75%'), 'Lo svolgimento è incompleto, lievemente errato o con linguaggio impreciso.'])
        ex_table.add_row([bold('50%'), 'Lo svolgimento è incompleto, superficiale, ' +
                                       'con errori diffusi o con linguaggio incerto.'])
        ex_table.add_row([bold('25%'),  'Lo svolgimento manca di molte parti, presenta errori gravi ' +
                                        'o con linguaggio molto insicuro.'])


def print_points_to_vote_table(doc, votes_data):
    with doc.create(LongTable(votes_data.get_table_string(), row_height=1.5)) as votes_table:
        votes_table.add_hline()
        votes_table.add_row(votes_data.get_points())
        votes_table.add_hline()
        votes_table.add_row(votes_data.get_votes())
        votes_table.add_hline()


def print_earned_points_table(doc, points_data):
    with doc.create(LongTable(points_data.get_table_string(), row_height=2.0)) as eval_table:
        eval_table.add_hline()
        eval_table.add_row(points_data.get_questions_numbers())
        eval_table.add_hline()
        eval_table.add_empty_row()
        eval_table.add_hline()

    with doc.create(LongTable('l l', col_space='0.5cm')) as eval_table:
        eval_table.add_row(['Punteggio totale: ', '__________'])
        eval_table.add_row(['Voto: ', '__________'])


def reset_page_counter(doc):
    doc.append(Command('setcounter', ['page', 1]))


def reset_section_counter(doc):
    doc.append(Command('setcounter', ['section', 0]))


def new_page(doc):
    doc.append(NewPage())
