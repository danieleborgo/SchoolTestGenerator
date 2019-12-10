from generator.generator import generate_tests

if __name__ == '__main__':
    generate_tests(
        students_file='json/students.json',
        test_file='json/test.json'
    )
