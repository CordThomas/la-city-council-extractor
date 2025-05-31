import pytesseract
from os import remove
from os import walk
from os.path import exists, join
from pathlib import Path
from pdf2image import pdfinfo_from_path, convert_from_path

base_path = '../documents/'
years = ['2021', '2022', '2023']


def is_locked(file_path):
    """
    To support multiple machines working on the same file list,
    we set a lock file while processing and check for it on
    each file we are going to process.  There still could be some
    collision but the time to create and remove a file is much less
    than the time to OCR a file
    :param file_path:  The full path to the file
    :return:  True if locked, e.g., the lck file exists
    """
    if exists(file_path[:-4] + '.lck'):
        return True

    return False


def is_processed(file_path):
    """
    To support reprocessing files, check whether the file has been processed
    :param file_path:  The full path to the file
    :return:  True if locked, e.g., the lck file exists
    """
    if exists(file_path[:-4] + '.processed'):
        return True

    return False


def set_lock(file_path):
    """
    Set a lock file to block other processes from trying to process
    the same file. While not a perfect mechanism, works well and
    it's not generally a disaster if multiple processes try to work
    on the file
    :param file_path: The path to the file being processed
    :return: nothing
    """
    lock_file = file_path[:-4] + '.lck'
    Path(lock_file).touch()


def set_processed(file_path):
    """
    Record that the file has been processed - need this to support partial file reprocessing
    :param file_path: The path to the file being processed
    :return: nothing
    """
    lock_file = file_path[:-4] + '.processed'
    Path(lock_file).touch()


def remove_lock(file_path):
    """
    Remove the lock file
    """
    lock_file = file_path[:-4] + '.lck'
    if exists(lock_file):
        remove(lock_file)


def extract(base_path, years):
    """
    Extract text from the files in the years list
    :param base_path: The base path where the documents are stored
    :param years: List of years to process
    :return: None
    """

    for year in years:
        year_path = base_path + year
        for root, subdirs, files in walk(year_path):
            if not ('13-0516' in root or '13-0318' in root or '13-1122' in root or '13-0343' in root):
                for file in files:
                    file_path = join(root, file)
                    # if exists(file_path[:-4] + '.txt'):
                    #     print('   skipping, already processed')
                    # else:
                    if file_path[-4:].lower() == '.pdf' and not is_locked(file_path):
                        try:
                            set_lock(file_path)
                            try:
                                info = pdfinfo_from_path(file_path)
                                maxPages = info["Pages"]
                                if maxPages > 9:
                                    if not is_processed(file_path):
                                        set_processed(file_path)
                                        print('{}: {}'.format(str(maxPages), file_path))
                                        pages = convert_from_path(file_path, first_page=0, last_page=maxPages)
                                        page_idx = 0
                                        final_file_path = file_path[:-4] + '.txt'
                                        with open (final_file_path, 'w') as final_extract:
                                            for page in pages:
                                                image_file = file_path[:-4] + '-' + str(page_idx) + '.tiff'
                                                page.save(image_file)
                                                string_contents = pytesseract.image_to_string(image_file)
                                                final_extract.write(string_contents)

                                                remove(image_file)
                                                page_idx += 1

                                else:
                                    print('   skipping, smaller than 9 pages')

                            except Exception as e:
                                print(e)

                            remove_lock(file_path)

                        except Exception as e:
                            print(e)
                    else:
                        print('        LOCKED - SKIPPING')


if __name__ == "__main__":

   extract(base_path, years)
