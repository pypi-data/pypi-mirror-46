import gevent
import confluent_kafka
from confluent_kafka.admin import AdminClient, NewPartitions
from confluent_kafka import KafkaException
from confluent_kafka import TIMESTAMP_LOG_APPEND_TIME
from confluent_kafka import TIMESTAMP_NOT_AVAILABLE
from confluent_kafka import TIMESTAMP_CREATE_TIME
from kafka_utils import log
from kafka_utils.kafka_exceptions import GetMetaDataFailException
from kafka_utils.kafka_exceptions import PartitionCreationException
from kafka_utils.kafka_exceptions import BufferFullException
from kafka_utils.kafka_exceptions import ProduceFailException
from kafka_utils.kafka_tools import confluent_error_transform
from kafka_utils.kafka_tools import serializer
from kafka_utils.kafka_tools import deserializer
from kafka_utils.kafka_msg import KafkaMsg


class ConfluentProducer(confluent_kafka.Producer):
    def __init__(self, conf):
        assert 'metadata.request.timeout.ms' in conf
        if conf['metadata.request.timeout.ms'] < 0:
            raise ValueError('metadata request timeout can\'t be negative')
        self._metadata_request_timeout = conf.pop('metadata.request.timeout.ms') / 1000
        confluent_kafka.Producer.__init__(self, conf)
        assert 'bootstrap.servers' in conf
        self._admin = AdminClient({'bootstrap.servers': conf['bootstrap.servers']})

    def flush(self, timeout=None):
        pending_msgs = confluent_kafka.Producer.flush(self, timeout=0)
        with gevent.Timeout(timeout, False):
            while pending_msgs > 0:
                gevent.sleep(0.1)
                pending_msgs = confluent_kafka.Producer.flush(self, timeout=0)
        return pending_msgs

    def create_enough_partition(self, topic, partition_num, timeout=None):
        try:
            cur_num = self.get_partition_num(topic)
        except GetMetaDataFailException as e:
            log.error('failed to get partition num from cluster metadata')
            raise PartitionCreationException from e
        if cur_num > partition_num:
            log.error('can\'t decrease the number of partitions')
            return
        elif cur_num == partition_num:
            log.info('no need to create partitions')
            return

        new_parts = [NewPartitions(topic, int(partition_num))]

        try:
            fs = self._admin.create_partitions(new_parts, validate_only=False)
        except KafkaException as e:
            log.error('partition creation failed')
            raise PartitionCreationException from e
        except TypeError or ValueError:
            log.error('partition creation failed due to invalid input')
            raise

        for topic, f in fs.items():
            try:
                f.result()
                self._wait_partition_creation(topic, partition_num, timeout)
            except GetMetaDataFailException as e:
                log.error('failed to get partition num from cluster metadata')
                raise PartitionCreationException from e
            except Exception as e:
                log.error('partition creation failed')
                raise PartitionCreationException from e

    def get_partition_num(self, topic):
        try:
            metadata = self.list_topics(topic, timeout=self._metadata_request_timeout)
            return len(metadata.topics[topic].partitions)
        except KafkaException as e:
            raise GetMetaDataFailException from e

    def get_existing_topics(self):
        try:
            metadata = self.list_topics(timeout=self._metadata_request_timeout)
        except KafkaException as e:
            raise GetMetaDataFailException from e
        topics = []
        for topic in metadata.topics:
            topics.append(topic)
        return topics

    def _wait_partition_creation(self, topic, target_num, timeout):
        with gevent.Timeout(timeout, False):
            while True:
                try:
                    num = self.get_partition_num(topic)
                except GetMetaDataFailException:
                    raise
                if num == target_num:
                    break
                else:
                    gevent.sleep(0.1)

    def send_msg(self, topic, key, msg, suc_cb=None, err_cb=None, partition=-1):
        assert isinstance(key, str)
        s_msg = serializer(msg)
        try:
            confluent_kafka.Producer.produce(self, topic, s_msg, key=key, partition=partition,
                                             on_delivery=self._make_delivery_callback(suc_cb, err_cb))
        except BufferError as e:
            raise BufferFullException from e
        except KafkaException as e:
            error = e.args[0]
            log.error('produce failed due to ' + error.str())
            raise ProduceFailException from e
        except NotImplementedError as e:
            log.error('produce failed due to lack of timestamp support')
            raise ProduceFailException from e

    def _make_delivery_callback(self, suc_cb, err_cb):
        def dummy_callback(_, _2):
            pass

        def delivery_callback(err, msg):
            if err is not None:
                err_cb(confluent_error_transform(err))
            elif msg.error() is not None:
                err_cb(confluent_error_transform(msg.error()))
            else:
                suc_cb(self._create_kafka_msg(msg))

        if suc_cb is None or err_cb is None:
            return dummy_callback
        return delivery_callback

    @staticmethod
    def _create_kafka_msg(confluent_msg):
        assert confluent_msg.error() is None
        topic = confluent_msg.topic()
        key = confluent_msg.key()
        value = deserializer(confluent_msg.value())
        timestamp = confluent_msg.timestamp()
        assert isinstance(timestamp, tuple) and len(timestamp) == 2
        if timestamp[0] == TIMESTAMP_NOT_AVAILABLE:
            timestamp = ('TIMESTAMP_NOT_IMPLEMENTED', None)
        elif timestamp[0] == TIMESTAMP_CREATE_TIME:
            timestamp = ('TIMESTAMP_CREATION_TIME', timestamp[1])
        else:
            assert timestamp[0] == TIMESTAMP_LOG_APPEND_TIME
            timestamp = ('TIMESTAMP_BROKER_RECEIVE_TIME', timestamp[1])
        partition = confluent_msg.partition()
        offset = confluent_msg.offset()
        return KafkaMsg(topic, key, value, timestamp, partition, offset)

