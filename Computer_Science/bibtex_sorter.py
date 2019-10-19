import re

filename = '/Users/iuh129/Desktop/Research/RateMyProfessor/Conf_Paper/related.bib'
with open(filename) as fObj:
    lines = fObj.readlines()

singleString = ''.join(lines)

my_dictionary = {}

# entries = re.split(r'[\n]+@', singleString)
entries = re.split('\n\n', singleString)
for entry in entries:  # each of the bib entry
    lines = entry.split(',')  # we want just the first line
    key = (lines[0].split('{'))[1]  # e.g., @article{abc19how , we want the name 'abc19how'
    # print(key)
    my_dictionary[key] = entry  # adding the entry with the key in dictionary

# get all the keys of the dictionary in a list and sort it
keysList = list(my_dictionary.keys())
keysList.sort()

output = []
for key in keysList:  # traverse the sorted keys list, get the value and add it to the output
    value = my_dictionary.get(key)
    if value[0] != '@':  # if no @ sign, add it
        value = '@' + value
    output.append(value)

sortedLines = '\n\n'.join(output)
print(sortedLines)
