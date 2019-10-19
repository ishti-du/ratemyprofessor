import re, nltk, pprint, heapq

"""
Code taken from:
https://github.com/Shaier/Movie-Summarizer/blob/master/Movie_Summarizer.ipynb

Original Medium Blog post:
https://towardsdatascience.com/summarizing-harry-potter-with-ml-e724c024e2a2

"""

filename = 'all_cs_students_comments.txt'
with open(filename) as fObj:
    lines = fObj.readlines()

# Convert into a single line for preprocessing.
lines = '. '.join(lines)

# Pre-processing
processed_comments = re.sub(r'\[[0-9]*\]', ' ', lines)
processed_comments = re.sub(r'\s+', ' ', lines)

# Removing special characters and digits
formatted_comments = re.sub('[^a-zA-Z]', ' ', processed_comments)
formatted_comments = re.sub(r'\s+', ' ', processed_comments)

# Converting Text To Sentences
sentence_list = nltk.sent_tokenize(processed_comments)
pprint.pprint(sentence_list)

# Find Weighted Frequency of Occurrence
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_comments):
    if word not in stopwords and word not in ".":
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1
pprint.pprint(word_frequencies)

# divide the number of occurances of all the words by the frequency of the most occurring word
maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)
pprint.pprint(maximum_frequncy)

# Calculating Sentence Scores
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]
pprint.pprint(sentence_scores)

# Getting the Summary
summary_sentences = heapq.nlargest(30, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
pprint.pprint("******** SUMMARY *********")
pprint.pprint(summary)
