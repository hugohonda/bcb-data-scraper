import os
import json
import re
import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from io import BytesIO
from PyPDF2 import PdfFileReader

def get_html_content_0_96 (url):
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  full_content = soup.find('div', {'class': 'conteudo'})
  print(url)
  return full_content.text

def get_html_content_97_199 (url):
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  comments = soup.find_all(string=lambda text:isinstance(text,Comment))
  text = ''
  for comment in comments:
    if comment == 'conteudo':
      contents = comment.find_all_next(text=True)
      for content in contents:
        text = text + ' ' + content
  print(url)
  return text

def get_html_content (url):
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  comments = soup.find_all(string=lambda text:isinstance(text,Comment))
  text = ''
  for comment in comments:
    if comment == 'conteudo':
      contents = comment.find_all_next(text=True)
      for content in contents:
        text = text + ' ' + content
  print(url)
  return text

def get_pdf_content (url):
  response = requests.get(url)
  pdf_file = BytesIO(response.content)
  pdf_reader = PdfFileReader(pdf_file)
  count = 0
  text = ''
  while count < pdf_reader.numPages:
      pageObj = pdf_reader.getPage(count)
      count += 1
      text += pageObj.extractText()
  print(url)
  return text

def get_records (initial_year, final_year):
  records = []
  for year in range(initial_year, final_year, 1):
    page = requests.get(f'https://www.bcb.gov.br/?id=ATACOPOM&ano={str(year)}')
    soup = BeautifulSoup(page.text, 'html.parser')
    months_list = soup.find(id='cronoGrupoMes').find_all('li')
    for month in reversed(months_list):
      try:
        link_href = month.find('a').get('href')
        link_details = month.text.strip()
        match = re.search(r'(\w+)\/(\d+)\s+-\s+(\d+).[\s\S]*?(\d{2}\/\d{2}\/\d{4})', link_details)
        obj = {
          'link': f'https://www.bcb.gov.br{link_href}',
          'month': match.group(1),
          'year': int(match.group(2)),
          'count': int(match.group(3)),
          'pub-date': match.group(4)
        }
        if obj['count'] <= 199:
          content_raw = get_html_content(obj['link'])
          content_type  = 0
        if obj['count'] >= 200:
          content_raw = get_pdf_content(obj['link'])
          content_type  = 1
        obj['content'] = {
          'raw': content_raw,
          'type': content_type
        }
        obj['id'] = 'COPOM' + str(obj['count'])
        records.append(obj)
      except Exception as error:
        print(f'erro: {error}')
  return records

initial = 1998
final = 2018
records = get_records(initial, final)
output_dir = '../output'

if not os.path.isdir(output_dir):
  os.mkdir(output_dir)
with open(f'{output_dir}/{initial}-{final}-copom-records.json', 'w') as file:
  json.dump(records, file)
