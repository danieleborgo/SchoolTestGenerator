# Package generator

Here is contained all the codes used for the generation.

## Index

1. [enums.py](#1-enumspyenumspy)
2. [generator.py](#2-generatorpygeneratorpy)
3. [Student.py](#3-studentpystudentpy)
4. [Test.py](#4-testpytestpy)
5. [Argument.py](#5-argumentpyargumentpy)
6. [test_support.py](#6-test_supportpytest_supportpy)
7. [Sentences.py](#7-sentencespysentencespy)

## 1. [enums.py](./enums.py)

This file contains two enums:

- **_StudentType_**: useful to determine a category where the student
belongs, in order to specify his or her needs in the test. According 
to students needs, this software supports people who need more time,
who need optional questions or who need the permission to use notes.
- **_QuestionType_**: useful to define the category of the questions.
Actually, two simple questions are supported, but can be easily
extended to support more.

## 2. [generator.py](./generator.py)

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

## 3. [Student.py](./Student.py)

This file contains a class representing a single student.
It is composed by a name, by a surname, by a register number and by
a type (_StudentType_). 

There is also a function able to convert the file _student.json_ in
an array of Students instances.

## 4. [Test.py](./Test.py)

This class contains the class used to optimize the test generator. It
extracts all the data from the JSON and, eventually, it completes the
optional parameters with default values. If it's necessary add further
parameters in the JSON, this is the place where they have to be parsed.

The used term _optimization_ is not meant regarding to the execution time
but to the avoidance of _spaghetti code_.

## 5. [Argument.py](./Argument.py)

The class **_Argument_** represents the JSON parameter equivalent and
contains a group of questions.

The class **_Question_** represent, obviously, a simple question and 
all its related data, like points and random values handler, managed
through **_RandomHandler_**.

## 6. [test_support.py](./test_support.py)

The classes **_PointsData_** and **_VotesData_** optimize their table
generation.

## 7. [Sentences.py](sentences.py)

This file is used to import strings in different languages. It contains
several constants, grouped in objects, that are filled at runtime
extracting them from the passed properties file.