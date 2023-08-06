from hash_ring import HashRing


class ConsistentPartitioner(object):
    def __init__(self, topics, partition_numbers):
        self._hashers = {}
        for i in range(len(topics)):
            keys = [key for key in range(partition_numbers[i])]
            self._hashers[topics[i]] = HashRing(keys)

    def get_key(self, topic, key):
        return self._hashers[topic].get_node(key)



