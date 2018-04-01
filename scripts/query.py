import json
from pprint import pprint
import re

data = json.load(open('../output/1998-2018-copom-records.json'))

for content in data:
  if content['count'] == 150:
    print(content['participants'])
