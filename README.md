# Test Generator

<img width="" src="img/student.png" alt="" align="right"> 
This repository contains a program able to generate several school 
tests all different between them. The tests are thought to be printed
or to be sent to the students. There is no automatic correction,
since the answers may be directly written on paper.

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

The folder _json_ contains two JSON files that show completely all the
available features of this software.

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
- **_extra_point_** (optional): if set and true, it enable the 
generation of an extra point for answers graphical order and for the
rules respect.

### The parameter **_votes_**

This section is used to generate the table to convert earned points
to a vote in tenths. It is made by three parameters:

- **_min_**: this specifies the minimum allowed vote and its related
points through the fields **_vote_** and **_up_to_** inside of it.
- **_max_**: this specifies the maximum allowed vote and its related
points through the fields **_vote_** and **_from_** inside of it.
- **_int_** (optional): this flag forces the program to convert the votes
in integers.

The votes inside the two limiters are computed at runtime.

### The parameter **_arguments_**

This is the section that contains the real test and all its
questions. It is organized as an array of arguments, that represent
a big section, where each of them contains a set of questions.

An argument is composed by an **_argument_name_** and an array of
**_questions_**. Each question has these parameters:

- **_type_**: this defines the question category.
- **_text_**: this contains the question in form of string or in form
of strings array if the flag **_array_** is set to true. It can contain
several _%n_ that will be substituted with a random value chosen
according to the rules of the following point.
- **_values_**: this field, optional if the **_text_** doesn't contain
any **_%n_**, specifies the policies to follow for the value to 
substitute. For each token in the **_text_** it is necessary specify 
one policy. There are three policies, stored in the parameter **_type_**:
    - **_int_**: this generates an integer in the given interval 
    [**_min_**, **_max_**];
    - **_float_**: this generates a float in the given interval 
    [**_min_**, **_max_**] with the specified number of **_digits_**;
    - **_set_**: this specifies the value is picked randomly in a set,
    stored in the field **_set_**.
- **_optional_** (optional): declare the question as optional for the
students who need less questions.
- **_points_** (optional): define the value in points of the question
and, if not specified, its value is one.
- **_array_** (optional): if set and true it defines the field **_text_**
as an array of string the program will concatenate.