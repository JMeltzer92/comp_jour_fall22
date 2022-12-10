#libs
import os
import json
import time
import requests
import datetime
from datetime import date
import dateutil
import pandas as pd

# List of months
end = date.today()
start = datetime.date(2020,11,1)

months_in_range = [x.split(' ') for x in pd.date_range(start, end, freq = 'MS').strftime("%Y %m").tolist()]

for month in months_in_range:
    month[1] = month[1].lstrip('0')

months_in_range

# remove old files
dir = r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data\headlines'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

# request format for each month
def send_request(date):
    base_url = 'https://api.nytimes.com/svc/archive/v1/'
    url = base_url + '/' + date[0] + '/' + date[1] + '.json?api-key=' + 'eB3rdKuvQYqaNJdnQK9XzkBUCBbG8iFK'
    response = requests.get(url).json()
    time.sleep(4.5) # API Limit = 10 requests/minute - if you get booted, try increasing the sleep timer
    return response

# ensure each article fits criteria
def is_valid(article, date):
    is_in_range = date > start and date < end
    has_headline = type(article['headline']) == dict and 'main' in article['headline'].keys()
    return is_in_range and has_headline

# add each article into a dataframe
def parse_response(response):
    data = {'headline': [],  
        'date': [], 
        'doc_type': [],
        'material_type': [],
        'section': [],
        'keywords': []}
    
    articles = response['response']['docs'] 
    for article in articles:
        date = dateutil.parser.parse(article['pub_date']).date()
        if is_valid(article, date):
            data['date'].append(date)
            data['headline'].append(article['headline']['main']) 
            if 'section' in article:
                data['section'].append(article['section_name'])
            else:
                data['section'].append(None)
            data['doc_type'].append(article['document_type'])
            if 'type_of_material' in article: 
                data['material_type'].append(article['type_of_material'])
            else:
                data['material_type'].append(None)
            keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
            data['keywords'].append(keywords)
    return pd.DataFrame(data) 

# batch download
def get_data(dates):
    total = 0
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    for date in dates:
        response = send_request(date)
        df = parse_response(response)
        total += len(df)
        df.to_csv(r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data\headlines\\' + date[0] + '-' + date[1] + '.csv', index=False)
        print('Saving headlines/' + date[0] + '-' + date[1] + '.csv...')

# execute
get_data(months_in_range)

# list of all new csv files
dir = r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data\headlines'
all_filenames = os.listdir(dir)
all_filenames

# delete old NYT master files
os.remove(r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data\times.csv')
# switch to proper dir
os.chdir(dir)
# combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# export to csv
combined_csv.to_csv(r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data\times.csv', index=False, encoding='utf-8-sig')