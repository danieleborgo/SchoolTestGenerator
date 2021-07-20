# Package generator

In this package there are all the codes used for the generation.

## Index

1. [The package test](#1-the-package-testtest)
   
    1.1. [Argument.py](#11-argumentpytestargumentpy)
    
    1.2. [Question.py](#12-questionpytestquestionpy)
    
    1.3. [Test.py](#13-testpytesttestpy)
    
    1.4. [test_support.py](#14-test_supportpytesttest_supportpy)
    
    1.5. [TestLogger.py](#15-testloggerpytesttestloggerpy)

2. [enums.py](#2-enumspyenumspy)
3. [generator.py](#3-generatorpygeneratorpy)
4. [Sentences.py](#4-sentencespysentencespy)
5. [User.py](#5-userpyuserpy)

## 1. The package [test](./test)

This package contains all the classes and all the functions needed to
interpret and reorganize the data for generating the tests.

### 1.1. [Argument.py](./test/Argument.py)

The class **_Argument_** represents the JSON parameter equivalent and
contains a group of questions in form of _Question_ instances.

### 1.2. [Question.py](./test/Question.py)

The class **_Question_** represent, obviously, a simple question and 
all its related data, like points and random values handler, managed
through **_RandomHandler_**.

### 1.3. [Test.py](./test/Test.py)

This file contains the class used to optimize the test generation. It
extracts all the data from the JSON and, eventually, it completes the
optional parameters with default values. If it's necessary to add further
parameters in the JSON, this is the place where they have to be parsed.

The term _optimization_ does not refer to the code's execution
time but to the avoidance of _spaghetti code_.

### 1.4. [test_support.py](./test/test_support.py)

The classes **_PointsData_** and **_VotesData_** optimize their table
generation.

### 1.5. [TestLogger.py](./test/TestLogger.py)

At the end of each generation, a logger is generated using the data
stored in this class.

## 2. [enums.py](./enums.py)

This file contains two enums:

- **_Modifier_**: useful to define some modifications in order to 
adapt the test specifically for the student's needs in the test. According 
to these needs, this software supports people who need more time,
optional questions or the permission to use notes.
- **_QuestionType_**: useful to define the category of the questions.
Actually, two simple questions are supported, but can be easily
extended to support more.

## 3. [generator.py](./generator.py)

This is the main core of the software and contains the function that
takes as parameters some JSONs and generates the document. This
translates these files in objects able to optimize the generation
and then iterates on the users' array, generating one test at a time,
invoking a proper function. This function is also responsible to collect
all the random values generated and to save them in a specific file in
order to easy out the correction. This function's named 
**_generate_tests_**.

The function invoked to generate a single test contains several calls
to specific other functions that generate all the elements in a page
and this should be the one that requires to be modified if a different
format test is requested. It's named **_generate_test_single_user_**.

## 4. [Sentences.py](sentences.py)

This file is used to import strings in different languages. It contains
several constants grouped in objects, that are filled runtime
extracting them from the passed properties file. This program doesn't
support the generation of tests in different languages at the same time.
For doing this, it's necessary to create multiple _test.json_ configured
in different languages.

## 5. [User.py](User.py)

This file contains the classes representing a single user. These can
be of two types as defined in the main repository README: students and
anonymous users. The firsts are composed by a name, by a surname, 
by a register number and by a tuple of modifiers (_Modifiers_). The
seconds don't have names, so they require just the modifiers.

There are also a functions able to convert the files _student.json_
and _anonymous_users.json_ in a tuple of users.