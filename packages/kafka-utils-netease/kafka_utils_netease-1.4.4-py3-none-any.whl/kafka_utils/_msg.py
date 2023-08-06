__all__ = ['Msg']


class Msg:
    def __init__(self, topics, payload, success_callback, err_callback):
        self.payload = payload
        self.topics = topics
        self.success_callback = success_callback
        self.err_callback = err_callback
