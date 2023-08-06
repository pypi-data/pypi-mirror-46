import confluent_kafka
import gevent


class Producer(confluent_kafka.Producer):
    def flush(self, timeout=None):
        pending_msgs = confluent_kafka.Producer.flush(self, timeout=0)
        with gevent.Timeout(timeout, False):
            while pending_msgs > 0:
                gevent.sleep(0.1)
                pending_msgs = confluent_kafka.Producer.flush(self, timeout=0)
        return pending_msgs
