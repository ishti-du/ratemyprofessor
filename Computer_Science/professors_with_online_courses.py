import json
import pprint

filename = '/Users/iuh129/Desktop/Research/RateMyProfessor/json_summary_cs_us_canada.json'
##filename = '/Users/iuh129/PycharmProjects/untitled/json_summary_result_cs_canada.json'

with open(filename) as fObj:
    reviews = json.load(fObj)

# check if 'video', 'online', 'youtube', 'website' words appear in the comments
buzzwords = ['video', 'online', 'youtube', 'website', 'upload', 'film', 'coursera', 'blog', 'edx']
count = 0

output = []

for review in reviews:
    all_comments = review[9]
    possible_online_course_available = False
    comments_with_buzz = []
    matched_buzzwords = {}
    for comment in all_comments:
        for target_word in buzzwords:
            if target_word in comment.lower():
                possible_online_course_available = True
                matched_buzzwords.setdefault(target_word, 0)
                matched_buzzwords[target_word] = matched_buzzwords[target_word] + 1
                comments_with_buzz.append(comment)

    if possible_online_course_available:
        print('\n' + review[0] + '\t' + review[2])
        print(matched_buzzwords)
        print(comments_with_buzz)
        count += 1

        output.append([review[0] + '-' + review[2], matched_buzzwords, comments_with_buzz])

with open('prof_with_online_courses.json', 'w') as fObj:
    json.dump(output, fObj)

print('Total such professors: ' + str(count))
print('Done..')
