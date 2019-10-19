"""
Collect all the comments for the highest rated professors for each university.
We already calculated the number of ratings for the highest rated professors for each university
when we created the 'meta-data'.

"""

import json, pprint

filename = "json_summary_english_us_canada.json"
output_json_file = "json_all_comments_for_top_rated_professors_english.json"

university_highest_review_count_dictionary = {"Massachusetts Institute of Technology": 14,
                                              "Stanford University": 88,
                                              "Carnegie Mellon University": 65,
                                              "University of California Berkeley": 101,
                                              "Harvard University": 53,
                                              "University of California Los Angeles": 30,
                                              "University of Washington": 188,
                                              "Georgia Institute of Technology": 71,
                                              "University of Texas at Austin": 265,
                                              "University of Southern California": 108,
                                              "University of California San Diego": 179,
                                              "University of Waterloo": 233,
                                              "University of British Columbia": 179,
                                              "University of Toronto": 15,
                                              "University of Alberta": 81,
                                              "McGill University": 67,
                                              "Carleton University": 98,
                                              "University of Ottawa": 56,
                                              "Simon Fraser University": 139
                                              }

english_highest_review_count_dictionary = {"Stanford University": 13,
                                           "Columbia University": 24,
                                           "University of California Berkeley": 49,
                                           "Harvard University": 37,
                                           "University of California Los Angeles (UCLA)": 27,
                                           "Yale University": 13,
                                           "New York University": 107,
                                           "York University (all campuses)": 145,
                                           "University of Michigan": 155,
                                           "Universite de Montreal": 14,
                                           "University of Calgary": 142,
                                           "University of British Columbia": 157,
                                           "University of Toronto": 23,
                                           "University of Alberta": 171,
                                           "McGill University": 93,
                                           "Concordia University": 77,
                                           "University of Ottawa": 130,
                                           "Western University": 77,
                                           "Princeton University": 14
                                           }

dictionary = english_highest_review_count_dictionary

with open(filename) as fObj:
    reviews = json.load(fObj)
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
all_comments_for_top_rated_profs = []
comments_count = 0

for review in reviews:
    temp = []
    if int(review[4]) == dictionary.get(review[0]):
        temp.append(review[0])  # University name
        temp.append(review[2])  # Instructor Name
        temp.append(review[4])  # Review Count
        temp.append(review[9])  # list of comments
        comments_count += len(review[9])

        all_comments_for_top_rated_profs.append(temp)
    else:
        temp.clear()

print('Total number of comments = ' + str(comments_count))
with open(output_json_file, 'w') as fObj:
    json.dump(all_comments_for_top_rated_profs, fObj)
