"""
This program first builds a dictionary of software engineering faculties with their set
of software engineering course numbers.

Then it uses this dictionary to gather SE faculty information from RMP data
The output is SE faculty data (ratings, comments etc.) from their SE related courses' RMP data.
"""

import pprint

file_se_faculty_with_course_no = "se_facutly_course_no.csv"
file_all_se_faculty_data = "se_faculty_data_all.csv"
ouput_file_se_faculty_who_teach_se = "se_faculty_teaches_se_course_data_all.csv"

with open(file_se_faculty_with_course_no) as fObj:
    all_lines = fObj.readlines()

# faculty_name - set of unique courses
se_faculty_dictionary = {}

# skip the header
for i in range(1, len(all_lines)):
    line = all_lines[i]

    # University, Department, Faculty_name, Course_no
    tokens = line.split(',')

    current_faculty = tokens[2].strip()
    course_no = tokens[3].strip()

    course_no_set = se_faculty_dictionary.get(current_faculty, set())
    course_no_set.add(course_no)

    se_faculty_dictionary[current_faculty] = course_no_set

pprint.pprint(se_faculty_dictionary)

with open(file_all_se_faculty_data) as fObj:
    all_lines = fObj.readlines()

with open(ouput_file_se_faculty_who_teach_se, 'w') as fObj:
    # ignore header
    for i in range(1, len(all_lines)):
        line = all_lines[i]
        # University,Department,Instructor,Overall Rating,Number of Ratings,Date,Rating,Overall Quality,Overall Quality Score, Level of Difficulty, Level of Difficulty Score,Course,
        # e.g.,
        # Stanford University	Computer Science	Alex Aiken	3.5	1	03/11/2013	GOOD	3.5	OVERALL QUALITY	4	LEVEL OF DIFFICULTY	CS143
        tokens = line.split(',')

        current_faculty = tokens[2].strip()
        course_no = tokens[11].strip()

        if current_faculty in se_faculty_dictionary:
            if course_no in se_faculty_dictionary.get(current_faculty):
                pprint.pprint(line)
                fObj.write(line)
