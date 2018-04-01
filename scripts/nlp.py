from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.stem.rslp import RSLPStemmer
import re
import unicodedata
import json
from pprint import pprint

data = json.load(open('../output/1998-2018-copom-records.json'))

# sentence split
def sentence_split (text):
  return re.split(r'\s+\d{1,2}\.\s+', text)

# tokenizer
sws = stopwords.words('portuguese')
stemmer = RSLPStemmer()
spacer_re = re.compile(r'\t+|\s+|\s+\s|["\'\n\.:]+')

def tokenize (text):
  tokens = re.split(spacer_re, text)
  tokens = [stemmer.stem(w) for w in tokens if len(w) >= 2 and w.lower() not in sws]
  return tokens

for content in data:
  if content['id'] == 50:
    for topic in content['topics']:
      print(topic['title'])
      subtopics = sentence_split(topic['content'])
      for subtopic in subtopics:
        print(tokenize(subtopic))
      break