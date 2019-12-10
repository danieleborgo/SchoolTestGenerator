from generator.enums import TYPE


class Student:
    def __init__(self, n, name, surname, student_type):
        self.__n = n
        self.__name = name
        self.__surname = surname
        self.__student_type = student_type

    def get_n(self):
        return self.__n

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_student_type(self):
        return self.__student_type


def translate_students(students_json):
    students = []

    for i in range(len(students_json)):
        student_type = TYPE.STANDARD
        if 'type' in students_json[i]:
            student_type = TYPE.translate_type(students_json[i]['type'])

        students.append(
            Student(i, students_json[i]['name'], students_json[i]['surname'], student_type)
        )

    return students
