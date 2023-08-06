__all__ = ['MsgSenderLightweight']


import json
from ._default_callbacks import sender_suc_cb
from ._default_callbacks import sender_err_cb
from ._producer import Producer


class MsgSenderLightweight:
    def __init__(self, conf):
        self._producer = Producer(self._resolve_conf(conf))
        self._magic_number = 0x12345678

    def send_sync(
            self, topics, msgs, timeout=None,
            suc_cb=sender_suc_cb, err_cb=sender_err_cb):
        assert self._magic_number == 0x12345678
        self.send_async(topics, msgs, suc_cb, err_cb)
        self._producer.flush(timeout)

    def send_async(
            self, topics, msgs,
            suc_cb=sender_suc_cb, err_cb=sender_err_cb):
        if isinstance(topics, str):
            topics = [topics]
        assert isinstance(msgs, list)

        for topic in topics:
            for msg in msgs:
                try:
                    self._producer.produce(
                        topic,
                        self._serializer(msg),
                        on_delivery=self._make_delivery_callback(
                            suc_cb,
                            err_cb))
                except BufferError:
                    raise

    def close(self):
        pass

    def wait(self, timeout=None):
        return self._producer.flush(timeout)

    @staticmethod
    def _make_delivery_callback(suc_cb, err_cb):
        def delivery_callback(err, msg):
            if err is None:
                suc_cb(msg.value())
            else:
                err_cb(err.str())
        return delivery_callback

    @staticmethod
    def _resolve_conf(conf):
        confluent_kafka_conf = {}
        assert isinstance(conf, dict)
        assert 'brokers' in conf
        assert isinstance(conf['brokers'], str)
        confluent_kafka_conf['bootstrap.servers'] = conf['brokers']
        if 'exactly_once' in conf:
            assert isinstance(conf['exactly_once'], str)
            if conf['exactly_once'].lower() == 'true':
                confluent_kafka_conf['enable.idempotence'] = 'true'
        return confluent_kafka_conf

    @staticmethod
    def _serializer(msg):
        return json.dumps(msg)
