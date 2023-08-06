__all__ = ['Buffer']


class Buffer:
    MAX_BUFFER_SIZE = 10000

    def __init__(self):
        self._msgs = []
        self._writer_index = 0
        self._reader_index = 0

    def readable_count(self):
        return self._writer_index - self._reader_index

    def writable_count(self):
        return Buffer.MAX_BUFFER_SIZE - self._writer_index + self._reader_index

    def retrieve(self, count):
        assert count <= self.readable_count()
        former_reader_index = self._reader_index
        self._reader_index += count
        return self._msgs[former_reader_index:former_reader_index + count]

    def retrieve_one(self):
        assert self.readable_count() >= 1
        msg = self._msgs[self._reader_index]
        self._reader_index += 1
        return msg

    def retrieve_all(self):
        self._reader_index = 0
        self._writer_index = 0
        return self._msgs

    def append(self, msgs):
        assert len(msgs) <= self.writable_count()
        if Buffer.MAX_BUFFER_SIZE - self._writer_index >= len(msgs):
            self._append_on_tail(msgs)
        else:
            self._append_with_movement(msgs)

    def append_one(self, msg):
        self.append([msg])

    def _append_on_tail(self, msgs):
        assert Buffer.MAX_BUFFER_SIZE - self._writer_index >= len(msgs)
        for msg in msgs:
            self._msgs.append(msg)
        self._writer_index += len(msgs)

    def _append_with_movement(self, msgs):
        assert Buffer.MAX_BUFFER_SIZE - self._writer_index < len(msgs)
        self._msgs = self._msgs[self._reader_index:self._writer_index]
        for msg in msgs:
            self._msgs.append(msg)
        self._reader_index = 0
        self._writer_index = self._writer_index - \
            self._reader_index + len(msgs)

    def clear(self):
        self._msgs.clear()
        self._reader_index = 0
        self._writer_index = 0
