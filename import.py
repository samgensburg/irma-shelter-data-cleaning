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
            return clean_red_cross_name(name[:-len(suffix)])

    return name


if len(sys.argv) != 2:
    print('usage: import.py red-cross-csv-file')
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

# Read from API

response = requests.get('https://irma-api.herokuapp.com/api/v1/shelters')
api_body = response.json()['shelters']

api_dict = dict()
api_address_dict = dict()
api_list = []

for shelter in api_body:
    shelter_key = clean_name(shelter['shelter'].lower())
    api_dict[shelter_key] = shelter
    address = shelter['address']
    if ',' in address:
        address = address[:address.index(',')]
    address.replace('.', '')
    api_address_dict[address.lower()] = shelter_key
    api_list.append(shelter_key)

mismatch_list = []

for red_cross_shelter_name in red_cross_dict:
    if (not red_cross_shelter_name in api_dict and
        not reverse_red_cross_address_dict[red_cross_shelter_name] in api_address_dict):
        mismatch_list.append(red_cross_shelter_name)

mismatch_list.sort()
api_list.sort()

mismatch_index = 0
api_index = 0

while api_index < len(api_list) and mismatch_index < len(mismatch_list):
    print('mismatched item: ' + mismatch_list[mismatch_index])
    print('api item: ' + api_list[api_index])

    key = input() or key

    if key == 'm':
        mismatch_index += 1
    elif key == 'a':
        api_index += 1
    elif key == 'match':
        del mismatch_list[mismatch_index]

print ('---------------------------')
for item in mismatch_list:
    print(item)
