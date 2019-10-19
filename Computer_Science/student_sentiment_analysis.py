from textblob import TextBlob
import json
import nltk

# Sentiment Analysis Source: https://www.analyticsvidhya.com/blog/2018/02/natural-language-processing-for-beginners-using-textblob/


filename = 'json_summary_cs_us_canada.json'

all_students_comments = []

with open(filename) as fObj:
    reviews_all_instructors = json.load(fObj)

for review_for_an_instructor in reviews_all_instructors:
    all_comments_for_an_instructor = review_for_an_instructor[9]
    polarity = []
    subjectivity = []
    unique_comments_set = set()
    for comment in all_comments_for_an_instructor:
        lower_case_comment = comment.lower()
        # ignore no comments and duplicate comments
        if 'no comment' not in lower_case_comment and lower_case_comment not in unique_comments_set:
            unique_comments_set.add(lower_case_comment)
            blob = TextBlob(lower_case_comment)
            sentiment = blob.sentiment
            polarity.append(sentiment[0])
            subjectivity.append(sentiment[1])

    # print average polarity and subjectivity for the professor
    average_polarity = round(sum(polarity) / len(polarity), 2)
    average_subjectivity = round(sum(subjectivity) / len(subjectivity), 2)

    institution = review_for_an_instructor[0]
    instructor = review_for_an_instructor[2]
    average_rating = review_for_an_instructor[3]
    unique_comments_count = len(unique_comments_set)

    all_students_comments.append(list(unique_comments_set))

    print('\t'.join([institution, instructor, str(average_rating),
                     str(unique_comments_count), str(average_polarity), str(average_subjectivity)]))

for comment in all_students_comments:
    print(comment)
