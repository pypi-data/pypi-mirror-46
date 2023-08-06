__all__ = ['MsgSenderGeventSingleThread']


import json
import gevent
import gevent.event
from ._producer import Producer
from ._buffer import Buffer
from ._default_callbacks import sender_suc_cb
from ._default_callbacks import sender_err_cb
from ._msg import Msg


class MsgSenderGeventSingleThread:
    def __init__(self, conf):

        self._cur_buffer = Buffer()
        self._next_buffer = Buffer()
        self._buffers_to_send = []

        self._buffer_not_empty = gevent.event.Event()
        self._flush_finished = gevent.event.Event()

        self._running = False
        self._routine_started = gevent.event.Event()
        self._controller_routine = gevent.spawn(self._controller_task)

        configure = self._resolve_conf(conf)
        self._producer = Producer(configure)

        self._start_controller_routine()  # start the controller routine
        self._magic_number = 0x12345678  # just in case!

    def send_sync(
            self, topic, msgs, timeout=None,
            suc_cb=sender_suc_cb, err_cb=sender_err_cb):
        assert self._magic_number == 0x12345678
        self._put_msgs_in_buffer(topic, msgs, suc_cb, err_cb)
        self._wait_for_msgs_to_deliver(timeout)

    def send_async(
            self, topics, msgs,
            suc_cb=sender_suc_cb, err_cb=sender_err_cb):
        assert self._magic_number == 0x12345678
        self._put_msgs_in_buffer(topics, msgs, suc_cb, err_cb)

    def wait(self, timeout=None):
        assert self._magic_number == 0x12345678
        self._wait_for_msgs_to_deliver(timeout)

    def close(self):
        assert self._magic_number == 0x12345678
        self._stop_controller_routine()
        self._magic_number = 0

    def _put_msgs_in_buffer(
            self, topics, raw_msgs,
            suc_cb, err_cb):
        if self._cur_buffer.writable_count() >= len(raw_msgs):
            self._cur_buffer.append(
                self.create_msg_objects(
                    topics, raw_msgs, suc_cb, err_cb))
        else:
            self._buffers_to_send.append(self._cur_buffer)
            self._cur_buffer = None
            if self._next_buffer is not None:
                self._cur_buffer = self._next_buffer
                self._next_buffer = None
            else:
                self._cur_buffer = Buffer()

            self._cur_buffer.append(
                self.create_msg_objects(
                    topics, raw_msgs, suc_cb, err_cb))

            self._buffer_not_empty.set()

    @staticmethod
    def create_msg_objects(topics, raw_msgs, suc_cb, err_cb):
        assert isinstance(raw_msgs, list)
        assert isinstance(topics, str) or isinstance(topics, list)
        msgs = []
        if isinstance(topics, str):
            for raw_msg in raw_msgs:
                msgs.append(Msg([topics], raw_msg, suc_cb, err_cb))
        else:
            for raw_msg in raw_msgs:
                msgs.append(Msg(topics, raw_msg, suc_cb, err_cb))
        return msgs

    def _wait_for_msgs_to_deliver(self, timeout=None):
        self._flush_finished.clear()
        self._flush_finished.wait(timeout)

    def _controller_task(self):
        self._routine_started.wait()
        while self._running:
            if not self._buffers_to_send:
                self._buffer_not_empty.clear()
                self._buffer_not_empty.wait(timeout=0.5)
                if not self._buffers_to_send and \
                        not self._cur_buffer.readable_count():
                    self._flush_finished.set()

            self._buffers_to_send.append(self._cur_buffer)
            self._cur_buffer = None

            msgs = []
            for buffer in self._buffers_to_send:
                msgs += buffer.retrieve_all()
                buffer.clear()

            self._buffers_to_send = self._buffers_to_send[:2]
            assert self._cur_buffer is None
            self._cur_buffer = self._buffers_to_send[0]
            if self._next_buffer is None:
                assert len(self._buffers_to_send) == 2
                self._next_buffer = self._buffers_to_send[1]
            self._buffers_to_send = []

            self._producer_task(msgs)

    def _start_controller_routine(self):
        self._running = True
        self._routine_started.set()

    def _stop_controller_routine(self):
        self._running = False
        self._buffer_not_empty.set()
        self._controller_routine.join()

    @staticmethod
    def _serializer(msg):
        return json.dumps(msg)

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

    def _producer_task(self, msgs):
        for msg in msgs:
            for topic in msg.topics:
                try:
                    self._producer.produce(
                        topic, self._serializer(msg.payload),
                        on_delivery=self._make_delivery_callback(
                            msg.success_callback, msg.err_callback))
                except BufferError:
                    self._producer.flush()
        self._producer.flush()

    @staticmethod
    def _make_delivery_callback(suc_cb, err_cb):
        def delivery_callback(err, msg):
            if err is None:
                suc_cb(msg.value())
            else:
                err_cb(err.str())
        return delivery_callback
