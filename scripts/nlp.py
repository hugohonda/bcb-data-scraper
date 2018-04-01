from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.stem.rslp import RSLPStemmer
import re
import unicodedata
import json
from pprint import pprint

data = json.load(open('../output/1998-2018-copom-records.json'))

# tokenizer
sws = stopwords.words('portuguese')
stemmer = RSLPStemmer()
spacer_re = re.compile(r'\t+|\s+|\s+\s|["\'\n\.:]+')
par_re = r'([\{(\(\[\|\]\))\}\!\"\'\#\*\+\/\:\;\<\=\>\?\@\^\_\`])'
punkt_re = r'(.)[\,]\s'

def norm_text (text):
  text = re.sub(r'TAG_CONTEUDO_FIM|/conteudo', '', text)
  text = unicodedata.normalize('NFD', text)
  text = text.encode('ascii', 'ignore').decode('utf-8')
  text = re.sub(punkt_re, r'\1 ', text)
  text = re.sub(par_re, '', text)
  text = re.sub(r'\s+', ' ', text)
  text = re.split(r'\s+\d{1,2}\.\s+', text)
  return text

def tokenize (text):
  tokens = re.split(spacer_re, text)
  tokens = [stemmer.stem(w) for w in tokens if len(w) >= 2 and w.lower() not in sws]
  return tokens

for content in data:
  if content['id'] == 50:
    for topic in content['topics']:
      print(topic['title'])
      subtopics = norm_text(topic['content'])
      for subtopic in subtopics:
        print(tokenize(subtopic))
      break