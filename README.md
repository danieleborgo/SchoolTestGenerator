# School Test Generator

<img width="" src="images/student.png" alt="" align="right"> 
This software is able to generate several school tests, all different
from each other and created from two different configuration files,
which grant flexibility to the program. These are made to be printed
or sent via mail to the students, since these files are thought to 
create written school tests. As a consequence no automatic correction
was developed, since the answers may be given on paper or through 
various specific files to deliver.

The **differences** in the tests consist in random numerical values or
random strings picked from a user-defined set. The generated values
don't change if the program is executed multiple times but they may
change if some basic data of the test are modified.

## Index

1. [Required installed software](#1-required-installed-software)
2. [How to run](#2-how-to-run)
3. [Example of use](#3-example-of-use)
4. [How it works](#4-how-it-works)
5. [How to create **_users.json_**](#5-how-to-create-_usersjson_)
   
   5.1. [**_students.json_**](#51-_studentsjson_)
   
   5.2. [**_anonymous_users.json_**](#52-_anonymous_usersjson_)
   
6. [How to create _text.json_](#6-how-to-create-_textjson_)
    
    6.1. [The parameter _votes_](#61-the-parameter-_votes_)
    
    6.2. [The parameter _arguments_](#62-the-parameter-_arguments_)

7. [How to add standard stuff](#7-how-to-add-standard-stuff)

    7.1. [Adding a new question type](#71-adding-a-new-question-type)
    
    7.2. [Adding a new student's type](#72-adding-a-new-modifier)
    
    7.3. [Adding a new grades format](#73-adding-a-new-grades-format)
    
    7.4. [Adding a new language](#74-adding-a-new-language)
    
    7.5. [Adding a new sentence](#75-adding-a-new-sentence)
    
    7.6. [Adding new test rules](#76-adding-new-test-rules)
    
8. [Author](#8-author)
9. [License](#9-license)

## 1. Required software

This software was written using **Python 3.8** with the package
**PyLaTeX**. It also requires an installed version of **LaTeX**,
which has to have all the necessary packages downloaded. One of the
major source of errors in the first execution is the lack of some
LaTeX packages or, in some version, of the Perl language installation.

In case the user doesn't want to install LaTeX, the program works
anyway generating just the _.tex_ file, which can then be compiled
through, for instance, [Overleaf](https://www.overleaf.com/).

## 2. How to run

This program needs two JSON file names in input:

- A JSON file containing all the information related to the users;
- A JSON file containing all the information related to the test.

There are two types of users:

- Named users: in this case the tests will be generated with the
students name fields already compiled;
- Anonymous users: the tests name fields will be left blank,
so they will be filled by hand.

This is the command structure to execute the program, given _-h_ as
parameter:

    usage: main.py [-h] [-s STUDENTS_PATH | -a USERS_PATH] TEST_PATH

The argument _TEST_PATH_ indicates the path where the test JSON 
configuration file is located, while STUDENTS_PATH and USERS_PATH
define the ones related to the users' file.
Because of this definition, the program is able to generate one
type at once.

The used interpreter has to have installed all the required Python
packages.

## 3. Example of use

The folder [sample](./sample) contains some JSON files that show
all the available features of this software and two examples of
the generated PDF files.

## 4. How it works

This software's structure is generic and allows easy and fast
modification directly in the code. Its main core is represented by a
function that does these operations:

- It extracts the information from the two JSONs, storing them in 
apposite structures and decorating them with various data in order to
avoid endless nested sequences of _ifs_.
- For each student, it calls a proper function that generates a single
test following school directives regarding their different needs.
- It creates a different file containing all the random values used 
in the test for each student, in order to simplify correction.

The function that generates a single test in function of the student
calls other ones, specific for this type of test. In order to change
the behaviour of the generator, it's necessary to modify these
invocations.

In case the anonymous users are requested, the program follows the
same points defined before, but it avoids the completion of the name 
fields. With this configuration is possible to generate different
tests according to various special needs.

Further and detailed information are given in the 
[generator package](./generator).

## 5. How to create **_users.json_**

### 5.1 **_students.json_**

This file contains all the information related to the students,
represented as objects in an array. These are composed by three
fields: **_name_**, **_surname_**, and **_mod_**. This last modifies
the behaviour of the generation in function of the student needs, in
order to follow the directives the school decided for each situation.
The allowed modifiers are:  **_more_time_**,  **_optional_questions_**,
**_allow_notes_** and **_bigger_font_**. They can be expressed
through an array, independent by their quantity, or through a direct 
specification if just one is required. This is an example of a 
student:

    {
        "name": "Hello",
        "surname": "World",
        "mod": "more_time"
    }

### 5.2 **_anonymous_users.json_**

This file works similarly to the previous one; the only difference is
that the names and the surnames are not specified. This is an example
of an anonymous student without modifiers:

    {
        # No data is needed
    }

## 6. How to create **_text.json_**

This file contains all the configurations referring to the school test, 
consequently it has a lot of parameters, these are the single value
ones (if not specified, they're strings):

- **_subject_**: this contains the school subject's name;
- **_subtitle_**: this contains the test's argument;
- **_language_**: this is the language of the document and it is used
to import the related properties file;
- **_class_**: this is the class which the students belong to;
- **_years_**: this is the current academic year;
- **_date_**: this is the test date;
- **_logo_**: this is the school logo path;
- **_duration_** (_int_): this is the standard test duration in
minutes;
- **_more_time_duration_** (optional, _int_): this is the duration for
the students who need more time and it is set equal to the previous if
not specified;
- **_extra_point_** (optional, _boolean_): if set and true, it enables
the  generation of an extra point for answers graphical order and for
the rules respect;
- **_open_book_** (optional, _boolean_): if set and true, the software
prints the rule allows the use of notes and books;
- **_single_files_** (optional, _boolean_): if this is set true, the
program generates one PDF for each student instead of a single file
containing all the tests;
- **_out_folder_**: (optional, _string_) this is the directory where
all the files have to be placed and, if not set, it uses the actual one;
- **_extra_params_** (optional, _array_): this field contains an array
of strings, representing some external things to evaluate for giving
the grade, like homework or projects;
- **_test_**: (array) this is the part that contains the questions and
it's implemented as a list of _argument_ object, defined later in
subsection [6.2](#62-the-parameter-_arguments_).

This is an example of these parameters, except for _test_:

    "subject": "Test subject",
    "subtitle": "Subtitle",
    "language": "English",
    "class": "class name",
    "years": "2019 - 2020",
    "date": "13/12/2019",
    "logo": "../images/school_logo.png",
    "duration": 60,
    "more_time_duration": 70,
    "extra_point": true,
    "open_book": false,
    "single_files": false,
    "out_folder": "sample",
    "extra_params": ["Project"]

### 6.1. The parameter **_votes_**

This section is used to generate the table to convert earned points
to a vote in tenths. It is composed of two parameters:

- **_min_** (_int_): this specifies the minimum allowed vote and its
related points through the fields **_vote_** and **_up_to_** inside of
it.
- **_max_** (_int_): this specifies the maximum allowed vote and its
related points through the fields **_vote_** and **_from_** inside of
it.

The intermediate votes inside the two limiters are computed runtime.

This example defines that the minimum grade is 2, gained with at most
two points, while the maximum is 10, gained with ten points or more.

    "votes": {
        "min": {
            "vote": 2,
            "up_to": 2
        },
        "max": {
            "vote": 10,
            "from": 10
        }
    }

### 6.2. The parameter **_arguments_**

This is the section that contains the real test and all its questions.
It is organized as an array of arguments, which represent a big
section, where each of them contains a set of questions.

An argument is composed by an **_argument_name_** and an array of
**_questions_**. These lasts can differ a lot from one another,
according on their apposite parameter's specifications, consequently
they may have different fields. These are the ones in common:

- **_type_**: this defines the question's category;
- **_optional_** (optional, _boolean_): declares the question as
optional for the students who need fewer questions;
- **_points_** (optional, _int_): defines the value in points of the
question and is set on one by default.

If the argument has a description, this can be set through 
**_argument_text_**. If it's necessary to shuffle the questions
in an argument, the flag **_shuffle_** has to be set to true. These
fields are both optional.

#### The types **_no_space_question_** and types **_spaced_question_**

These two types indicate simple open questions where the student has to
write the answer. The only difference between these is that the 
second provides an additional space under the question, while the first
one doesn't. These are the common fields:

- **_text_**: this contains the question in form of string or in form
of strings array. It can contain several **_%n_** that will be
substituted with a random value chosen according to the rules of the
following point.
- **_values_** (_array_): this field, optional if the **_text_**
doesn't contain any **_%n_**, specifies the policies to follow for the
value to  substitute. For each token in the **_text_** it is necessary
specify one policy. There are three policies, stored in the parameter 
**_type_**:
    - **_int_**: this generates an integer between the given interval 
    [**_min_**, **_max_**];
    - **_float_**: this generates a float between the given interval 
    [**_min_**, **_max_**] with the specified number of **_digits_**;
    - **_set_**: this specifies the value picked randomly in a set,
    stored in the array field **_set_**.

This is the code for generating a question containing a random int
and a random float. The first belongs to [0, 40] the second to 
[-10, -1] with two decimal digits.

    {
        "type": "no_space_question",
        "text": "int: %n, float %n",
        "values": [
            {
                "type": "int",
                "min": 0,
                "max": 40
            },
            {
                "type": "float",
                "min": -10,
                "max": -1,
                "digits": 2
            }
        ]
    }
    
The type **_spaced_question_** requires an additional integer field
named  **_row_** where the specification of an integer number of rows
to leave for the answer is necessary.

## 7. How to add standard stuff

Here there are some explanations on how to extend the software for the
most common needs.

### 7.1. Adding a new question type

The first thing to do is to add it in the **_QuestionType_** enum in
[enums.py](./generator/enums.py), then explain to the program how to
parse it. Consequently, in the class **_Question_** in
[Argument.py](generator/test/Argument.py), the constructor offers a
simple way to add it, using its _ifs_ structure. In the constructor
it's possible to parse new JSON fields but it's mandatory to set the
field **_\_\_print_question_** with an enum and a student's type that
prints in the enum the question as parameters. The second parameter
can be used if it's necessary differentiate the question according to
the student's type. It's important to remember that the specification
of the points value and if the question may be mandatory in the
generation. The two already implemented question can be an example.

### 7.2. Adding a new modifier

After adding it in **_Modifier_** in [enums.py](./generator/enums.py),
the next step strictly depends on which is the effect of this new
modifier. All the questions, before being generated, can receive 
some flags related to these as parameter and this can 
be exploited to generate different versions of the question,
in case there are students that need optional questions.

### 7.3. Adding a new grades format

In [test_support.py](generator/test/test_support.py), in the last rows,
there is an object that translates a float vote in a more conventional
representation. By modifying that, the program would be able to support
other types of grades.

### 7.4. Adding a new language

Adding a new language is pretty easy, since it's only necessary to
create a property file, naming it with the language of reference,
putting it in the _languages_ folder and then translating all the
sentences. After this modification, the two JSON files can be written
directly in the new language, the program will automatically adapt to it.

The string used to specify the language for the properties file is also
used to specify it for the LaTeX file.

### 7.5. Adding a new sentence

A sentence is a phrase used in the program that can be translated in
different languages. For adding a new one, after having put the new
properties in the apposite file, it has to be imported as a constant in
the [sentences.py](./generator/sentences.py) file. Then, it can be used
as the other ones. The only drawback is that, after having added a new 
sentence to the Python file, the program will require it for all the
languages.

### 7.6 Adding new test rules

In the _properties_ file, it's possible add new rules in the section
named _*UserRules*_. Their names are ignored by the program, they
only need to be disjoint.

## 8. Author

This software was developed by Borgo Daniele in _range(2019, 2021+1)_.

## 9. License

This software is distributed on GPLv3.0, more information available
in [LICENSE.md](./LICENSE.md).