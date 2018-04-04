import os
import json
import re
import feedparser
import time

sources = [
  { 'name': 'G1', 'link': 'http://pox.globo.com/rss/g1/economia/' },
  { 'name': 'Governo', 'link': 'http://www.brasil.gov.br/rss/colecoes-de-rss/rss-economia-e-emprego' },
  { 'name': 'Folha', 'link': 'http://feeds.folha.uol.com.br/mercado/rss091.xml' },
  { 'name': 'O Globo', 'link': 'https://oglobo.globo.com/rss.xml?completo=true&secao=economia' },
  { 'name': 'InfoMoney', 'link': 'http://www.infomoney.com.br/ultimas-noticias/rss' },
  { 'name': 'Correio Braziliense', 'link': 'http://www.correiobraziliense.com.br/rss/noticia/economia/rss.xml' },
  { 'name': 'Jornal do Comércio RS', 'link': 'http://jcrs.uol.com.br/_conteudo/economia/rss.xml' }
]


def feeds_to_object (sources):
  obj_entries = []
  for source in sources:
    feed = feedparser.parse(source['link'])
    for entry in feed.entries:
        if re.match(r'(Banco Central)|(BC)', entry.title):
          obj = { 'source': source['name'] }
          if entry.title:
            obj['title'] = entry.title
          if entry.link:
            obj['link'] = entry.link
          if entry.published or entry.updated:
            obj['pub-date'] = entry.published or entry.updated
          if entry.summary_detail.value:
            obj['summary'] = entry.summary_detail.value
          obj_entries.append(obj)
  return obj_entries

documents = feeds_to_object(sources)

output_dir = '../output/rss'
if not os.path.isdir(output_dir):
  os.mkdir(output_dir)
with open('../output/rss/{}-bcb-news.json'.format(time.strftime('%Y-%m-%d')), 'w') as file:
  json.dump(documents, file)
