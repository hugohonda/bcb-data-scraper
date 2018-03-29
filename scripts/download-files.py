import os
from lxml import html
import requests

addresses = [
  {
    'url': 'http://portal.tcu.gov.br/transparencia/viagens/',
    'host': 'http://portal.tcu.gov.br/',
    'roots': ['http://portal.tcu.gov.br/lumis/portal/file/fileDownload.jsp?fileId='],
    'xpath': '//section/div/div/p/a',
    'dir': './data/tcu/'
  },
  {
    'url': 'http://www.fab.mil.br/voos',
    'host': 'http://www.fab.mil.br/',
    'roots': ['http://www.fab.mil.br/cabine/voos/'],
    'xpath': '//*[@id="content"]/div[@class="row"]/div/div/div[@class="datadia"]/a',
    'dir': './data/fab/'
  },
  {
    'url': 'http://portal.stf.jus.br/textos/verTexto.asp?servico=transparenciaPassagens',
    'host': 'http://portal.stf.jus.br/',
    'roots': ['http://www.stf.jus.br/arquivo/cms/transparenciaPassagens/anexo/'],
    'xpath': '//*[@id="lado_esquerdo"]/p/a',
    'dir': './data/stf/'
  },
  {
    'url': 'http://www.tse.jus.br/transparencia/pessoal/diarias-e-passagens',
    'host': 'http://www.tse.jus.br/',
    'roots': ['http://www.tse.jus.br/arquivos/', 'http://www.justicaeleitoral.jus.br/arquivos/'],
    'xpath': '//*[@id="ancora-1"]/p/a',
    'dir': './data/tse/'
  },
  {
    'url': 'https://www2.stm.jus.br/st2/index.php/ctrl_visualizacao/pesquisar_por_tipo/152/site',
    'host': 'https://www2.stm.jus.br/',
    'roots': ['https://www2.stm.jus.br/st2/index.php/ctrl_visualizacao/visualizar_pdf/'],
    'xpath': '/html/body/div/div[3]/div/a',
    'dir': './data/stm/internacional/'
  }
]

def address_stm():
  page = requests.get('https://www2.stm.jus.br/st2/index.php/ctrl_visualizacao/pesquisar_por_agrupador/15/site')
  tree = html.fromstring(page.content)
  links = tree.xpath('/html/body/div/div/div/div/a')
  for link in links:
    addresses.append({
      'url': link.get('href'),
      'host': 'https://www2.stm.jus.br/',
      'roots': ['https://www2.stm.jus.br/st2/index.php/ctrl_visualizacao/visualizar_pdf/'],
      'xpath': '/html/body/div/div[3]/div/a',
      'dir': './data/stm/nacional/'
    })

dirs = [
  './data',
  './data/tcu',
  './data/fab',
  './data/stf',
  './data/tse',
  './data/stm',
  './data/stm/internacional',
  './data/stm/nacional',
]

def check_dir (dir):
  if not os.path.isdir(dir):
    os.system('mkdir ' + dir)

def get_links (address):
  page = requests.get(address['url'])
  tree = html.fromstring(page.content)
  links = tree.xpath(address['xpath'])
  new_links = []
  for link in links:
    new_link = link.get('href').replace('../../', address['host'])
    new_links.append(new_link)
  address['links'] = new_links

def extract_transform (address):
  for url in address['links']:
    formatted = url
    for root in address['roots']:
      formatted = formatted.replace(root,'')
    formatted = address['dir'] + formatted
    if not formatted.endswith('.pdf'):
      formatted = formatted + '.pdf'
    if os.path.isfile(formatted):
      print('Already downloaded %s' % url)
    else:
      print('Downloading %s' % url)
      os.system('curl {0} -o {1}'.format(url, formatted))
      os.system('pdftotext {0} -table -enc UTF-8'.format(formatted))

def main ():
  address_stm()
  for dir in dirs:
    check_dir(dir)
  for address in addresses:
    get_links(address)
    extract_transform(address)

main()