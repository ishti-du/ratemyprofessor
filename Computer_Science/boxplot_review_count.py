filenames = ['cs_review_count.txt', 'eng_review_count.txt', 'cs_student_sentiment.txt', 'eng_student_sentiment.txt']

for filename in filenames:
    with open(filename) as fObj:
        lines = fObj.readlines()

    output = [int(line) if '.' not in line else float(line) for line in lines]
    print(filename)
    print(output)
