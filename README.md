# Test Generator

<img width="" src="images/student.png" alt="" align="right"> 
This repository contains a program able to generate several school 
tests all different between them. The tests are thought to be printed
or to be sent to the students. There is no automatic correction,
since the answers may be directly written on paper.

The **differences** in the tests consist in random numerical values or
random strings picked from a user defined set. The generated values
don't change if the program is run multiple times but they may change if
some basic data of the test is modified.

## Required installed software

This software was written using **Python 3.6** with the package
**PyLaTex**. It also requires an installed version of **LaTex**,
which has to have downloaded all the necessary packages.

## How to run

This program needs two files in input:

- A JSON file containing all the information related to the students;
- A JSON file containing all the information related to the test.

These two should be passed as parameter to the file _main.py_:

    python main.py students.json test.json
    
The used interpreter should have installed all the required Python
packages. The names are only symbolic.

This software was developed using PyCharm, which can 
simplify the execution and the package installation of this software.

## Example of use

The folder [sample](./sample) contains two JSON files that show
completely all the available features of this software and an example
of the generated PDF file.

## How it works

This generator structure is generic and allows easy and fast
modification. It is made by a function that:

- Extracts the information from the tho JSONs, storing them is apposite
structures, decorating them with various data to improve the
performances;
- For each student, calls a proper function that generates a test
following school directives for different needs, as the school
established;
- Creates a file containing all the random values used in the test
in function of each student, in order to simplify correction.

The function that generates a single test in function of the student
calls other ones, specific for this type of test. In order to change the
behaviour of the generator, it's necessary modifying these invocations.

Further information are given in the [generator package](./generator).

## How to create **_student.json_**

This file is made by an array containing all the students data in form
of objects. These lasts have these fields: **_name_**, **_surname_** and
**_type_**. The types modify the behaviour of the generation in function
of the student needs, in order to follow the directives the school
decided for each situation. The allowed types are: **_more_time_**, 
**_optional_questions_**, **_allow_notes_** and, obviously, 
**_standard_**. If not specified, the student is assumed to have a 
standard test.

## How to create **_text.json_**

This file has a lot of parameters, these are the single value ones:

- **_subject_**: this contains the school subject name;
- **_subtitle_**: this contains the test argument;
- **_language_**: this is the language of the LaTex document;
- **_class_**: this is the class which the students belong to;
- **_years_**: this is the class school year;
- **_date_**: this is the test date;
- **_duration_**: this is the standard test duration;
- **_more_time_duration_** (optional): this is the duration for the
students who need more time and it is equal to the previous if not
specified.
- **_extra_point_** (optional): if set and true, it enables the 
generation of an extra point for answers graphical order and for the
rules respect;
- **_extra_params_** (optional): this field contains an array of string,
representing some external things to evaluate for giving the grade,
like homework or projects.

### The parameter **_votes_**

This section is used to generate the table to convert earned points
to a vote in tenths. It is made by three parameters:

- **_min_**: this specifies the minimum allowed vote and its related
points through the fields **_vote_** and **_up_to_** inside of it.
- **_max_**: this specifies the maximum allowed vote and its related
points through the fields **_vote_** and **_from_** inside of it.

The votes inside the two limiters are computed at runtime.

### The parameter **_arguments_**

This is the section that contains the real test and all its
questions. It is organized as an array of arguments, that represent
a big section, where each of them contains a set of questions.

An argument is composed by an **_argument_name_** and an array of
**_questions_**. These lasts can be of a lot of types, according to
what the apposite parameter specifies, consequently they may have
different fields. These are all in common:

- **_type_**: this defines the question category.
- **_optional_** (optional): declare the question as optional for the
students who need less questions.
- **_points_** (optional): define the value in points of the question
and, if not specified, its value is one.

#### The types **_no_space_question_** and types **_spaced_question_**

These two types indicate simple open questions where the student has to
write the answer. The only difference between these two is that the 
second provide an additional space under the question, while the first
not. These two have in common these fields:

- **_text_**: this contains the question in form of string or in form
of strings array if the flag **_array_** is set to true. It can contain
several **_%n_** that will be substituted with a random value chosen
according to the rules of the following point.
- **_values_**: this field, optional if the **_text_** doesn't contain
any **_%n_**, specifies the policies to follow for the value to 
substitute. For each token in the **_text_** it is necessary specify 
one policy. There are three policies, stored in the parameter 
**_type_**:
    - **_int_**: this generates an integer in the given interval 
    [**_min_**, **_max_**];
    - **_float_**: this generates a float in the given interval 
    [**_min_**, **_max_**] with the specified number of **_digits_**;
    - **_set_**: this specifies the value is picked randomly in a set,
    stored in the field **_set_**.
- **_array_** (optional): if set and true it defines the field
**_text_** as an array of string the program will concatenate.
    
The type **_spaced_question_** requires an additional field named 
**_row_** where it's necessary specify an integer number of rows to
leave for the answer.

## How to add standard stuff

### Adding a new question type

The first thing to do is to add it in the **_QuestionType_** enum in
[enums.py](./generator/enums.py), then explain to the program how to
parse it. Consequently, in the class **_Question_** in
[Argument.py](./generator/Argument.py), the constructor offers a simple
way to add it, using its if structure. In the if code it's possible 
parsing new JSON fields but it's mandatory to set the field
**_\_\_print_question_** with a method takes as parameters an enum and
a student's type that prints in the enum the question. The second
parameter can be used if it's necessary differentiate the question
according to the student's type. It's important remember to specify the
points value and if the question is mandatory or less in the generation.
The two already implemented question can be an example.

### Adding a new student's type

After adding it in **_StudentType_** in 
[enums.py](./generator/enums.py), the next step strictly depends on 
which is the effect of this new category. All the questions, before
being generated, receive the student's type as parameter and this can be
exploited to generate different version of the question, like it happens
for the students that need optional question. Some functions, like the
one that generates the rules, receive the student's type as parameter.

### Adding a new grades format

In [test_support.py](./generator/test_support.py), in the last rows,
there is an object that translates a float vote in a more conventional
representation. Modifying that, the program would be able to support
other types of grades.

### Adding a new language

Adding a new language it's pretty easy, since it's only necessary to
create a properties file, naming it with the language of reference,
putting it in the _languages_ folder and then translate all the
sentences. After this modification, the two JSON files can be written
directly in the new language, the program'll automatically adapt to it.

The string used to specify the language for the properties file is also
used to specify it for the Latex file.

### Adding a new sentence

After having put the new properties in the apposite file, it has to be
imported as a constant in the [sentences.py](./generator/sentences.py)
file. Then, it can be used as the other ones. The only drawback is
that, after having added a new sentence to the Python file, the program
 will require it for all the languages.