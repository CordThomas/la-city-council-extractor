# from https://stackabuse.com/text-summarization-with-nltk-in-python/
import nltk
import os
import re
from utils.db import *
from pathlib import Path
from os.path import exists, isfile, isdir, join
from pprint import pprint


script_path = os.path.dirname(__file__)
docs_base = join(Path(script_path).parent.parent, 'documents/')
db_file = join(Path(script_path).parent.parent, 'data/city-council.db')
years = ['2020','2021','2022']


def clean_text(input_text):
    # Removing Square Brackets and Extra Spaces
    input_text = re.sub(r'\[[0-9]*\]', ' ', input_text)
    input_text = re.sub(r'\s+', ' ', input_text)

    # Removing special characters and digits
    formatted_input_text = re.sub('[^a-zA-Z]', ' ', input_text)
    formatted_input_text = re.sub(r'\s+', ' ', formatted_input_text)

    return formatted_input_text, input_text


def process_cleaned_motion(formatted_motion_text,  motion_text):

    sentence_list = nltk.sent_tokenize(motion_text)
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_motion_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    pprint(sentence_scores)


def main(db_file, docs_base, years):

    db_conn = create_connection(db_file)
    motion_documents = get_council_motion_documents(db_conn)

    for motion_document in motion_documents:
        motion_document_path = join(docs_base, motion_document).strip()
        print(motion_document_path)
        if exists(motion_document_path):
            with open(motion_document_path, 'r') as final_extract:
                motion_text = final_extract.read()
                formatted_motion_text, motion_text = clean_text(motion_text)
                process_cleaned_motion(formatted_motion_text, motion_text)
                # print(formatted_motion_text)
        else:
            print('Cannot find {}'.format(motion_document))

        break

    db_conn.close()


if __name__ == "__main__":

    main(db_file, docs_base, years)