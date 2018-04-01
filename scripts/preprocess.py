import os
import json
import re
from pprint import pprint
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.stem.rslp import RSLPStemmer
import unicodedata

data = json.load(open('../output/1998-2018-copom-records.json'))

# tokenizer
sws = stopwords.words('portuguese')
stemmer = RSLPStemmer()
spacer_re = re.compile(r'\t+|\s+|\s+\s|["\'\n\.,:]+')
par_re = r'(\(|\[|\]|\))'

def tokenize (text):
    text = re.sub(r'TAG_CONTEUDO_FIM|/conteudo', '', text)
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(par_re, r' \1 ', text)
    tokens = re.split(spacer_re, text)
    tokens = [stemmer.stem(w) for w in tokens if len(w) >= 2 and w.lower() not in sws]
    return tokens

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

# topics extractor < 200
summary_pattern = r'[Ss]um.rio\s+([\s\S]*?)\s+[Dd]ata:?'
all_topics = set()

def get_topics (text):
  text = re.sub(r'A\s*?valiação\s+?prospectiva\s+?das\s+?tendências\s+?d.\s+?inflação', 'Avaliação prospectiva das tendências de inflação', text, flags=re.I)
  text = re.sub(r'A\s*?mbiente\s+externo', 'Ambiente externo', text, flags=re.I)
  text = re.sub(r'E\s*?volução\s+?recente\s+?da\s+?(?:economia|atividade\s+economica)', 'Evolucao do mercado de cambio', text, flags=re.I)
  text = re.sub(r'E\s*?volução\s+?recente\s+?da\s+?inflação', 'Evolução recente da inflação', text, flags=re.I)
  text = re.sub(r'E\s*?conomia\s+mundial', 'Economia mundial', text, flags=re.I)
  text = re.sub(r'I\s*?mplementação\s+?d.\s+?política\s+?monetária', 'Implementação de política monetária', text, flags=re.I)
  text = re.sub(r'M\s*?e\s*?rcado\s+?monetário\s+?e\s+?operações\s+?de\s+?mercado\s+?aberto', 'Mercado monetário e operações de mercado aberto', text, flags=re.I)
  text = re.sub(r'C\s*?omércio\s+?exterior\s+?e\s+?reservas\s+?internacionais', 'Comércio exterior', text, flags=re.I)
  text = re.sub(r'C\s*?omércio\s+?exterior\s+?e\s+?itens\s+?do\s+?balanço\s+?de\s+?pagamentos', 'Comércio exterior', text, flags=re.I)
  text = re.sub(r'C\s*?omércio\s+?exterior\s+?e\s+?balanço\s+?de\s+?pagamentos', 'Comércio exterior', text, flags=re.I)
  text = re.sub(r'C\s*?omércio\s+?exterior\s+?e\s+?alguns\s+?resultados\s+?do\s+?balanço\s+?de\s+?pagamentos', 'Comércio exterior', text, flags=re.I)
  text = re.sub(r'A\s*?tividade\s+?econômica', 'Atividade econômica', text, flags=re.I)
  text = re.sub(r'M\s*?ercado\s+de\s+trabalho', 'Mercado de trabalho', text, flags=re.I)
  text = re.sub(r'E\s*?xpectativas\s+e\s+sondagens', 'Expectativas e sondagens', text, flags=re.I)
  text = re.sub(r'C\s*?rédito\s+e\s+inadimplência', 'Crédito', text, flags=re.I)
  text = re.sub(r'D\s*?iretrizes\s+d.\s+Política\s+Monetária', 'Diretrizes de política monetária', text, flags=re.I)
  text = re.sub(r'S\s*?etor\s+externo', 'Setor externo', text, flags=re.I)
  text = re.sub(r'I\s*?nflação', 'Inflação', text)
  text = re.sub(r'B\s*?alanço\s+de\s+Pagamentos', 'Balanço de pagamentos', text)
  text = re.sub(r'P\s*?reçose\s+Nível\s+de\s+Atividade', 'Preços e Nível de Atividade', text)
  summary = re.search(summary_pattern, text).group(1)
  summary = re.sub('\r', '', summary)
  summary = re.sub(r'\n+', r'\n', summary)
  summary = summary.split(' \n ')
  summary = [x.replace('\n',' ').strip() for x in summary]
  l = len(summary)
  topics = []
  for idx, curr_topic in enumerate(summary):
    topic = {}
    content_pattern = None
    if idx < (l - 1):
      next_topic = summary[idx + 1]
      content_pattern = re.compile(f'{curr_topic}[\s\S]*?{curr_topic}\s+([\s\S]*?)\s+{next_topic}')
    else:
      content_pattern = re.compile(f'{curr_topic}[\s\S]*?{curr_topic}\s+([\s\S]*?)\s+Atendimento: 145')
    if content_pattern != None:
      try:
        result = re.search(content_pattern, text).group(1)
        curr_topic = unicodedata.normalize('NFD', curr_topic).lower()
        curr_topic = curr_topic.encode('ascii', 'ignore').decode('utf-8')
        curr_topic = re.sub(r'\s+', ' ', curr_topic).capitalize()
        topic = {
          'title': curr_topic,
          'content': tokenize(result)
        }
        all_topics.add(curr_topic)
      except Exception as err:
        print('error message: ', err)
        pass
    topics.append(topic)
  return topics

# topics extractor >= 200

def get_topics_200 (text):
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
          'content': tokenize(result)
        }
        all_topics.add(curr_topic)
      except Exception as err:
        print('error message: ', err)
        pass
    topics.append(topic)
  return topics

# execution

initial = 1998
final = 2018
output_dir = '../output'
full_text = ''
err_participants = []
err_topics = []

for content in data:
  print(content['count'])
  text = content['content']['raw']
  full_text = full_text + text
  try:
    if content['count'] < 200:
      content['topics'] = get_topics(text)
    else:
      content['topics'] = get_topics_200(text)
  except Exception:
    err_topics.append(content['count'])
    pass
  try:
    if content['count'] < 200:
      content['participants'] = get_participants(text)
    else:
      content['participants'] = get_participants_200(text)
  except Exception:
    err_participants.append(content['count'])
    pass

print(err_topics)
print(err_participants)
print(sorted(all_topics))

if not os.path.isdir(output_dir):
  os.mkdir(output_dir)
with open(f'{output_dir}/{initial}-{final}-copom-records.json', 'w') as file:
  json.dump(data, file)

# with open(f'full-text.txt', 'w') as file:
#   file.write(full_text)
