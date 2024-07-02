#This routine has the Search client to be used as both a vector store and searching
import logging

from configs import es_config
from elasticsearch import Elasticsearch


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Search:
    def __init__(self, index, **configs) -> None:
        self.es = Elasticsearch(**configs)
        if self.es.ping():
            logger.info('elastic is ready!')
            self.index = index
        else:
            logger.info('elastic is not ready')

    def create_index(self, mappings=dict()) -> None:
        self.es.indices.delete(index=self.index, ignore_unavailable=True) # deleting index for dev testing
        resp = self.es.indices.create(index=self.index, mappings=mappings)
        logger.info(f'{self.index} create response: {resp}')
        logger.info(f'index mappings: {self.es.indices.get_mapping(index=self.index)}')
        return resp

    def index_document(self, key, document) -> None:
        resp = self.es.index(index=self.index, id=key, body=document)
        logger.info(f'Document with ID - {key} index response: {resp}')
        return resp

    def delete_document(self, key) -> None:
        resp = self.es.delete(index=self.index, id=key)
        logger.info(f'Document with ID - {key} index response: {resp}')
        return resp

    def search(self, debug=False, **query_args):
        resp = self.es.search(index=self.index, **query_args)
        if debug: logger.info(f'Document search response: {resp}')
        return resp
    
    def delete_index(self):
        resp = self.es.indices.delete(index=self.index, ignore_unavailable=True)
        logger.info(f'{self.index} delete response: {resp}')
        return resp


if __name__ == '__main__':
    es_index = 'conversations'

    search = Search(index=es_index, **es_config)

    search.create_index()
