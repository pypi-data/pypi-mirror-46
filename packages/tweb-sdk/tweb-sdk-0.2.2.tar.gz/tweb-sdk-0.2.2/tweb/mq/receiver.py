from kafka import KafkaConsumer
import config


def subscribe(topics, group):
    if type(topics) == list:
        temp = list()
        for m in topics:
            temp.append(m)
        tps = tuple(temp)
    elif type(topics) == tuple:
        tps = topics
    else:
        tps = tuple([topics])
    return KafkaConsumer(*tps, group_id=group, bootstrap_servers=config.KafkaServers)


def unsubscribe(consumer):
    if consumer is not None:
        consumer.close()
