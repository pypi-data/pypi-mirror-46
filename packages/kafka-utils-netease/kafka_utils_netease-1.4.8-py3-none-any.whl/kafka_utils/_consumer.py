__all__ = ['Consumer']


import confluent_kafka
import gevent


class Consumer(confluent_kafka.Consumer):
    def consume(self, num_messages=1, *args, **kwargs):
        timeout = kwargs.get('timeout', None)
        msgs = confluent_kafka.Consumer.consume(
            self, num_messages=num_messages, timeout=0)
        with gevent.Timeout(timeout, False):
            while len(msgs) < num_messages:
                gevent.sleep(0.1)
                msgs += confluent_kafka.Consumer.consume(
                    self, num_messages=num_messages, timeout=0)
        return msgs

    def poll(self, timeout=None):
        msg = confluent_kafka.Consumer.poll(self, timeout=0)
        with gevent.Timeout(timeout, False):
            while msg is None:
                gevent.sleep(0.5)
                msg = confluent_kafka.Consumer.poll(self, timeout=0)
        return msg
