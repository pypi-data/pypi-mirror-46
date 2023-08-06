

class KafkaMsg:
    def __init__(self, topic, key, value, timestamp, partition, offset):
        self._topic = topic
        self._key = key
        self._value = value
        self._timestamp = timestamp
        self._partition = partition
        self._offset = offset

    def __len__(self):
        return len(self._value)

    @property
    def topic(self):
        return self._topic

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def partition(self):
        return self._partition

    @property
    def offset(self):
        return self._offset
