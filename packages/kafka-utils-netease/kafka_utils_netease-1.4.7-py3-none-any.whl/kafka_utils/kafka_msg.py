__all__ = ['KafkaMsg']


class KafkaMsg:
    def __init__(self, msg_value, topic, partition):
        self.payload = msg_value
        self.topic = topic
        self.partition = partition
