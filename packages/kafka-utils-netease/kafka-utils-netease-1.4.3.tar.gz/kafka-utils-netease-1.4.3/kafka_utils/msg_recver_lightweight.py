__all__ = ['MsgRecverLightweight']


import json
import gevent
import gevent.queue
import gevent.event
from .kafka_msg import KafkaMsg
from ._consumer import Consumer
from ._default_callbacks import recver_suc_cb
from ._default_callbacks import recver_err_cb
from ._default_callbacks import dummy_cb


class MsgRecverLightweight:
    def __init__(self, conf):
        self._consumer = Consumer(self._resolve_conf(conf))
        self._cb_queue = gevent.queue.JoinableQueue(None)
        self._work_routine = gevent.spawn(self._work)
        self._work_routine_start = gevent.event.Event()
        self._work_running = False
        self._start_work_routine()

        self._magic_number = 0x87654321

    def subscribe(self, topics):
        assert self._magic_number == 0x87654321
        assert isinstance(topics, list)
        self._consumer.subscribe(topics)

    def unsubscribe(self, timeout=None):
        assert self._magic_number == 0x87654321
        self.wait(timeout)
        self._consumer.unsubscribe()
        while True:
            try:
                self._cb_queue.get_nowait()
                self._cb_queue.task_done()
            except gevent.queue.Empty:
                break
        assert self._cb_queue.empty()

    def close(self):
        assert self._magic_number == 0x87654321
        self._stop_work_routine()
        self._consumer.close()
        self._magic_number = 0

    def consume_sync(
            self,
            timeout=None,
            suc_cb=recver_suc_cb,
            err_cb=recver_err_cb):
        assert self._magic_number == 0x87654321
        self._cb_queue.put(self._make_user_callback(suc_cb, err_cb))
        self.wait(timeout)

    def consume_async(self, suc_cb=recver_suc_cb, err_cb=recver_err_cb):
        assert self._magic_number == 0x87654321
        self._cb_queue.put(self._make_user_callback(suc_cb, err_cb))

    def wait(self, timeout=None):
        self._cb_queue.join(timeout)

    def _work(self):
        self._work_routine_start.wait()
        while self._work_running:
            cb = self._cb_queue.get()
            if self._work_running:
                msg = self._consumer.poll()
                assert msg is not None
                cb(msg)
                self._consumer.store_offsets(msg)
            self._cb_queue.task_done()

    def _start_work_routine(self):
        self._work_running = True
        self._work_routine_start.set()

    def _stop_work_routine(self):
        self._work_running = False
        self._cb_queue.put(self._make_user_callback(dummy_cb, dummy_cb))
        self._work_routine.join()

    @staticmethod
    def _resolve_conf(conf):
        confluent_kafka_conf = {}
        assert isinstance(conf, dict)
        assert 'brokers' in conf
        assert 'group_id' in conf
        assert isinstance(conf['brokers'], str)
        assert isinstance(conf['group_id'], str)
        confluent_kafka_conf['bootstrap.servers'] = conf['brokers']
        confluent_kafka_conf['group.id'] = conf['group_id']
        confluent_kafka_conf['auto.offset.reset'] = 'smallest'
        confluent_kafka_conf['queue.buffering.max.ms'] = '50'
        confluent_kafka_conf['enable.auto.offset.store'] = 'false'
        return confluent_kafka_conf

    def _make_user_callback(self, suc_cb, err_cb):
        def user_callback(kafka_msg):
            if kafka_msg.error() is None:
                suc_cb(
                    KafkaMsg(
                        self._deserializer(
                            kafka_msg.value()),
                        kafka_msg.topic(),
                        kafka_msg.partition()))
            else:
                err_cb(kafka_msg.error().str())
        return user_callback

    @staticmethod
    def _deserializer(raw_msg):
        return json.loads(raw_msg)
