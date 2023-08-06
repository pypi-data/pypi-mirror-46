from kafka_utils.confluent_producer import ConfluentProducer
from kafka_utils.kafka_python_producer import KafkaPythonProducer
from kafka_utils import MAX_PARTITION_NUMBER
from kafka_utils.consistent_partitioner import ConsistentPartitioner


class MsgSender(object):
    DEFAULT_CONFIG = {
        'brokers': 'localhost',
        'client.id': None,
        'partitions.num': None,
        'enable.consistent.partitioner': False,
        'topics': None,
        'support.utils': 'confluent',
        'required.acks': 1,
        'compression.type': 'None',
        'request.retries': 5,
        'request.retries.backoff.ms': 100,
        'request.timeout.ms': 300000,
        'buffering.max.memory': 1048576,
        'buffering.max.ms': 0,
        'batch.num.messages': 10000,
        'metadata.age.max.ms': 300000,
        'metadata.request.timeout.ms': 300000,
        'nagle.enbale': True,
        'reconnect.backoff.ms': 50,
        'reconnect.timeout.ms': 30000,
        'max.in.flight.requests.per.connection': 1000000,
        'exactly.once': False,
        'security.protocol': 'PLAINTEXT',
        'ssl.cafile': 'None',
        'ssl.certfile': 'None',
        'ssl.keyfile': 'None',
        'ssl.password': 'None',
        'sasl.mechanism': 'GSSAPI',
        'sasl.username': 'None',
        'sasl.password': 'None'
    }

    def __init__(self, configs):
        self._topics = list()
        self._partition_nums = list()
        self._producer_type = ConfluentProducer
        self._consistent_hash = False
        self._consistent_hasher = None
        configure = self._resolve_conf(configs)
        self._producer = self._producer_type(configure)
        self._create_partitions()
        if self._consistent_hash:
            self._consistent_hasher = self._create_consistent_partitioner()

    def _create_consistent_partitioner(self):
        for i in range(len(self._partition_nums)):
            if self._partition_nums[i] == 0:
                self._partition_nums[i] = self.get_partition_num_for_topic(self._topics[i])
        return ConsistentPartitioner(self._topics, self._partition_nums)

    def _resolve_conf(self, conf):
        if not isinstance(conf, dict):
            raise TypeError('configure must be of type dict')
        if 'brokers' not in conf:
            raise ValueError('the configuration must contains brokers')
        if 'support.utils' in conf:
            if conf.pop('support.utils') == 'kafka-python':
                self._producer_type = KafkaPythonProducer

        if 'enable.consistent.partitioner' in conf:
            if conf.pop('enable.consistent.partitioner'):
                self._consistent_hash = True

        if 'partitions.num' in conf:
            if not isinstance(conf['partitions.num'], list):
                raise TypeError('partitions must be of type list')
            if 'topics' not in conf:
                raise ValueError('topics must be specified with the partitions.num option')

        if 'topics' in conf:
            if not isinstance(conf['topics'], list):
                raise TypeError('topics must be of type list')
            self._topics = conf.pop('topics')
            if 'partitions.num' in conf:
                self._partition_nums = conf.pop('partitions.num')
                if len(self._partition_nums) != len(self._topics):
                    raise ValueError('topics must be of the same length as partitions.num')
            else:
                self._partition_nums = [0 for _ in range(len(self._topics))]

        if self._producer_type is ConfluentProducer:
            configure = self._resolve_confluent_conf(conf)
        elif self._producer_type is KafkaPythonProducer:
            configure = self._resolve_kafka_python_conf(conf)
        else:
            configure = None

        if len(conf) > 0:
            unrecognized_options = ''
            for item in conf:
                unrecognized_options += (str(item) + ', ')
            unrecognized_options = unrecognized_options[:len(unrecognized_options)-2]
            raise ValueError('unrecognized options: ' + unrecognized_options)

        return configure

    @staticmethod
    def _resolve_kafka_python_conf(conf):
        return None

    @staticmethod
    def _resolve_confluent_conf(conf):
        configure = dict()

        assert 'brokers' in conf
        configure['bootstrap.servers'] = conf.pop('brokers')
        configure['client.id'] = conf.pop(
            'client.id') if 'client.id' in conf \
            else MsgSender.DEFAULT_CONFIG['client.id']
        configure['acks'] = conf.pop(
            'required.acks') if 'required.acks' in conf \
            else MsgSender.DEFAULT_CONFIG['required.acks']
        configure['compression.codec'] = conf.pop(
            'compression.type') if 'compression.type' in conf \
            else MsgSender.DEFAULT_CONFIG['compression.type']
        configure['retries'] = conf.pop(
            'request.retries') if 'request.retries' in conf \
            else MsgSender.DEFAULT_CONFIG['request.retries']
        configure['retry.backoff.ms'] = conf.pop(
            'request.retries.backoff.ms') if 'request.retries.backoff.ms' in conf \
            else MsgSender.DEFAULT_CONFIG['request.retries.backoff.ms']
        configure['delivery.timeout.ms'] = conf.pop(
            'request.timeout.ms') if 'request.timeout.ms' in conf \
            else MsgSender.DEFAULT_CONFIG['request.timeout.ms']
        configure['queue.buffering.max.kbytes'] = conf.pop(
            'buffering.max.memory') if 'buffering.max.memory' in conf \
            else MsgSender.DEFAULT_CONFIG['buffering.max.memory']
        configure['queue.buffering.max.ms'] = conf.pop(
            'buffering.max.ms') if 'buffering.max.ms' in conf \
            else MsgSender.DEFAULT_CONFIG['buffering.max.ms']
        configure['batch.num.messages'] = conf.pop(
            'batch.num.messages') if 'batch.num.messages' in conf \
            else MsgSender.DEFAULT_CONFIG['batch.num.messages']
        configure['metadata.max.age.ms'] = conf.pop(
            'metadata.age.max.ms') if 'metadata.age.max.ms' in conf \
            else MsgSender.DEFAULT_CONFIG['metadata.age.max.ms']
        configure['socket.nagle.disable'] = True if 'nagle.enbale' in conf and not conf.pop(
            'nagle.enbale') else False
        configure['reconnect.backoff.ms'] = conf.pop(
            'reconnect.backoff.ms') if 'reconnect.backoff.ms' in conf \
            else MsgSender.DEFAULT_CONFIG['reconnect.backoff.ms']
        configure['reconnect.backoff.max.ms'] = conf.pop(
            'reconnect.timeout.ms') if 'reconnect.timeout.ms' in conf \
            else MsgSender.DEFAULT_CONFIG['reconnect.timeout.ms']
        configure['max.in.flight'] = conf.pop(
            'max.in.flight.requests.per.connection') if 'max.in.flight.requests.per.connection' in conf \
            else MsgSender.DEFAULT_CONFIG['max.in.flight.requests.per.connection']
        configure['security.protocol'] = conf.pop(
            'security.protocol') if 'security.protocol' in conf \
            else MsgSender.DEFAULT_CONFIG['security.protocol']
        configure['ssl.ca.location'] = conf.pop(
            'ssl.cafile') if 'ssl.cafile' in conf \
            else MsgSender.DEFAULT_CONFIG['ssl.cafile']
        configure['ssl.certificate.location'] = conf.pop(
            'ssl.certfile') if 'ssl.certfile' in conf \
            else MsgSender.DEFAULT_CONFIG['ssl.certfile']
        configure['ssl.key.location'] = conf.pop(
            'ssl.keyfile') if 'ssl.key.location' in conf \
            else MsgSender.DEFAULT_CONFIG['ssl.keyfile']
        configure['ssl.key.password'] = conf.pop(
            'ssl.password') if 'ssl.password' in conf \
            else MsgSender.DEFAULT_CONFIG['ssl.password']
        configure['sasl.mechanism'] = conf.pop(
            'sasl.mechanism') if 'sasl.mechanism' in conf \
            else MsgSender.DEFAULT_CONFIG['sasl.mechanism']
        configure['sasl.username'] = conf.pop(
            'sasl.username') if 'sasl.username' in conf \
            else MsgSender.DEFAULT_CONFIG['sasl.username']
        configure['sasl.password'] = conf.pop(
            'sasl.password') if 'sasl.password' in conf \
            else MsgSender.DEFAULT_CONFIG['sasl.password']
        configure['metadata.request.timeout.ms'] = conf.pop(
            'metadata.request.timeout.ms') if 'metadata.request.timeout.ms' in conf \
            else MsgSender.DEFAULT_CONFIG['metadata.request.timeout.ms']

        if 'exactly.once' in conf:
            if conf.pop('exactly.once'):
                configure['enable.idempotence'] = True
                configure['enable.gapless.guarantee'] = True
        return configure

    @staticmethod
    def _check_partition_nums(partition_num):
        if partition_num < 0 or partition_num > MAX_PARTITION_NUMBER:
            raise ValueError('invalid partition num')

    def _create_partitions(self):
        for i in range(len(self._topics)):
            self._check_partition_nums(self._partition_nums[i])
            if self._partition_nums[i] > 0:
                self._producer.create_enough_partition(self._topics[i], self._partition_nums[i])

    def send_sync(self, key, value, suc_cb=None, err_cb=None, timeout=None, topics=None):
        self.send_async(key, value, suc_cb, err_cb, topics)
        self._producer.flush(timeout)

    def send_async(self, key, value, suc_cb=None, err_cb=None, topics=None):
        if topics is None:
            topics = self._topics
        if not isinstance(key, str):
            raise TypeError('key must be of type str')
        for topic in topics:
            if self._consistent_hash:
                partition = self._consistent_hasher.get_key(topic, key)
                self._producer.send_msg(topic, key, value, suc_cb, err_cb, partition=partition)
            else:
                self._producer.send_msg(topic, key, value, suc_cb, err_cb)

    def flush(self, timeout=None):
        self._producer.flush(timeout)

    def set_topics(self, topics, partition_nums=None):
        if not isinstance(topics, list):
            raise TypeError('topics must be of type list')

        if partition_nums is not None:
            if not isinstance(partition_nums, list):
                raise TypeError('partition_nums must be of type list')
            if len(topics) != len(partition_nums):
                raise ValueError('topics must be of the same length as partition_nums')
        else:
            partition_nums = [0 for _ in range(len(topics))]

        self._topics = topics
        self._partition_nums = partition_nums
        self._create_partitions()
        if self._consistent_hasher:
            self._partitioner = self._create_consistent_partitioner()

    def get_partition_num_for_topic(self, topic):
        return self._producer.get_partition_num(topic)

    def get_existing_topics(self):
        return self._producer.get_existing_topics()

    def close(self):
        pass

