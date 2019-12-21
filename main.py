from generator.generator import generate_tests
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: two parameters are requested")
    else:
        generate_tests(
            students_file_name=sys.argv[1],
            test_file_name=sys.argv[2]
        )
