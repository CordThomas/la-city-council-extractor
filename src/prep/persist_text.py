"""
    Clean the text from the OCR to prepare for the models
    For data cleansing:  https://towardsdatascience.com/write-a-document-classifier-in-less-than-30-minutes-2d96a8a8820c
"""
import configparser
import string
from os import listdir, walk
from os.path import isdir, join, exists
import socket
from wpds-utils import system_utils as sysu
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from extract.extract_text_donlin_with_ocr import document_exists
from extract.extract_text_donlin_with_ocr import record_document

config = configparser.ConfigParser()
config.read('config/base.ini')
hostname = socket.gethostname()
config_section = sysu.get_config_section(hostname)
base_claim_file_path_root = config['Locations.{}'.format(config_section)]['claims_file_root']
base_claim_file_path_root_pattern = config['Locations.{}'.format(config_section)]['claims_file_root_pattern']
sqlite_db_file = config['Locations.{}'.format(config_section)]['sqlite_db_path']


def save_claim_file_text(db_conn, confirmation_code, file_name, processed_text, document_text='', text_extracted=1):
    """
    Save the cleaned text to the database
    :param claims_db: Open database connection
    :param confirmation_code:  Claim's confirmation code
    :param file_name:  File name on the disk with wildcards in every non-ascii character
    :param processed_text: The cleaned text ready for modeling
    :param document_text:  The original document text
    :param text_extracted: Whether or not the document text has been processed, 1 = basic clean, 2 = further cleaned
    :return:  Nothing
    """

    if len(document_text) > 0:
        sql_statement = 'UPDATE claims_documents_on_fs SET TextExtracted=?, OCRText=?, ProcessedText=? ' \
                        'WHERE ConfirmationCode=? AND DocumentName LIKE ?'

        query_field_values = (text_extracted, document_text, processed_text, confirmation_code, file_name, )
    else:
        sql_statement = 'UPDATE claims_documents_on_fs SET TextExtracted=?, ProcessedText=? ' \
                        'WHERE ConfirmationCode=? AND DocumentName LIKE ?'

        query_field_values = (text_extracted, processed_text, confirmation_code, file_name,)

    execute_sql_params(db_conn, sql_statement, query_field_values)


def get_ankura_file_name(file_name):
    """
    The file names provided by Ankura replace spaces and special characters with underscores.  Need to
    convert the file name as found on disk to the Ankura format
    From https://stackoverflow.com/questions/12985456/replace-all-non-alphanumeric-characters-in-a-string
    :param file_name:  The file name as present on disk
    :return:  The donlin-formated file name
    """

    donlin_file_name = "".join([c if c.isalnum() or c=='.' or c=='-' else '_' for c in file_name])
    return donlin_file_name[:-4] + '.pdf'


def remove_claims_terms(source):

    source = source.replace('CONFIDENTIAL — SUBJECT TO CONFIDENTIALITY ORDER AND USE RESTRICTIONS.', '')

    return source


def remove_legal_terms(words):
    """
    Remove common legal terms we'll see in a lot of documents
    :param words:  the current list of words in the bag
    :return:  A new list with the common legal terms removed
    """
    legal_terms = ['confidential', 'subject', 'confidentiality', 'claim', 'claimant']
    words = [w for w in words if not w in legal_terms]
    return words


def read_and_prepare_file_text(file_path):
    """
    Clean text input for processing following instructions found here
    https://machinelearningmastery.com/clean-text-machine-learning-python/
    :param file_path: the path to the file to be prepared
    :return: The original file text and the prepared text ready to model
    """

    text = ''
    with open(file_path, 'r') as file:
        text = file.read()

    # print(text)
    prepared_text = remove_claims_terms(text)
    prepared_text = prepared_text.lower()
    # split into words
    tokens = word_tokenize(prepared_text)
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    words = remove_legal_terms(words)
    ## 7) Reformat to have a single text.
    prepared_text = ' '.join(words)
    return text, prepared_text


def process_claims_files(db_conn, batch_date, base_claim_file_path):
    """
    Loop through all of the claims files and then categorize them based on
    their text to train the model
    :param db_conn: Open database connection
    :param batch_date:  Batch date
    :param base_claim_file_path: formatted batch date file path
    """

    submit_modes = ['']

    # In the 2022-11-22 batch, donlin introduce subfolders to organize data into 3 submission modes
    if isdir(join(base_claim_file_path, 'Uploaded')):
        submit_modes = ['Guided', 'Mailed', 'Uploaded']

    for submit_mode in submit_modes:
        if isdir(join(base_claim_file_path, submit_mode)):
            for f in listdir(join(base_claim_file_path, submit_mode)):
                if isdir(join(base_claim_file_path, submit_mode, f)):
                    path_parts = f.split('_')
                    confirmation_code = path_parts[0]

                    for root, subdirs, files in walk(join(base_claim_file_path, submit_mode, f)):
                        for file in files:
                            if '.pdf' == file[-4:]:
                                file_path = join(root, file)[:-4] + '.txt'
                                if exists(file_path):
                                    try:
                                        print('   Confirmation {} has file {}'.format(confirmation_code, file_path))
                                    except:
                                        print('   Could not print the file name - likely unicode issue')
                                    original_file_text, processed_text = read_and_prepare_file_text(file_path)
                                    if not document_exists(db_conn, confirmation_code, batch_date, file):
                                        record_document(db_conn, confirmation_code, batch_date, file)
                                    save_claim_file_text(db_conn, confirmation_code, file, processed_text,
                                                         original_file_text)


def main(sqlite_db_file, batch_dates):

    sqlite_db = create_connection(sqlite_db_file)
    # batch_dates = get_batch_dates_from_path(base_claim_file_path_root, 'submissions-')

    for batch_date in batch_dates:

        print('Cleaning txt from PDFs for: {batch}'.format(batch=batch_date))
        base_claim_file_path_date = base_claim_file_path_root_pattern.format(batch_date)
        process_claims_files(sqlite_db, batch_date, base_claim_file_path_date)

        sqlite_db.commit()

    sqlite_db.close()


if __name__ == '__main__':

    batch_dates = batch_dates_all[hostname]

    main(sqlite_db_file, batch_dates)