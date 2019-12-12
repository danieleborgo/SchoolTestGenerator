from generator.generator import generate_tests
import sys

if __name__ == '__main__':
    generate_tests(
        students_file=sys.argv[1],
        test_file=sys.argv[2]
    )
