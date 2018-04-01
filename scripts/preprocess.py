import os
import json
import re
import unicodedata
from pprint import pprint

data = json.load(open('../output/1998-2018-copom-records.json'))

# participants extractor < 200
all_pattern = r'(?:[Pp]articipante|[Pp]resente)s?\s?:?\s*?[Mm]embros.*\s*([\s\S]*?)\s*?[Cc]hefes?'
president_pattern = r'(.*?)[\s\W]*?[Pp]residente.*\n'
presents_pattern = r'[Pp]residente[\s\W]*([\s\S]*)'

def get_participants (text):
  all = re.search(all_pattern, text).group(1)
  president = re.search(president_pattern, all).group(1).strip()
  presents = re.search(presents_pattern, all).group(1)
  presents = re.sub('\r', '', presents)
  presents = re.sub(r'\n+', r'\n', presents)
  presents = presents.split(' \n ')
  presents = [x.replace('\n',' ').strip() for x in presents]
  participants = {
    'president': president,
    'others': presents
  }
  return participants

# participants extractor >= 200
def get_participants_200 (text):
  all = re.search(all_pattern, text).group(1)
  president = re.search(president_pattern, all).group(1).strip()
  presents = re.search(presents_pattern, all).group(1)
  presents = re.sub(r'\n([A-Z])', r'\1', presents)
  presents = presents.split('\n')
  presents = [x.strip() for x in presents]
  participants = {
    'president': president,
    'others': presents
  }
  return participants

# topics extractor 90 < x < 200
summary_pattern = r'[Ss]um.rio\s+([\s\S]*?)\s+[Dd]ata:?'
all_topics = set()

def get_topics (text, copom_id):
  text = re.sub(r'A\s*?valia..o\s+?[Pp]rospectiva\s+?[Dd]as\s+?[Tt]end.ncias\s+?d.\s+?[Ii]nfla..o', 'Avaliacao prospectiva das tendencias de inflacao', text)
  text = re.sub(r'A\s*?mbiente\s+[Ee]xterno', 'Ambiente externo', text)
  text = re.sub(r'E\s*?volu..o\s+?[Rr]ecente\s+?[Dd]a\s+?(?:[Ee]conomia|[Aa]tividade\s+[Ee]conomica)', 'Evolucao do mercado de cambio', text)
  text = re.sub(r'E\s*?volu..o\s+?[Rr]ecente\s+?[Dd]a\s+?[Ii]nfla..o', 'Evolucao recente da inflacao', text)
  text = re.sub(r'E\s*?conomia\s+[Mm]undial', 'Economia mundial', text)
  text = re.sub(r'I\s*?mplementa..o\s+?d.\s+?[Pp]ol.tica\s+?[Mm]onet.ria', 'Implementação de politica monetaria', text)
  text = re.sub(r'M\s*?e\s*?rcado\s+?[Mm]onet.rio\s+?e\s+?[Oo]pera..es\s+?[Dd]e\s+?[Mm]ercado\s+?[Aa]berto', 'Mercado monetario e operacoes de mercado aberto', text)
  text = re.sub(r'C\s*?om.rcio\s+?[Ee]xterior\s+?e\s+?(?:[Rr]eservas\s+?[Ii]nternacionais|[Ii]tens\s+?[Dd]o\s+?[Bb]alan.o\s+?de\s+?[Pp]agamentos|[Bb]alan.o\s+?[Dd]e\s+?[Pp]agamentos|[Aa]lguns\s+?[Rr]esultados\s+?[Dd]o\s+?[Bb]alan.o\s+?[Dd]e\s+?[Pp]agamentos)', 'Comercio exterior', text)
  text = re.sub(r'A\s*?tividade\s+?[Ee]con.mica', 'Atividade economica', text)
  text = re.sub(r'M\s*?ercado\s+de\s+[Tt]rabalho', 'Mercado de trabalho', text)
  text = re.sub(r'E\s*?xpectativas\s+e\s+[Ss]ondagens', 'Expectativas e sondagens', text)
  text = re.sub(r'C\s*?rédito\s+e\s+[Ii]nadimpl.ncia', 'Credito', text)
  text = re.sub(r'D\s*?iretrizes\s+d.\s+[Pp]ol.tica\s+[Mm]onet.ria', 'Diretrizes de politica monetaria', text)
  text = re.sub(r'S\s*?etor\s+[Ee]xterno', 'Setor externo', text)
  text = re.sub(r'I\s*?nfla..o', 'Inflacao', text)
  text = re.sub(r'P\s*?re.os', 'Precos', text)
  text = re.sub(r'B\s*?alan.o\s+de\s+[Pp]agamentos', 'Balanco de pagamentos', text)
  text = re.sub(r'P\s*?reçose\s+[Nn].vel\s+de\s+[Aa]tividade', 'Precos e Nivel de Atividade', text)
  summary = re.search(summary_pattern, text).group(1)
  summary = re.sub('\r', '', summary)
  summary = re.sub(r'\n+', r'\n', summary)
  summary = summary.split(' \n ')
  summary = [x.replace('\n',' ').strip() for x in summary]
  summary = list(filter(None, summary))
  l = len(summary)
  topics = []
  for idx, curr_topic in enumerate(summary):
    topic = {}
    content_pattern = None
    if idx < (l - 1):
      next_topic = summary[idx + 1]
      content_pattern = re.compile(f'{curr_topic}[\s\S]+?{curr_topic}([\s\S]+?){next_topic}')
    else:
      content_pattern = re.compile(f'{curr_topic}[\s\S]+?{curr_topic}([\s\S]+?)Atendimento: 145')
    if content_pattern:
      try:
        result = re.search(content_pattern, text).group(1)
        curr_topic = unicodedata.normalize('NFD', curr_topic).lower()
        curr_topic = curr_topic.encode('ascii', 'ignore').decode('utf-8')
        curr_topic = re.sub(r'\s+', ' ', curr_topic).capitalize()
        topic = {
          'title': curr_topic,
          'content': result,
          'copom_id': copom_id
        }
      except Exception as err:
        print('error message: ', err)
        pass
      all_topics.add(curr_topic)
      topics.append(topic)
  return topics

