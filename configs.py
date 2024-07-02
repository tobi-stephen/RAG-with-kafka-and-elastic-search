# kafka connection configurations, elastic search config

kafka_server = 'localhost:9098'

kafka_config: dict = {
    'producer': {
        'bootstrap.servers': kafka_server,
        'acks':              'all'
    },
    'consumer': {
        'bootstrap.servers': kafka_server,
        'group.id':          'search-index-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': 'false' # this allows to easily replay the same events in development
    }
}

# elastic search configuration
es_config: dict = {
    'hosts': 'https://localhost:9200',
    'basic_auth': ('elastic', 'BYdQVzTIuE56EpfNh=K8'), 
    'ssl_assert_fingerprint': 'd990855d1e11975a6d063b4624703868ab784bb441e93166444d43930f71322a'
}