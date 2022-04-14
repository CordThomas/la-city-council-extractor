from rake_nltk import Rake
import spacy
import yake
import pytextrank
from collections import Counter
from string import punctuation

path = '../../documents/2021/21-1066/21-1066_misc_9-28-21.txt'

paths = ['../../documents/2021/21-1066/21-1066_misc_9-28-21.txt',
         '../../documents/2021/21-1463/21-1463_CIS_01132022103306_01-13-2022.txt',
         '../../documents/2021/21-1463/21-1463_CIS_01192022101252_01-19-2022.txt'
]

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

    for path in paths:
        print('Starting {}'.format(path))
        text = retrieve_text(path)
        rakeit(text)
        spacyit(text)
        yakeit(text)
        textrankit(text)
