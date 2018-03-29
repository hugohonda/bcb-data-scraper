import os
import json
import re
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfFileReader

def get_html_content_96_198 (url):
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  divs = soup.find_all('div', class_='lista1')
  text = ''
  for div in divs:
    text = text + div.text
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

print(get_html_content_96_198('https://www.bcb.gov.br/?COPOM132'))
