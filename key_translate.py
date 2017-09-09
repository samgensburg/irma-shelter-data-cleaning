import csv
import re
import requests
import sys

# Process arguments

def clean_name(name):
    name = name.strip()
    name.replace('  ', ' ')

    for suffix in ['special needs', 'pet', 'pets', '-', 'es', 'psn',
        '(special-needs only)', '(pet shelter)', 'livestock shelter', ':',
        'general population', 'red cross', '(special needs-only)', '(special needs only)',
        '(pets only)']:
        if name.endswith(suffix):
            return clean_name(name[:-len(suffix)])

    return name


if len(sys.argv) != 3:
    print('usage: key_translate.py red-cross-csv-file key-csv-file')
    exit()

# Read Red Cross file

csv_name = sys.argv[1]
red_cross_dict = dict()
red_cross_address_dict = dict()
reverse_red_cross_address_dict = dict()

with open(csv_name, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        shelter_key = clean_name(row['Shelter Name'].lower())
        shelter_address = row['Shelter Address'].lower()
        shelter_address.replace('.', '')
        red_cross_dict[shelter_key] = row
        red_cross_address_dict[shelter_address] = shelter_key
        reverse_red_cross_address_dict[shelter_key] = shelter_address

# Read from items csv

csv_name = sys.argv[2]

with open(csv_name, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    out_key_list = [row['key'] for row in csvreader]

with open('out.csv', 'w') as csvfile:
    fieldnames = ['county', 'shelter', 'address', 'city', 'state', 'zip']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key in out_key_list:
        item = red_cross_dict[key]
        writer.writerow({'county': item['County/Parish'],
            'shelter': item['Shelter Name'], 'address': item['Shelter Address'],
            'city': item['City'], 'state': item['State'], 'zip': item['Zip']})
