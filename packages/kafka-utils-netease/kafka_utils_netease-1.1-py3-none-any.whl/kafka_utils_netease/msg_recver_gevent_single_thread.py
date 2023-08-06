__all__ = ['MsgRecver']


import json
import gevent
import gevent.event
from _buffer import Buffer
from _consumer import Consumer
from _default_callbacks import recver_suc_cb
from _default_callbacks import recver_err_cb
from kafka_msg import KafkaMsg


class MsgRecver:
    def __init__(self, conf):

        self._recv_cur_buffer = Buffer()
        self._recv_next_buffer = Buffer()
        self._buffers_to_change_recv = []
        self._msgs = []

        self._recv_buffer_empty = gevent.event.Event()
        self._recv_buffer_not_empty = gevent.event.Event()

        configure = self._resolve_conf(conf)
        self._consumer = Consumer(configure)

        self._recv_running = False
        self._recv_started = gevent.event.Event()
        self._recv_routine = gevent.spawn(self._recv_task)

        self._consume_started = gevent.event.Event()
        self._consume_running = False
        self._consume_routine = gevent.spawn(self._consume_task)

        self._consume_cur_buffer = Buffer()
        self._consume_next_buffer = Buffer()
        self._buffers_to_change_consume = []
        self._cbs = []

        self._consume_buffer_not_empty = gevent.event.Event()
        self._consume_finished = gevent.event.Event()

        self._start_recv_routine()
        self._start_consume_routine()

        self._magic_number = 0x87654321

    def consume_sync(
            self,
            timeout=None,
            suc_cb=recver_suc_cb,
            err_cb=recver_err_cb):
        assert self._magic_number == 0x87654321
        self._put_callbacks_in_consume_buffer(
            [self._make_user_callback(suc_cb, err_cb)])
        self._consume_buffer_not_empty.set()
        self._consume_finished.clear()
        self._consume_finished.wait(timeout)

    def consume_async(self, suc_cb=recver_suc_cb, err_cb=recver_err_cb):
        assert self._magic_number == 0x87654321
        self._put_callbacks_in_consume_buffer(
            [self._make_user_callback(suc_cb, err_cb)])
        self._consume_buffer_not_empty.set()

    def wait(self, timeout=None):
        assert self._magic_number == 0x87654321
        self._wait_for_callbacks_finished(timeout)

    def _wait_for_callbacks_finished(self, timeout=None):
        assert self._magic_number == 0x87654321
        self._consume_finished.clear()
        self._consume_finished.wait(timeout)

    def close(self):
        assert self._magic_number == 0x87654321
        self._stop_consume_routine()
        self._stop_recv_routine()
        self._magic_number = 0

    def subscribe(self, topics):
        assert self._magic_number == 0x87654321
        assert isinstance(topics, list)
        self._consumer.subscribe(topics)

    def unsubscribe(self, timeout=None):
        assert self._magic_number == 0x87654321

        self._wait_for_callbacks_finished(timeout)
        self._consumer.unsubscribe()
        self._msgs = []
        self._cbs = []

        if self._recv_cur_buffer is not None:
            self._recv_cur_buffer.clear()
        if self._recv_next_buffer is not None:
            self._recv_next_buffer.clear()

        assert self._consume_cur_buffer is not None
        self._consume_cur_buffer.clear()
        if self._consume_next_buffer is not None:
            self._consume_next_buffer.clear()

    def _start_recv_routine(self):
        self._recv_running = True
        self._recv_started.set()

    def _stop_recv_routine(self):
        self._recv_running = False
        self._recv_buffer_empty.set()
        self._recv_routine.join()

    def _start_consume_routine(self):
        self._consume_running = True
        self._consume_started.set()

    def _stop_consume_routine(self):
        self._consume_running = False

        if self._recv_cur_buffer is not None:
            self._recv_cur_buffer.clear()
        if self._recv_next_buffer is not None:
            self._recv_next_buffer.clear()
        self._recv_buffer_not_empty.set()

        assert self._consume_cur_buffer is not None
        self._consume_cur_buffer.clear()
        if self._consume_next_buffer is not None:
            self._consume_next_buffer.clear()
        self._consume_buffer_not_empty.set()

        self._consume_routine.join()

    def _put_msgs_in_recv_buffer(self, raw_msgs):
        assert isinstance(raw_msgs, list)
        if not raw_msgs:
            return
        if self._recv_cur_buffer.writable_count() >= len(raw_msgs):
            self._recv_cur_buffer.append(raw_msgs)
        else:
            self._buffers_to_change_recv.append(self._recv_cur_buffer)
            self._recv_cur_buffer = None
            if self._recv_next_buffer is not None:
                self._recv_cur_buffer = self._recv_next_buffer
                self._recv_next_buffer = None
            else:
                self._recv_buffer_empty.clear()
                self._recv_buffer_empty.wait()

            if self._recv_running:
                self._recv_cur_buffer.append(raw_msgs)

            self._recv_buffer_not_empty.set()

    def _put_callbacks_in_consume_buffer(self, raw_callbacks):
        assert raw_callbacks
        assert isinstance(raw_callbacks, list)

        if self._consume_cur_buffer.writable_count() >= len(raw_callbacks):
            self._consume_cur_buffer.append(raw_callbacks)
        else:
            self._buffers_to_change_consume.append(
                self._consume_cur_buffer)
            self._consume_cur_buffer = None
            if self._consume_next_buffer is not None:
                self._consume_cur_buffer = self._consume_next_buffer
                self._consume_next_buffer = None
            else:
                self._consume_cur_buffer = Buffer()

            self._consume_cur_buffer.append(raw_callbacks)

            self._consume_buffer_not_empty.set()

    def _recv_task(self):
        self._recv_started.wait()
        while self._recv_running:
            kafka_msgs = self._recv_task_inner()
            self._put_msgs_in_recv_buffer(kafka_msgs)
        self._consumer.close()

    def _recv_task_inner(self):
        return self._consumer.consume(
            num_messages=Buffer.MAX_BUFFER_SIZE, timeout=0.3)

    def _consume_task(self):
        self._consume_started.wait()

        recv_buffer_empty = True
        consume_buffer_empty = True

        while self._consume_running:
            if recv_buffer_empty:
                if not self._buffers_to_change_recv:
                    self._recv_buffer_not_empty.clear()
                    self._recv_buffer_not_empty.wait(timeout=0.5)
                if self._recv_cur_buffer is not None:
                    self._buffers_to_change_recv.append(self._recv_cur_buffer)
                    self._recv_cur_buffer = None

                for buffer in self._buffers_to_change_recv:
                    msgs = buffer.retrieve_all()
                    self._msgs += msgs
                    buffer.clear()

                self._buffers_to_change_recv = self._buffers_to_change_recv[:2]
                assert self._recv_cur_buffer is None
                self._recv_cur_buffer = self._buffers_to_change_recv[0]
                if self._recv_next_buffer is None:
                    assert len(self._buffers_to_change_recv) == 2
                    self._recv_next_buffer = self._buffers_to_change_recv[1]
                self._buffers_to_change_recv = []

                recv_buffer_empty = False
                self._recv_buffer_empty.set()

            if consume_buffer_empty:
                if not self._buffers_to_change_consume:
                    self._consume_buffer_not_empty.clear()
                    self._consume_buffer_not_empty.wait(timeout=0.5)
                    if not self._buffers_to_change_consume and \
                            not self._consume_cur_buffer.readable_count():
                        self._consume_finished.set()
                self._buffers_to_change_consume.append(
                    self._consume_cur_buffer)
                self._consume_cur_buffer = None

                for buffer in self._buffers_to_change_consume:
                    cbs = buffer.retrieve_all()
                    self._cbs += cbs
                    buffer.clear()

                self._buffers_to_change_consume = \
                    self._buffers_to_change_consume[:2]
                assert self._consume_cur_buffer is None
                self._consume_cur_buffer = self._buffers_to_change_consume[0]
                if self._consume_next_buffer is None:
                    assert len(self._buffers_to_change_consume) == 2
                    self._consume_next_buffer = \
                        self._buffers_to_change_consume[1]
                self._buffers_to_change_consume = []

                consume_buffer_empty = False

            self._consume_task_inner(self._msgs, self._cbs)

            if not self._msgs:
                recv_buffer_empty = True

            if not self._cbs:
                consume_buffer_empty = True

    def _consume_task_inner(self, msgs_recved, cbs_recved):
        while True:

            kafka_msg = None
            if msgs_recved:
                kafka_msg = msgs_recved[0]

            cb = None
            if cbs_recved:
                cb = cbs_recved[0]

            if kafka_msg is not None and cb is not None:
                cb(kafka_msg)
                msgs_recved.pop(0)
                cbs_recved.pop(0)
                self._consumer.store_offsets(kafka_msg)
            else:
                break

    @staticmethod
    def _deserializer(raw_msg):
        return json.loads(raw_msg)

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
                        kafka_msg.topic(), kafka_msg.partition()))
            else:
                err_cb(kafka_msg.error().str())
        return user_callback
