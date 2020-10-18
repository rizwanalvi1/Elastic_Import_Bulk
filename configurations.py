# elasticsearch configurations
host_addr = '192.168.18.74'
host_port = '9200'
elastic_username = 'elastic'
elastic_password = 'elastic123'
index_name = 'fbr_taxfile'
batch_size = 20000

file_path = 'D:\\AirUniversity\\FBR_Processing\\taxpayer_5000.csv'
# sr_no,taxpayer_name,registration_no,tax_paid
mapping = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            # "location" : {
            #   "type" : "geo_point"
            # },
            'sr_no': {"type": "integer"},
            # 'month': {"type": "date", "format": "dd-MMM-yy"},
            'taxpayer_name': {"type": "keyword"},
            'registration_no': {"type": "text"},
            'tax_paid': {"type": "long"}
        }
    }
}

query_body = {
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "District": "BAHAWALNAGAR"
          }
        }
      ]
    }
  }
}