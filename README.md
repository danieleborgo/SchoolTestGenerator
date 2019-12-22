# Test Generator

This repository contains a program able to generate several school 
tests all different between them. The tests are thought to be printed
or to be sent to the students. There is no automatic correction,
since the answers may be directly written on paper.

#### Required installed software

This software was written using **Python 3.6** with the package
**PyLaTex**. It also requires an installed version of **LaTex**.
In this last, it is possible to install all the required packages.

#### How to run

This programs need two files in input:

- A JSON file containing all the information related to the students;
- A JSON file containing all the information related to the test.

These two should be passed as parameter to the file _main.py_:

    python main.py students.json test.json
    
The used interpreter should have installed all the required Python
packages. The name are only symbolic.

This software was developed using PyCharm, which can 
simplify the execution and the package installation of this software.

#### How to create _student.json_

This file is made by an array containing the students data in form
of object. These lasts have these fields: _name_, _surname_ and
_type_. The types modify the behaviour of the generation in function
of the student needs, in order to follow the directives the school
decided for each situation. The allowed types are: _more_time_, 
_optional_questions_, _allow_notes_ and, obviously, _standard_.
If not specified, the student is assumed to have a standard test.

#### How to create _text.json_

This file has a lot of parameters, these are the single value ones:

- _subject_: this should contains the school subject name;
- _subtitle_: this should contains the test argument;
- _language_: the language of the LaTex document;
- _class_: the class which the students belong to;
- _years_: the class school year;
- _date_: the test date;
- _duration_: the standard test duration;
- _more_time_duration_ (optional): the duration for the students who
need more time and it is equal to the previous if not specified.
- _extra_point_ (optional): if set and true, it generates an extra
point for answers order and for the rules respect.

##### The parameter _votes_

This section is used to generate the table to convert earned points
to a vote in tenths. It is made by three parameters:

- _min_: this specifies the minimum allowed vote and its related
points through the fields _vote_ and _up_to_ inside of it.
- _max_: this specifies the maximum allowed vote and its related
points through the fields _vote_ and _from_ inside of it.
- _int_ (optional): this flag force the program to convert the vote
in integers.

The votes inside the two limiters are computed at runtime.

##### The parameter _arguments_

This is the section that contains the real test and all its
questions. It is organized as an array of arguments, that represent
a big section, where each of them contains a set of questions.

An argument is composed by an _argument_name_ and an array of
_questions_. Each question has these parameters:

- _type_: this defines the question category.
- _text_: this contains the question in form of string or in form
of strings array if the flag _array_ is set to true. It can contain
several _%n_ that will be substituted with a random value chosen
according to the rules of the following point.
- _values_: this field, optional if the _text_ doesn't contain any
_%n_ specify the policies to follow for the value to substitute. 
There are three policies:
    - _int_: generate an integer in the given interval 
    [_min_, _max_];
    - _float_: generate a float in the given interval 
    [_min_, _max_] with the specified number of _digits_;
    - _set_: the value is picked randomly in a set.
- _optional_ (optional): declare the question as optional for the
students who need less questions.
- _points_ (optional): define the value in points of the question
and, if not specified, its value is one.
- _array_ (optional): if set and true it defines the field _text_
as an array of string the program will concatenate.