# The produce routine streams contextual information into a kafka topic
import logging
import json

from configs import config
from confluent_kafka import Producer


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_conversations(source):
   ''' Reads a json file and yield list of Conversation '''

   with open(file=source, mode='rt') as f:
       conversations_dict = json.loads(f.read())
      
   # Yield conversation objects using fields of interest.
   for item in conversations_dict:
       yield item['conversation_id'], item['conversation']


def on_delivery_cb(err, msg):
    if err:
        logger.error(f'ERROR: Message failed delivery: {err}')
    else:
        logger.info(f'Produced event to topic {topic}: key = {msg.key().decode('utf-8')}')


def produce(topic: str) -> None:
    producer = Producer(config['producer'])
    
    conversation_file = 'conversations.json' # This can be a database table to be integrated with kafka connect

    try:
        for key, value in get_conversations(source=conversation_file):
            key = str(key).encode()
            value = str(value).encode()
            producer.produce(topic, value, key, callback=on_delivery_cb)

            res = producer.poll(10)
            logger.info(f'{res} messages polled')
        
    except Exception as e:
        logger.info(f'error: {e}')
    finally:
        producer.flush()
        logger.info(f'producer flushed and closing!')


if __name__ == '__main__':
    topic = 'conversations'

    produce(topic=topic)
