import PIL
import pytesseract
import pdf2image
from os import walk
from os.path import isfile, isdir, join
from pdf2image import pdfinfo_from_path, convert_from_path

base_path = '/mnt/usb1/srv/projects/city-council-files/documents/'
years = ['2013']


def extract(base_path, years):

  for year in years:
    files_processed = 0
    year_path = base_path + year
    for root, subdirs, files in walk(year_path):
      for file in files:
        file_path = join(root, file)
        print(file_path)
        info=pdfinfo_from_path(file_path)
        maxPages = info["Pages"]
        pages = convert_from_path(file_path, first_page=0, last_page = min(9,maxPages))
        page_idx = 0
        for page in pages:
          image_file = file_path[:-4] + '-' + str(page_idx) + '.tiff'
          page_idx += 1
          page.save(image_file)
          txt_file = file_path[:-4] + '-' + str(page_idx) + '.txt'
          string_contents = pytesseract.image_to_string(image_file)
          with open (txt_file, 'w') as f:
            f.write(string_contents)
        files_processed += 1

        if files_processed >= 50:
          exit()

if __name__ == "__main__":

   extract(base_path, years)
