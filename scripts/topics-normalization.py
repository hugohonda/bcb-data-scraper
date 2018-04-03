import json
import os

topics = json.load(open('../data/topics-count.json'))
sorted = sorted(topics, key=lambda k: k['count'])

output_dir = '../data/twitter'
if not os.path.isdir(output_dir):
  os.mkdir(output_dir)
with open('../data/topics-count.json', 'w') as file:
  json.dump(sorted, file)