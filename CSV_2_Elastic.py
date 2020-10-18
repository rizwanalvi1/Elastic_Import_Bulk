from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import ElasticsearchException
import csv
import uuid
import configurations as conf

# es=Elasticsearch([conf.host_addr+':'+conf.host_port],http_auth=(conf.elastic_username, conf.elastic_password))
es=Elasticsearch([conf.host_addr+':'+conf.host_port])

print(es.indices.delete(index=conf.index_name, ignore=[400, 404]))

response = es.indices.create(
    index=conf.index_name,
    body=conf.mapping,
    ignore=400 # ignore 400 already exists code
)

print('response:', response)

url = conf.file_path

iterator = 0
batch = 0
tmp_array = []

def insert_batch_in_elasticsearch(batch):
  actions = []
  # spamreader = csv.reader(batch, delimiter=',', quotechar='"')
  spamreader = csv.reader(batch, delimiter=',', quotechar='"')
  # "sr","taxpayer_name","registration_no","tax_paid"

  for row in spamreader:
      # print(row)
      if len(row[3]) > 0:
          doc = {
              'sr_no': int(row[0]),
              'taxpayer_name': row[1],
              'registration_no': row[2],
              'tax_paid': int(row[3]),
              # 'location':
              #     {
              #         "lat": row['lat'],
              #         "lon": row['lon']
              #     }
          }
          # print(doc)
          action = [{"_source": doc}]
          actions.append(action[0])

  try:
    response = helpers.bulk(es, actions, index=conf.index_name)
    print("\nRESPONSE:", response)
  except ElasticsearchException as e:
    print("\nERROR:", e)

with open(url) as infile:
  for line in infile:
      if line.find('sr_no') != 0:
          iterator = iterator + 1
          tmp_array.append(line)
          if iterator==conf.batch_size:
            batch = batch+1
            insert_batch_in_elasticsearch(tmp_array)
            iterator = 0
            tmp_array = []