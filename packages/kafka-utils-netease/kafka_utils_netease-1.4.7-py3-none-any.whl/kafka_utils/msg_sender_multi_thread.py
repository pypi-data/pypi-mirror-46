__all__ = ['MsgSenderMultiThread']


import threading
import json
from gevent import monkey

import confluent_kafka
from ._buffer import Buffer
from ._msg import Msg
from ._default_callbacks import sender_suc_cb
from ._default_callbacks import sender_err_cb

_threading_patched = monkey.is_module_patched('threading')
if _threading_patched:
    import gevent.threadpool


class MsgSenderMultiThread:
    def __init__(self, conf):

        self._foreground_cur_buffer = Buffer()
        self._foreground_next_buffer = Buffer()
        self._buffers_to_send = []

        self._buffer_mutex = threading.Lock()
        self._buffer_not_empty_cond = threading.Condition(
            self._buffer_mutex)
        self._flush_finished_cond = threading.Condition(self._buffer_mutex)

        self._controller_thread = threading.Thread(
            target=self._controller_task)
        self._running = False
        self._thread_started = threading.Event()

        configure = self._resolve_conf(conf)
        self._producer = confluent_kafka.Producer(configure)

        self._start_controller_thread()
        self._magic_number = 0x12345678

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
        self._stop_controller_thread()
        self._magic_number = 0

    def _put_msgs_in_buffer(
            self, topics, raw_msgs,
            suc_cb, err_cb):
        with self._buffer_mutex:
            if self._foreground_cur_buffer.writable_count() >= len(raw_msgs):
                self._foreground_cur_buffer.append(
                    self.create_msg_objects(
                        topics, raw_msgs, suc_cb, err_cb))
            else:
                self._buffers_to_send.append(self._foreground_cur_buffer)
                self._foreground_cur_buffer = None
                if self._foreground_next_buffer is not None:
                    self._foreground_cur_buffer = self._foreground_next_buffer
                    self._foreground_next_buffer = None
                else:
                    self._foreground_cur_buffer = Buffer()

                self._foreground_cur_buffer.append(
                    self.create_msg_objects(
                        topics, raw_msgs, suc_cb, err_cb))

                self._buffer_not_empty_cond.notify()

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
        with self._buffer_mutex:
            self._flush_finished_cond.wait(timeout)

    def _controller_task(self):
        self._thread_started.set()
        if _threading_patched:
            thread_pool = gevent.threadpool.ThreadPool(1)

        background_cur_buffer = Buffer()
        background_next_buffer = Buffer()
        buffers_to_flush = []

        while self._running:
            with self._buffer_mutex:
                if not self._buffers_to_send:
                    self._buffer_not_empty_cond.wait(
                        timeout=0.5)
                    if not self._buffers_to_send and \
                            not self._foreground_cur_buffer.readable_count():
                        self._flush_finished_cond.notify()

                self._buffers_to_send.append(self._foreground_cur_buffer)
                self._foreground_cur_buffer = background_cur_buffer
                background_cur_buffer = None
                self._buffers_to_send, buffers_to_flush \
                    = buffers_to_flush, self._buffers_to_send
                if self._foreground_next_buffer is None:
                    self._foreground_next_buffer = background_next_buffer
                    background_next_buffer = None

            msgs = []
            for buffer in buffers_to_flush:
                msgs += buffer.retrieve_all()
                buffer.clear()

            if msgs:
                if _threading_patched:
                    a_result = thread_pool.spawn(self._producer_task, msgs)
                    a_result.get()
                else:
                    self._producer_task(msgs)

            buffers_to_flush = buffers_to_flush[:2]

            assert background_cur_buffer is None
            background_cur_buffer = buffers_to_flush[0]

            if background_next_buffer is None:
                assert len(buffers_to_flush) == 2
                background_next_buffer = buffers_to_flush[1]

            buffers_to_flush = []
        if _threading_patched:
            thread_pool.join()

    def _start_controller_thread(self):
        self._running = True
        self._controller_thread.start()
        self._thread_started.wait()

    def _stop_controller_thread(self):
        self._running = False
        with self._buffer_mutex:
            self._buffer_not_empty_cond.notify()
        self._controller_thread.join()

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
