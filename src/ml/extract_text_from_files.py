import pytesseract
from os import remove
from os import walk
from os.path import exists, isfile, isdir, join
from pdf2image import pdfinfo_from_path, convert_from_path

base_path = '../documents/'
years = ['2024', '2025']

def extract(base_path, years):

    for year in years:
        files_processed = 0
        year_path = base_path + year
        for root, subdirs, files in walk(year_path):
            if not ('13-0516' in root or '13-0318' in root or '13-1122' in root or '13-0343' in root):
                for file in files:
                    file_path = join(root, file)
                    if exists(file_path[:-4] + '.txt'):
                        print('   skipping, already processed')
                    else:
                        try:
                            info=pdfinfo_from_path(file_path)
                            maxPages = info["Pages"]
                            print('{}: {}'.format(str(maxPages), file_path))
                            pages = convert_from_path(file_path, first_page=0, last_page = min(9,maxPages))
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
                                    files_processed += 1

                          except Exception as e:
                              print(e)


if __name__ == "__main__":

   extract(base_path, years)
