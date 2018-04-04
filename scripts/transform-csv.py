import io
import re
import json
import csv
import pprint

data = json.load(open('../output/records-processed-1998-2018.json'))
csv_file = open('../output/copom-records.csv','w')
csv_writer = csv.writer(csv_file)

def split_subtopics (text):
  return filter(None, re.split(r'\s*\d{1,2}\.\s+', text))

for record in data:
  if 'topics' in record:
    for topic_index, topic in enumerate(record['topics']):
      if 'content' in topic:
        for sub_index, subtopic in enumerate(split_subtopics(topic['content'])):
          try:
            content = subtopic
            if 'title' in topic:
              title = topic['title']
            else:
              title = ''
            if 'president' in record['participants']:
              president = record['participants']['president']
            else:
              president = ''
            year = record['year']
            month = record['month']
            csv_file = csv_writer.writerow([title, content, president, year, month])
          except Exception as err:
            print('error message: ', err)
            pass