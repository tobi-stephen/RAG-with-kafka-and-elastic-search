# The consume routine does 'data loading and indexing' three things
#   - reads from the `conversations` topic
#   - processes it by using llm to get embeddings
#   - stores the conversation alongside the embeddings
import logging
from typing import List

import llm
from search_client import Search

from configs import kafka_config, es_config
from confluent_kafka import Consumer


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def consume(topic: str) -> None:
    msg_count = 0
    logger.info('about to start consuming messages')
    
    search = Search(index=topic, **es_config)
    search.create_index()

    consumer = Consumer(kafka_config['consumer'])
    consumer.subscribe([topic])

    # Poll for new messages from Kafka and index into Elastic.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                pass
            elif msg.error():
                logger.error(f'ERROR: {msg.error()}')
            else:                
                # Loading
                topic=msg.topic()
                key=msg.key().decode('utf-8')
                value=msg.value().decode('utf-8')

                # Get Embeddings and normalize
                embedding_vector = llm.get_normalized_embedding(value)

                # Index in Elastic Search
                document = {
                    'conversation_id': key,
                    'conversation': value,
                    'conversation_vector': embedding_vector
                }

                search.index_document(key=key, document=document)

    except Exception as e:
        logger.info(f'consumer ending: {e}')
    finally:
        # Leave group and commit final offsets
        logger.info(f'{msg_count} messages consumed')
        consumer.close()


if __name__ == '__main__':
    topic = 'conversations'

    consume(topic=topic)
