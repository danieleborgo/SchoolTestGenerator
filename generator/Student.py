from generator.enums import StudentType


class Student:
    """
        This class represents a single student with all the
        related information.
    """
    def __init__(self, register_number, name, surname, student_type):
        self.__register_number = register_number
        self.__name = name
        self.__surname = surname
        self.__student_type = student_type

    def get_register_number(self):
        return self.__register_number

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_student_type(self):
        return self.__student_type

    def do_you_want_optional(self):
        return StudentType.OPTIONAL_QUESTIONS == self.__student_type


def translate_students(students_json):
    """
        This function translates an array of JSON students in an array
        of instances of ste Student object
    """
    students = []

    for i in range(len(students_json)):
        student_type = StudentType.STANDARD
        if 'type' in students_json[i]:
            student_type = StudentType.translate_type(students_json[i]['type'])

        students.append(
            Student(i+1, students_json[i]['name'], students_json[i]['surname'], student_type)
        )

    return students
