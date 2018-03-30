import os
import json
import re
from pprint import pprint
from unicodedata import normalize

data = json.load(open('../output/1998-2018-copom-records.json'))
all_pattern = r'(?:[Pp]articipante|[Pp]resente)s?:?\s*?[Mm]embros.*\s*([\s\S]*?)\s*?[Cc]hefes?\s[Dd]e\s[Dd]epartamento:?'
president_pattern = r'(.*?)[\s\W]*?[Pp]residente.*\n'
presents_pattern = r'[Pp]residente[\s\W]*([\s\S]*)'

not_found = [] # [88, 92, 94]
count = 0
full_text = ''

for content in data:
  if content['count'] == 96:
    break
  count += 1
  text = content['content']['raw']
  full_text = full_text + text
  try:
    all = re.search(all_pattern, text).group(1)
    president = re.search(president_pattern, all).group(1)
    presents = re.search(presents_pattern, all).group(1)
    presents = re.sub(r'\r', ' ', presents)
    presents = re.sub(r'\s{2,}', '@', presents)
    participants = {
      'president': president,
      'others': presents.split('@')
    }
    content['participants'] = participants
  except Exception:
    not_found.append(content['count'])

print(not_found)

initial = 1998
final = 2018
output_dir = '../output'

if not os.path.isdir(output_dir):
  os.mkdir(output_dir)
with open(f'{output_dir}/{initial}-{final}-copom-records.json', 'w') as file:
  json.dump(data, file)

with open(f'full-text.txt', 'w') as file:
  file.write(full_text)
  