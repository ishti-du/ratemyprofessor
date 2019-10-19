import json

filename = '/Users/iuh129/Desktop/Research/RateMyProfessor/json_summary_english_us_canada.json'
##filename = '/Users/iuh129/PycharmProjects/untitled/json_summary_result_cs_canada.json'

with open(filename) as fObj:
    reviews = json.load(fObj)

total_review = 0
no_comment_count = 0
for review in reviews:
    # total_review += len(review[9])
    for comment in review[9]:
        if "No Comment" not in comment:
            total_review += 1
        else:
            no_comment_count += 1

print('Total comments made by students = ' + str(total_review + no_comment_count))
print('Total valid comments =' + str(total_review))
print('Total no comment count = ' + str(no_comment_count))