# topics extractor >= 200

def get_topics_200 (text, copom_id):
  summary = re.findall(r'\s+[A-Z]\)\s+?([\s\S]*?)\s+?\d+\.', text, flags=re.M)
  l = len(summary)
  topics = []
  for idx, curr_topic in enumerate(summary):
    curr_topic = curr_topic.rstrip().split('\n')
    curr_topic = '\s+'.join(curr_topic)
    topic = {}
    content_pattern = None
    if idx < (l - 1):
      next_topic = summary[idx + 1]
      next_topic = next_topic.rstrip().split('\n')
      next_topic = '\s+'.join(next_topic)
      content_pattern = re.compile(f'{curr_topic}\s+([\s\S]*?)\s+{next_topic}')
    else:
      content_pattern = re.compile(f'{curr_topic}\s+([\s\S]*)')
    if content_pattern != None:
      try:
        result = re.search(content_pattern, text).group(1)
        curr_topic = unicodedata.normalize('NFD', curr_topic).lower()
        curr_topic = curr_topic.encode('ascii', 'ignore').decode('utf-8')
        curr_topic = re.sub('\n', ' ', curr_topic)
        curr_topic = re.sub('\\\\s\+', '', curr_topic)
        curr_topic = re.sub(r'\s+', ' ', curr_topic).capitalize()
        topic = {
          'title': curr_topic,
          'content': result,
          'copom_id': copom_id
        }
        all_topics.add(curr_topic)
      except Exception as err:
        print('error message: ', err)
        pass
    topics.append(topic)
  return topics

# preprocess

initial = 1998
final = 2018
output_dir = '../output'
full_text = ''
err_participants = []
err_topics = []

for record in data:
  copom_id = record['id']
  print(copom_id)
  text = record['raw']
  full_text = full_text + text
  try:
    if record['id'] < 200:
      record['topics'] = get_topics(text, copom_id)
    else:
      record['topics'] = get_topics_200(text, copom_id)
  except Exception:
    err_topics.append(record['id'])
    pass
  try:
    if record['id'] < 200:
      record['participants'] = get_participants(text)
    else:
      record['participants'] = get_participants_200(text)
  except Exception:
    err_participants.append(record['id'])
    pass

print(err_topics)
print(err_participants)
print(sorted(all_topics))

if not os.path.isdir(output_dir):
  os.mkdir(output_dir)
with open(f'{output_dir}/{initial}-{final}-copom-records.json', 'w') as file:
  json.dump(data, file)

with open(f'{output_dir}/{initial}-{final}-full-compom-records.txt', 'w') as file:
  file.write(full_text)
