"""
This class will print the meta-data table with the following information:

university_name, #instructors, avg. rating score/instructor, avg. #ratings/instructor, Max. Rating, Max. Rating Duration, Avg. Rating Duration

Each entry in the JSON Fromat:
[0] : University Name
[1] : Subject
[2] : Instructor Name
[3] : Overall Score
[4] : # Ratings ( who gave them more than 3.5 score)
[5] : Latest Rating Date
[6] : First Rating Date
[7] : List of courses
[8] : List of Tags
[9] : List of Student comments

"""

import json, pprint, statistics

# filename = "json_summary_english_us_canada.json"
filename = "json_summary_cs_us_canada.json"

with open(filename) as fObj:
    reviews = json.load(fObj)

university_set = set()
university = ''
instructor_count = 0
score_count = 0
ratings_count = 0
max_ratings_count = 0
max_ratings_duration_in_years = 0
ratings_duration_count = 0
rating_durations = []


def reset_variables():
    global instructor_count, score_count, ratings_count, max_ratings_count, max_ratings_duration_in_years, ratings_duration_count

    instructor_count = 0
    score_count = 0
    ratings_count = 0
    max_ratings_count = 0
    max_ratings_duration_in_years = 0
    ratings_duration_count = 0
    rating_durations.clear()


def prepare_and_print_output():
    """
    Output:
    university_name,  # instructors, avg. rating score/instructor, avg. #ratings/instructor, Avg. Rating Duration, Max. Rating, Max. Rating Duration
    """

    output = list()
    output.append(university)
    output.append(subject)
    output.append(str(instructor_count))
    output.append(str(round(score_count / instructor_count, 1)))
    output.append(str(int(round(ratings_count / instructor_count, 0))))
    output.append(str(int(round(ratings_duration_count / instructor_count, 0))))
    output.append(str(max_ratings_count))
    output.append(str(max_ratings_duration_in_years))

    result = '\t'.join(output)
    print(result)
    print('Median Rating Duration = ')
    print(statistics.median(rating_durations))


def print_header():
    if print_header:
        header = list()
        header.append('University Name')
        header.append('Subject')
        header.append('#Instructors')
        header.append('Avg. Ratings Score')
        header.append('Avg. Ratings Count')
        header.append('Avg. Ratings Duration (years)')
        header.append('Max. Ratings Count')
        header.append('Max. Ratings Duration (years)')

        heading = '\t'.join(header)

    print(heading)


"""
Each entry in the JSON Fromat:
[0] : University Name
[1] : Subject
[2] : Instructor Name
[3] : Overall Score
[4] : # Ratings ( who gave them more than 3.5 score)
[5] : Latest Rating Date
[6] : First Rating Date
[7] : List of courses
[8] : List of Tags
[9] : List of Student comments
"""

print_header()

for review in reviews:
    current_university = review[0]
    if university == '':
        university = current_university

    subject = review[1]
    # new university, initialize variables
    if current_university not in university_set:
        if len(university_set) > 0:
            prepare_and_print_output()

        # reset variables before new calculation
        reset_variables()
        university = current_university
        university_set.add(university)

    instructor_count += 1
    score_count += float(review[3])
    individual_rating_count = int(review[4])
    ratings_count += individual_rating_count
    individual_rating_duration = int((review[5].split('/'))[2]) - int((review[6].split('/'))[2])
    ratings_duration_count += individual_rating_duration
    rating_durations.append(individual_rating_duration)

    if max_ratings_count == individual_rating_count:
        if max_ratings_duration_in_years < individual_rating_duration:
            max_ratings_duration_in_years = individual_rating_duration
    elif max_ratings_count < individual_rating_count:
        max_ratings_count = individual_rating_count
        max_ratings_duration_in_years = individual_rating_duration

# for the last university
prepare_and_print_output()
