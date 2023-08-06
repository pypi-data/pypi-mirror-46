__all__ = ['MsgRecverGeventMultiThread']


import json
import gevent
import gevent.threadpool
import confluent_kafka

from ._gevent_cross_threads_synchronize import Lck
from ._gevent_cross_threads_synchronize import Cond
from ._gevent_cross_threads_synchronize import Evnt
from ._buffer import Buffer
from ._default_callbacks import recver_suc_cb
from ._default_callbacks import recver_err_cb
from .kafka_msg import KafkaMsg


class MsgRecverGeventMultiThread:
    def __init__(self, conf):

        self._recv_cur_buffer = Buffer()
        self._recv_next_buffer = Buffer()
        self._buffers_to_change_recv = []
        self._msgs = []

        self._recv_buffer_mutex = Lck()
        self._recv_buffer_empty_cond = Cond(
            self._recv_buffer_mutex)
        self._recv_buffer_not_empty_cond = Cond(
            self._recv_buffer_mutex)

        configure = self._resolve_conf(conf)
        self._consumer = confluent_kafka.Consumer(configure)

        self._recv_thread = gevent.threadpool.ThreadPool(1)
        self._recv_running = False
        self._recv_started = Evnt()

        self._consume_thread = gevent.threadpool.ThreadPool(1)
        self._consume_running = False
        self._consume_started = Evnt()

        self._consume_cur_buffer = Buffer()
        self._consume_next_buffer = Buffer()
        self._buffers_to_change_consume = []
        self._cbs = []

        self._msg_cb_lock = Lck()

        self._consume_buffer_mutex = Lck()
        self._consume_buffer_not_empty_cond = Cond(
            self._consume_buffer_mutex)
        self._consume_finished_cond = Cond(
            self._consume_buffer_mutex)

        self._start_recv_thread()
        self._start_consume_thread()

        self._magic_number = 0x87654321

    def consume_sync(
            self,
            timeout=None,
            suc_cb=recver_suc_cb,
            err_cb=recver_err_cb):
        assert self._magic_number == 0x87654321
        self._put_callbacks_in_consume_buffer(
            [self._make_user_callback(suc_cb, err_cb)])
        with self._consume_buffer_mutex:
            self._consume_buffer_not_empty_cond.notify()
            self._consume_finished_cond.wait(timeout)

    def consume_async(self, suc_cb=recver_suc_cb, err_cb=recver_err_cb):
        assert self._magic_number == 0x87654321
        self._put_callbacks_in_consume_buffer(
            [self._make_user_callback(suc_cb, err_cb)])
        with self._consume_buffer_mutex:
            self._consume_buffer_not_empty_cond.notify()

    def wait(self, timeout=None):
        assert self._magic_number == 0x87654321
        self._wait_for_callbacks_finished(timeout)

    def _wait_for_callbacks_finished(self, timeout=None):
        assert self._magic_number == 0x87654321
        with self._consume_buffer_mutex:
            self._consume_finished_cond.wait(timeout)

    def close(self):
        assert self._magic_number == 0x87654321
        self._stop_consume_thread()
        self._stop_recv_thread()
        self._magic_number = 0

    def subscribe(self, topics):
        assert self._magic_number == 0x87654321
        assert isinstance(topics, list)
        self._consumer.subscribe(topics)

    def unsubscribe(self, timeout=None):
        assert self._magic_number == 0x87654321

        self._wait_for_callbacks_finished(timeout)
        self._consumer.unsubscribe()
        with self._msg_cb_lock:
            self._msgs.clear()
            self._cbs.clear()

        with self._recv_buffer_mutex:
            self._buffers_to_change_recv.clear()
            if self._recv_cur_buffer is not None:
                self._recv_cur_buffer.clear()
            if self._recv_next_buffer is not None:
                self._recv_next_buffer.clear()

        with self._consume_buffer_mutex:
            self._buffers_to_change_consume.clear()
            assert self._consume_cur_buffer is not None
            self._consume_cur_buffer.clear()
            if self._consume_next_buffer is not None:
                self._consume_next_buffer.clear()

    def _start_recv_thread(self):
        self._recv_running = True
        self._recv_thread.spawn(self._recv_task)
        self._recv_started.wait()

    def _stop_recv_thread(self):
        self._recv_running = False
        with self._recv_buffer_mutex:
            self._recv_buffer_empty_cond.notify()
        self._recv_thread.join()

    def _start_consume_thread(self):
        self._consume_running = True
        self._consume_thread.spawn(self._consume_task)
        self._consume_started.wait()

    def _stop_consume_thread(self):
        self._consume_running = False
        # 唤醒可能正在阻塞的消费数据线程
        with self._recv_buffer_mutex:
            if self._recv_cur_buffer is not None:
                self._recv_cur_buffer.clear()
            if self._recv_next_buffer is not None:
                self._recv_next_buffer.clear()
            self._recv_buffer_not_empty_cond.notify()

        with self._consume_buffer_mutex:
            assert self._consume_cur_buffer is not None
            self._consume_cur_buffer.clear()
            if self._consume_next_buffer is not None:
                self._consume_next_buffer.clear()
            self._consume_buffer_not_empty_cond.notify()

        self._consume_thread.join()

    def _put_msgs_in_recv_buffer(self, raw_msgs):
        assert isinstance(raw_msgs, list)
        if not raw_msgs:
            return

        with self._recv_buffer_mutex:
            if self._recv_cur_buffer.writable_count() >= len(raw_msgs):
                self._recv_cur_buffer.append(raw_msgs)
            else:
                self._buffers_to_change_recv.append(
                    self._recv_cur_buffer)
                self._recv_cur_buffer = None
                if self._recv_next_buffer is not None:
                    self._recv_cur_buffer = self._recv_next_buffer
                    self._recv_next_buffer = None
                else:
                    self._recv_buffer_empty_cond.wait()

                if self._recv_running:
                    self._recv_cur_buffer.append(raw_msgs)

                self._recv_buffer_not_empty_cond.notify()

    def _put_callbacks_in_consume_buffer(self, raw_callbacks):
        assert raw_callbacks
        assert isinstance(raw_callbacks, list)

        with self._consume_buffer_mutex:
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

                self._consume_buffer_not_empty_cond.notify()

    def _recv_task(self):
        self._recv_started.set()
        while self._recv_running:
            kafka_msgs = self._recv_task_inner()
            self._put_msgs_in_recv_buffer(kafka_msgs)
        self._consumer.close()

    def _recv_task_inner(self):
        return self._consumer.consume(
            num_messages=Buffer.MAX_BUFFER_SIZE, timeout=0.3)

    def _consume_task(self):
        self._consume_started.set()

        recv_cur_buffer_r = Buffer()
        recv_next_buffer_r = Buffer()
        buffers_to_recv = []
        recv_buffer_empty = True

        consume_cur_buffer_r = Buffer()
        consume_next_buffer_r = Buffer()
        buffers_to_consume = []
        consume_buffer_empty = True

        while self._consume_running:
            if recv_buffer_empty:
                with self._recv_buffer_mutex:
                    if not self._buffers_to_change_recv:
                        self._recv_buffer_not_empty_cond.wait(timeout=0.5)

                    if self._recv_cur_buffer is not None:
                        self._buffers_to_change_recv.append(
                            self._recv_cur_buffer)
                    self._recv_cur_buffer = recv_cur_buffer_r
                    recv_cur_buffer_r = None
                    self._buffers_to_change_recv, buffers_to_recv \
                        = buffers_to_recv, self._buffers_to_change_recv
                    if self._recv_next_buffer is None:
                        self._recv_next_buffer = recv_next_buffer_r
                        recv_next_buffer_r = None

                    self._recv_buffer_empty_cond.notify()
                recv_buffer_empty = False

            if consume_buffer_empty:
                with self._consume_buffer_mutex:
                    if not self._buffers_to_change_consume:
                        self._consume_buffer_not_empty_cond.wait(timeout=0.5)
                        if not self._buffers_to_change_consume and \
                                not self._consume_cur_buffer.readable_count():
                            self._consume_finished_cond.notify()

                    self._buffers_to_change_consume.append(
                        self._consume_cur_buffer)
                    self._consume_cur_buffer = consume_cur_buffer_r
                    consume_cur_buffer_r = None
                    self._buffers_to_change_consume, buffers_to_consume \
                        = buffers_to_consume, self._buffers_to_change_consume
                    if self._consume_next_buffer is None:
                        self._consume_next_buffer \
                            = consume_next_buffer_r
                        consume_next_buffer_r = None

                consume_buffer_empty = False

            with self._msg_cb_lock:
                for buffer in buffers_to_consume:
                    self._cbs += buffer.retrieve_all()
                    buffer.clear()
                for buffer in buffers_to_recv:
                    self._msgs += buffer.retrieve_all()
                    buffer.clear()

                if self._cbs and self._msgs:
                    self._consume_task_inner(self._msgs, self._cbs)

                if not self._msgs:
                    buffers_to_recv, recv_cur_buffer_r, \
                        recv_next_buffer_r \
                        = self._refill_buffer(buffers_to_recv,
                                              recv_cur_buffer_r,
                                              recv_next_buffer_r)
                    recv_buffer_empty = True

                if not self._cbs:
                    buffers_to_consume, consume_cur_buffer_r, \
                        consume_next_buffer_r \
                        = self._refill_buffer(buffers_to_consume,
                                              consume_cur_buffer_r,
                                              consume_next_buffer_r)
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
    def _refill_buffer(buffers, buffer1, buffer2):
        buffers = buffers[:2]

        if buffer1 is None:
            buffer1 = buffers[len(buffers) - 1]
            buffers = buffers[:1]
            buffer1.clear()

        if buffer2 is None:
            buffer2 = buffers[len(buffers) - 1]
            buffer2.clear()

        buffers = []

        return buffers, buffer1, buffer2

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
