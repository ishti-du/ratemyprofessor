from textblob import TextBlob

tags = ['RESPECTED', 'AMAZING LECTURES', 'INSPIRATIONAL', 'CARING', 'GIVES GOOD FEEDBACK',
        'LOTS OF HOMEWORK', 'HILARIOUS', 'ACCESSIBLE OUTSIDE CLASS', 'CLEAR GRADING CRITERIA',
        "SKIP CLASS? YOU WON'T PASS.", 'TOUGH GRADER', 'PARTICIPATION MATTERS', 'LECTURE HEAVY',
        'EXTRA CREDIT', 'GROUP PROJECTS', 'GET READY TO READ', 'TEST HEAVY', 'BEWARE OF POP QUIZZES',
        'GRADED BY FEW THINGS', 'SO MANY PAPERS', 'AWFUL']

for tag in tags:
    blob = TextBlob(tag)
    print(tag + ' = Polarity = ' + str(round(blob.polarity)))
    # print(tag + ' = Subjectivity = ' + str(round(blob.subjectivity)))
