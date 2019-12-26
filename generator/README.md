# Package generator

Here is contained all the codes used for the generation.

## [enums.py](./enums.py)

This file contains two useful enums:

- **_StudentType_**: useful to determine a category where the student
belongs, in order to specify his or her needs in the test. According 
to students needs, this software supports people who need more time,
who need optional questions or who need the permission to use notes.
- **_QuestionType_**: useful to define the category of the questions.
Actually, only simple questions are supported, but can be easily
extended to support more.

## [generator.py](./generator.py)

This is the main core of the software and contains the function that
takes as parameters the two JSONs and generates the document. This
translates the two files in objects able to optimize the generation
and then iterates on the students array, generating one test per time,
invoking a proper function. This function is also responsible to collect
all the random values generated and to save them in a specific file in
order to make easier the correction. This function's named 
**_generate_tests_**.

The function invoked to generate a single test contains several calls
to  specific other functions that generate all the elements in a page
and this should be the one that requires to be modified if a different
format test is requested. It's named **_parse_student_**.

## [Student.py](./Student.py)

This file contains a class supposed to represent a single student.
It is composed by a name, by a surname, by a register number and by
a type (_StudentType_). 

There is also a function able to convert the file _student.json_ in
an array of Students instances.

## [Test.py](./Test.py)

This class contains the class used to optimize the test generator. It
extracts all the data from the JSON and, eventually, it completes the
optional parameters with default values. If it's necessary add further
parameters in the JSON, this is the place where they have to be parsed.

## [Argument.py](./Argument.py)

The class **_Argument_** represents the JSON parameter equivalent and
contains a group of questions

The class **_Question_** represent, obviously, a simple question and 
all its related data, like points and random values handler, managed
through **_RandomHandler_**.

## [test_support.py](./test_support.py)

The classes **_PointsData_** and **_VotesData_** optimize their
table generation.