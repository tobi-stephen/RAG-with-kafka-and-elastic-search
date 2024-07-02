#This routine queries the LLM with context provided via semantic search in Elastic
import logging

import llm
from configs import es_config
from search_client import Search


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

es_index = 'conversations'
search = Search(index=es_index, **es_config)


def query_with_rag(data: dict):
        
    try:
        user_query = data.get('query')

        # Retrieval: Get contexts from Elastic Search

        # Pack the query args with the embeddings for the query
        query_args = {
            'knn': {
                'field': 'conversation_vector',
                'query_vector': llm.get_normalized_embedding(user_query),
                'num_candidates': 20,
                'k': 4
                # 'filters': {} this can be added to further refine the search with BM-25
            },
            'source': ['conversation_id', 'conversation'],
            # '_source': False
        }

        results = search.search(**query_args)
        logger.info(f'contexts derived with {results['hits']['total']['value']} results')
        
        # Augmentation: pack the results with the user's query
        augmented_query = []
        context_query = ''
        for hit in results['hits']['hits']:
            conversation = hit['_source']['conversation']
            context_query += conversation
            context_query += '\n'
        
        augmented_query.append({'role': 'assistant', 'content': context_query})
        augmented_query.append({'role': 'user', 'content': user_query})

        # Generation: with the query augmented, we can pass to LLM for generating an answer
        answer = llm.prompt(augmented_query)
        logger.info(f'LLM Prompt: {answer}')

        response = {
            'status': 'ok',
            'data': answer
        }

    except Exception as e:
        logger.error(f'Query error: {e}')
        response = {'status': 'internal error', 'data': []}
    finally:
        return response


if __name__ == '__main__':
    data = {
        'query': 'Give me summary of non-water related issues'
    }
    query_with_rag(data)
