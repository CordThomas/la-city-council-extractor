import requests
import bs4
from bs4 import BeautifulSoup

cf_url_pattern = 'https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber=21-{item}'

# for cf in range (9999):
#     item_number = str(cf).zfill(4)
#     cf_url = cf_url_pattern.format(item = item_number)
#     print (cf_url)

cf_url = 'https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber=21-0349'

html_text = requests.get(cf_url, verify=False).text
soup = BeautifulSoup(html_text, 'html.parser')

main_content = soup.find('div', {'id': 'viewrecord'})
sections = main_content.children


def extract_label_text(var_name, var_text):
    if var_name is None or var_text is None:
        print('Skipping blank')
    else:
        if not (var_name.string is None or var_text.string is None):
            label_value = var_name.string.strip()
            text_value = var_text.string.strip()
            print('We have label {label} with {text}'.format(label=label_value, text=text_value))
        else:
            if var_name.string is not None and var_text.contents is not None:
                label_value = var_name.string.strip()
                text_value = ''
                # print('Name : ' + str(var_name.string))
                # print('Label: ' + str(var_text.string))
                # print(var_text.contents)
                for entry in var_text.contents:
                    # print (type(entry))
                    if isinstance(entry, bs4.element.Tag):
                        text_value = entry.contents[0].strip()
                print('We have label {label} with {text}'.format(label=label_value, text=text_value))

i = 0
for section in sections:
    if i >= 12:
        break
    print(section)
    # If we have a set of children we know we have content
    if len(section) > 1:
        has_left = section.contents[1]
        if has_left.attrs['class'][0] == 'left':
            # we have a left and right div
            left = section.contents[1]
            for element in left.contents:
                if element != '\n':
                    left_label = left.contents[1]
                    left_text = left.contents[3]
                    extract_label_text(left_label, left_text)
            right = section.contents[3]
            for element in right.contents:
                if element != '\n':
                    right_label = right.contents[1]
                    right_text = right.contents[3]
                    extract_label_text(right_label, right_text)
        else:
            # we are in a section with no left/right sections
            print('No Left')
            label = section.contents[1]
            text = section.contents[3]
            if label == 'File Activities':
                break
            extract_label_text(label, text)

    i+= 1

# print(main_content)