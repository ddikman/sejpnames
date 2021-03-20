''' This file takes two input files `flicknamn.csv` and `pojknamn.csv` as per the `example_input.csv` format, joins the content and spits out a single normalized file with all the names that have names that can be writen with only katana
'''

import csv
import jaconv
import re

''' normalize an integer string with or without comma to integer
'''
def normalize_int(count: str):
    if ',' in count:
        return int(count.replace(',', ''))
    
    return int(count)

''' takes a swedish name and simplifies patterns in a way that they can be translated to katakana
'''
def simplify_swedish_name(name: str):
    simplified = name.lower().replace('nn', 'n')
    return simplified

''' checks if a name contains any small characters that makes the name harder to write
'''
def is_simple_katakana(name: str):
    return re.match(u".*[ァィッェゥåäö].*", name) is None

''' return dictionary of all names with katakana
'''
def get_names(filename: str, gender: str):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            name_simplified = simplify_swedish_name(row['name'])
            count = normalize_int(row['count'])
            link = row['link']
            katakana = jaconv.hira2kata(jaconv.alphabet2kana(name_simplified))
            if is_simple_katakana(katakana):
                yield { 'name': name, 'katakana': katakana, 'link': link, 'count': count, 'gender': gender }

all_names = list(get_names('flicknamn.csv', 'girl')) + list(get_names('pojknamn.csv', 'boy'))

with open('names.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(['gender','name', 'katakana', 'count'])
    for row in all_names:
        writer.writerow([row['gender'], row['name'], row['katakana'], row['count']])