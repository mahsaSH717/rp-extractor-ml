import re
import nltk
import pandas as pd
from bs4 import BeautifulSoup as bs
from nltk import word_tokenize


def pre_process(text):
    return re.sub(r'(\s([?,.!"]))|(?<=\[|\()(.*?)(?=\)|\])|(\s-\s)', lambda x: x.group().strip(), text)


def append_annotations(file_path):
    annotated_data_set = pd.read_excel(file_path)
    data = ""
    for annotated_sent in annotated_data_set['annotated_sentence']:
        data += annotated_sent
    return data


def remove_punctuation(with_punctuation):
    punctuations = '''!()[]{};:'"\,<>./?@#$%^&*_~'''
    without_punctuation = ""
    try:
        for char in with_punctuation:
            if char not in punctuations:
                without_punctuation = without_punctuation + char
    finally:

        return without_punctuation


def get_labels(doc):
    return [label for (token, postag, label) in doc]


def extract_features(doc):
    return [word2features(doc, i) for i in range(len(doc))]


def word2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]

    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'len=%s' % len(word)
    ]

    # Features for words that are not at the beginning of a document
    if i > 0:
        word1 = doc[i - 1][0]
        postag1 = doc[i - 1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:word.isdigit=%s' % word1.isdigit(),
            '-1:postag=' + postag1,
            '-1:len=%s' % len(word1)
        ])
    else:
        # Indicate that it is the 'beginning of a document'
        features.append('BOS')

    if i > 1:
        word2 = doc[i - 2][0]
        postag2 = doc[i - 2][1]
        features.extend([
            '-2:word.lower=' + word2.lower(),
            '-2:word.istitle=%s' % word2.istitle(),
            '-2:word.isupper=%s' % word2.isupper(),
            '-2:word.isdigit=%s' % word2.isdigit(),
            '-2:postag=' + postag2,
        ])

    # Features for words that are not at the end of a document
    if i < len(doc) - 1:
        pword1 = doc[i + 1][0]
        postag1 = doc[i + 1][1]
        features.extend([
            '+1:word.lower=' + pword1.lower(),
            '+1:word.istitle=%s' % pword1.istitle(),
            '+1:word.isupper=%s' % pword1.isupper(),
            '+1:word.isdigit=%s' % pword1.isdigit(),
            '+1:postag=' + postag1,
            '+1:len=%s' % len(pword1)
        ])
    else:
        # Indicate that it is the 'end of a document'
        features.append('EOS')

    if i < len(doc) - 2:
        pword2 = doc[i + 2][0]
        ppostag2 = doc[i + 2][1]
        features.extend([
            '+2:word.lower=' + pword2.lower(),
            '+2:word.istitle=%s' % pword2.istitle(),
            '+2:word.isupper=%s' % pword2.isupper(),
            '+2:word.isdigit=%s' % pword2.isdigit(),
            '+2:postag=' + ppostag2
        ])

    return features


def generate_final_data(labeled_docs):
    data = []
    for i, doc in enumerate(labeled_docs):
        tokens = [t for t, label in doc]
        tagged = nltk.pos_tag(tokens)
        data.append([(w, pos, label) for (w, label), (word, pos) in zip(doc, tagged)])
    return data


def generate_labeled_docs(soup):
    docs = []
    for d in soup.find_all("document"):
        tags = []
        for wrd in d.contents:
            none_type = type(None)

            if isinstance(wrd.name, none_type):
                without_punctuation = remove_punctuation(wrd)
                temp = word_tokenize(without_punctuation)
                for token in temp:
                    tags.append((token, 'o'))
            else:
                without_punctuation = remove_punctuation(wrd)
                temp = word_tokenize(without_punctuation)
                for token in temp:
                    tags.append((token, wrd.name))

        docs.append(tags)
    return docs


def generate_labeled_tagged_data(labeled_train_data):
    all_text = append_annotations(labeled_train_data)
    soup = bs(all_text, "html5lib")
    labeled_docs = generate_labeled_docs(soup)
    labeled_tagged_data = generate_final_data(labeled_docs)
    return labeled_tagged_data
