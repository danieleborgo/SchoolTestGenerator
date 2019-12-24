import sys
from generator.generator import generate_tests

if __name__ == '__main__':
    print("TEST GENERATOR")

    if len(sys.argv) < 2:
        raise Exception("Two parameters are requested")
    else:
        generate_tests(
            students_file_name=sys.argv[1],
            test_file_name=sys.argv[2]
        )
