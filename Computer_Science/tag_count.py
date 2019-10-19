import pprint

filename = '/Users/iuh129/Desktop/Research/RateMyProfessor/tags.txt'

with open(filename) as fObj:
    lines = fObj.readlines()

tag_dictionary = {}

for line in lines:
    if '(' not in line:
        continue

    tags = line.split(',')

    for tag in tags:
        tag.strip()
        # tag example: AMAZING LECTURES(16)
        tokenize = tag.split('(')
        tag_name = tokenize[0].strip()

        tag_count = tokenize[1].replace(')', '').strip()

        tag_dictionary.setdefault(tag_name, 0)
        tag_dictionary[tag_name] += 1

for k, v in tag_dictionary.items():
    print(k + '\t' + str(v))
