# School Test Generator

<img width="" src="images/student.png" alt="" align="right"> 
This software is able to generate several school tests, all different
from each other, created using two configuration files, which grant
flexibility to the program. These are made to be printed or sent via
mail to the students, since they're created thinking about written
school tests. As a consequence no automatic correction was developed,
since the answers may be given on paper or through various specific 
files to deliver.

The **differences** in the tests consist in random numerical values or
random strings picked from a user defined set. The generated values
don't change if the program is executed multiple times but they may
change if some basic data of the test is modified.

## Index

1. [Required installed software](#1-required-installed-software)
2. [How to run](#2-how-to-run)
3. [Example of use](#3-example-of-use)
4. [How it works](#4-how-it-works)
5. [How to create _student.json_](#5-how-to-create-_studentjson_)
6. [How to create _text.json_](#6-how-to-create-_textjson_)
    
    6.1. [The parameter _votes_](#61-the-parameter-_votes_)
    
    6.2. [The parameter _arguments_](#62-the-parameter-_arguments_)

7. [How to add standard stuff](#7-how-to-add-standard-stuff)

    7.1. [Adding a new question type](#71-adding-a-new-question-type)
    
    7.2. [Adding a new student's type](#72-adding-a-new-students-type)
    
    7.3. [Adding a new grades format](#73-adding-a-new-grades-format)
    
    7.4. [Adding a new language](#74-adding-a-new-language)
    
    7.5. [Adding a new sentence](#75-adding-a-new-sentence)
    
    7.6. [Adding new test rules](#76-adding-new-test-rules)
    
8. [Author](#8-author)
9. [License](#9-license)

## 1. Required installed software

This software was written using **Python 3.6** with the package
**PyLaTex**. It also requires an installed version of **LaTex**,
which has to have downloaded all the necessary packages. One of the
major source of errors in the first execution is the lack of some LaTex
packages or, in some version, of the Perl language installed on
Windows.

## 2. How to run

This program needs two JSON file names in input:

- A JSON file containing all the information related to the students;
- A JSON file containing all the information related to the test.

These two should be passed as parameter to the file _main.py_:

    python main.py students.json test.json
    
The used interpreter has to have installed all the required Python
packages. The names are only symbolic.

This software was developed using PyCharm, which can simplify the
execution and the package installation of this software.

## 3. Example of use

The folder [sample](./sample) contains two JSON files that show
completely all the available features of this software and an example
of the generated PDF file.

## 4. How it works

This generator structure is generic and allows easy and fast
modification directly in the code. Its main core is represented by a
function that does these operations:

- It extracts the information from the tho JSONs, storing them is 
apposite structures, decorating them with various data in order to
avoid endless nested sequences of _ifs_.
- For each student, it calls a proper function that generates a test
following school directives regarding her or his different needs.
- It creates a file containing all the random values used in the test
in function of each student, in order to simplify correction.

The function that generates a single test in function of the student
calls other ones, specific for this type of test. In order to change
the behaviour of the generator, it's necessary modifying these
invocations.

Further and detailed information are given in the 
[generator package](./generator).

## 5. How to create **_student.json_**

This file contains all the information related to the students,
represented by objects in an array. These are composed by three fields:
**_name_**, **_surname_**, and **_mod_**. This last modifies the
behaviour of the generation in function of the student needs, in order
to follow the directives the school decided for each situation. The
allowed modifiers are:  **_more_time_**,  **_optional_questions_**,
**_allow_notes_**. They can be expressed through an array,
independently by their quantity, of through a direct specification if
just one is required.

## 6. How to create **_text.json_**

This file contains all the data regarding the school test, consequently
it has a lot of parameters, these are the single value ones (if not
specified, they're strings):

- **_subject_**: this contains the school subject name;
- **_subtitle_**: this contains the test argument;
- **_language_**: this is the language of the document and it is used
to import the related properties file;
- **_class_**: this is the class which the students belong to;
- **_years_**: this is the class school year;
- **_date_**: this is the test date;
- **_duration_** (_int_): this is the standard test duration in
minutes;
- **_more_time_duration_** (optional, _int_): this is the duration for
the students who need more time and it is set equal to the previous if
not specified.
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
the grade, like homework or projects.

### 6.1. The parameter **_votes_**

This section is used to generate the table to convert earned points
to a vote in tenths. It is made by three parameters:

- **_min_** (_int_): this specifies the minimum allowed vote and its
related points through the fields **_vote_** and **_up_to_** inside of
it.
- **_max_** (_int_): this specifies the maximum allowed vote and its
related points through the fields **_vote_** and **_from_** inside of
it.

The intermediate votes inside the two limiters are computed at runtime.

### 6.2. The parameter **_arguments_**

This is the section that contains the real test and all its questions.
It is organized as an array of arguments, which represent a big
section, where each of them contains a set of questions.

An argument is composed byan **_argument_name_** and an array of
**_questions_**. These lasts can be of a lot of types, according to
what the apposite parameter specifies, consequently they may have
different fields. These are the ones in common:

- **_type_**: this defines the question category;
- **_optional_** (optional, _boolean_): declares the question as
optional for the students who need less questions;
- **_points_** (optional, _int_): define the value in points of the
question and, if not specified, its value is one.

If the argument has a description, this can be set through 
**_argument_text_**. If it's necessary to shuffle the questions
in an argument, the flag **_shufle_** has to be set to true. These
fields are both optional.

#### The types **_no_space_question_** and types **_spaced_question_**

These two types indicate simple open questions where the student has to
write the answer. The only difference between these two is that the 
second provide an additional space under the question, while the first
not. These two have in common these fields:

- **_text_**: this contains the question in form of string or in form
of strings array if the flag **_array_** is set to true. It can contain
several **_%n_** that will be substituted with a random value chosen
according to the rules of the following point.
- **_values_** (_array_): this field, optional if the **_text_**
doesn't contain any **_%n_**, specifies the policies to follow for the
value to  substitute. For each token in the **_text_** it is necessary
specify one policy. There are three policies, stored in the parameter 
**_type_**:
    - **_int_**: this generates an integer in the given interval 
    [**_min_**, **_max_**];
    - **_float_**: this generates a float in the given interval 
    [**_min_**, **_max_**] with the specified number of **_digits_**;
    - **_set_**: this specifies the value is picked randomly in a set,
    stored in the array field **_set_**.
- **_array_** (optional, _boolean_): if set and true it defines the
field **_text_** as an array of strings that the program will
concatenate.
    
The type **_spaced_question_** requires an additional integer field
named  **_row_** where it's necessary specify an integer number of rows
to leave for the answer.

## 7. How to add standard stuff

Here there are some explanations on how to extend the software for the
most common needs.

### 7.1. Adding a new question type

The first thing to do is to add it in the **_QuestionType_** enum in
[enums.py](./generator/enums.py), then to explain to the program how to
parse it. Consequently, in the class **_Question_** in
[Argument.py](./generator/Argument.py), the constructor offers a simple
way to add it, using its _ifs_ structure. In the constructor it's
possible  parsing new JSON fields but it's mandatory to set the field
**_\_\_print_question_** with a method takes as parameters an enum and
a student's type that prints in the enum the question. The second
parameter can be used if it's necessary differentiate the question
according to the student's type. It's important remember to specify the
points value and if the question is mandatory or less in the
generation. The two already implemented question can be an example.

### 7.2. Adding a new modifiers

After adding it in **_Modifier_** in [enums.py](./generator/enums.py),
the next step strictly depends on which is the effect of this new
modifier. All the questions, before being generated, can receive 
some flags related to these as parameter and this can 
be exploited to generate different versions of the question, like it
happens for the students that need optional questions.

### 7.3. Adding a new grades format

In [test_support.py](./generator/test_support.py), in the last rows,
there is an object that translates a float vote in a more conventional
representation. Modifying that, the program would be able to support
other types of grades.

### 7.4. Adding a new language

Adding a new language it's pretty easy, since it's only necessary to
create a properties file, naming it with the language of reference,
putting it in the _languages_ folder and then translating all the
sentences. After this modification, the two JSON files can be written
directly in the new language, the program'll automatically adapt to it.

The string used to specify the language for the properties file is also
used to specify it for the Latex file.

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

This software was developed by Borgo Daniele in _range(2019, 2021)_.

## 9. License

This software is distributed on GPLv3.0, more information available
in [LICENSE.md](./LICENSE.md).