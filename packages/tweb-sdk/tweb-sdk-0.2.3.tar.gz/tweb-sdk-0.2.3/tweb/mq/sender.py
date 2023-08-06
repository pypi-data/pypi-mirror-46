from kafka import KafkaProducer
import config
import json
import logging

_producer = KafkaProducer(bootstrap_servers=config.KafkaServers,
                          value_serializer=lambda m: json.dumps(m).encode('utf-8'))


def send(topic, key, data):
    if type(key) == str:
        key = key.encode('utf-8')
    future = _producer.send(topic, key=key, value=data)
    future.add_callback(lambda meta: {
        logging.debug('Kafka send success: [%s] %s:%s:%s' % (key, meta.topic, meta.partition, meta.offset))
    })
    future.add_errback(lambda e: {
        logging.error('Kafka producer error', exc_info=e)
    })
