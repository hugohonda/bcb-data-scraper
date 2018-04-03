# criar conta no https://developer.twitter.com/
# criar uma nova applicação no https://apps.twitter.com/ e salvar credenciais
# instalar wrapper da API do twitter: pip install tweepy
import tweepy
import json
import os
import time

consumer_key = 'szwXZgsFxKKHQl1feQy40PnY6'
consumer_secret = 'v7s3yvBjZXMuwOh4y7k0hX3RR2RIMXKnRa1KnICxOBaoy9hEZi'
access_token = '2479807915-3clxGGyrm0FnDPGXKeYoiRm2Jo0DOQ1MtdjMH2T'
access_token_secret = 'rurN0vj4AEXnMx0ffaWXn80ddD6cZT121EBBRYUhKkS4f'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

if (not api):
  print ('Falha ao conectar com a API')

# Geo ID do Brasil e de Brasília
# brasil_places = api.geo_search(query='Brasil', granularity='country')
# brasil_id = brasil_places[0].id
# print('Brasil Geo ID: ', brasil_id)
brasil_id = '1b107df3ccc0aaa1'
print(f'Brasil Geo ID:  {brasil_id}')

# Checar quantidade de queries restantes usando o método rate_limit_status()
print('Queries restantes: ', api.rate_limit_status()['resources']['search']['/search/tweets'])

query = f'place:{brasil_id} lang:pt (banco central) OR #bancocentral OR #ipca OR # OR #economia OR #selic OR selic OR #RelatóriodeInflação OR #EstatísticasFiscais OR Copom OR #Copom'
max_tweets = 10000

def data_into_file (data):
  with open('fetched_tweets.txt','a') as tf:
      tf.write(data)

tweets = []
fetched_tweets = [status for status in tweepy.Cursor(api.search, q=query, tweet_mode='extended').items(max_tweets)]
for tweet in fetched_tweets:
  if 'RT @' not in tweet.full_text:
    tweets.append(tweet.full_text)

output_dir = '../output/twitter'
if not os.path.isdir(output_dir):
  os.mkdir(output_dir)
with open('../output/twitter/{}-bcb-tweets.json'.format(time.strftime('%Y-%m-%d')), 'w') as file:
  json.dump(tweets, file)