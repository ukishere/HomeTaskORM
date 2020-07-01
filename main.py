import csv
import re
from datetime import datetime
from pymongo import MongoClient

def read_data(csv_file, events):
    with open(csv_file, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

        for event in data:
            event['Цена'] = int(event['Цена'])
            print(event['Дата'])
            event['Дата'] = datetime.strptime(event['Дата']+'.2020', '%d.%m.%Y')
        events.insert_many(data)

def find_cheapest(events):
    return list(events.find({}, {'_id': 0, 'Исполнитель': 1, 'Цена': 1, 'Место': 1, 'Дата': 1}).sort('Цена', 1))

def find_by_name(name, events):
    list_of_letters = list(name)
    name = ''
    for letter in list_of_letters:
        name += '[' + letter.lower() + ',' + letter.upper() + ']{1}'
    name += '.*'

    pattern = re.compile(rf'{name}.*')
    all_events = list(events.find({}, {'_id': 0, 'Исполнитель': 1, 'Цена': 1, 'Место': 1, 'Дата': 1}).sort('Цена', 1))
    result = []

    for test_event in all_events:
        if re.match(pattern, test_event['Исполнитель']):
            result.append(test_event)

    return result

def sort_by_date(event):
    return list(events.find({}, {'_id': 0, 'Исполнитель': 1, 'Цена': 1, 'Место': 1, 'Дата': 1}).sort('Дата', 1))

if __name__ == '__main__':
    client = MongoClient()
    events_db = client['events_db']
    events = events_db['events']

    events.drop()
    read_data('artists.csv', events)

    # result = find_cheapest(events)
    # result = find_by_name('t', events)
    result = sort_by_date(events)
    for event in result:
        print(event)