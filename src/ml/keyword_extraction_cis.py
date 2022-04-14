from rake_nltk import Rake
import spacy
import yake
import pytextrank
from collections import Counter
from string import punctuation
from os import walk
from os.path import exists, isfile, isdir, join

base_path = '../../documents/'
years = ['2021']


def retrieve_text(path):

    with open (path, 'r') as extract:
        lines = extract.read()
        return lines


def rakeit(text):

    print('****** RAKE ')
    r = Rake()
    r.extract_keywords_from_text(text)
    keywordList = []
    rankedList = r.get_ranked_phrases_with_scores()
    for keyword in rankedList:
        keyword_updated = keyword[1].split()
        keyword_updated_string = " ".join(keyword_updated[:2])
        keywordList.append(keyword_updated_string)
        if len(keywordList) > 9:
            break
    print(keywordList)


def spacyit(text):

    nlp = spacy.load("en_core_web_lg")
    print('****** SPACY ')

    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    doc = nlp(text.lower())
    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)

    output = set(result)
    most_common_list = Counter(output).most_common(10)
    for item in most_common_list:
        print(item[0])


def yakeit(text):

    print('****** YAKE ')
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
    for kw in keywords:
        print(kw)

def textrankit(text):

    print('****** RANK ')
    nlp = spacy.load('en_core_web_lg')

    # tr = pytextrank.TextRank()
    # nlp.add_pipe(tr.PipelineComponent, name='textrank', last=True)

    # add pytextrank to the pipe
    nlp.add_pipe("textrank")
    doc = nlp(text)
    for phrase in doc._.phrases:
        print(phrase.text)
        print(phrase.rank)
        print(phrase.count)
        print(phrase.chunks)
    # examine the top-ranked phrases in the document
    # for p in doc._.phrases:
    #     print('{:.4f} {:5d}  {}'.format(p.rank, p.count, p.text))
    #     print(p.chunks)


if __name__ == "__main__":

    cis_count = 0
    summary_count = 0
    for year in years:
        year_path = base_path + year
        for root, subdirs, files in walk(year_path):
            for file in files:
                if '_cis_' in file.lower():
                    cis_count += 1
                    file_path = join(root, file)
                    print('Starting {}'.format(file_path))
                    text = retrieve_text(file_path)
                    if 'Summary:' not in text:
                        print('no summary in {}'.format(file_path))
                    else:
                        summary_count += 1
                    # rakeit(text)
                    # spacyit(text)
                    # yakeit(text)
                    # textrankit(text)

    print('Found {} summaries in {} CIS'.format(summary_count, cis_count))