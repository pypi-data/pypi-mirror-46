from logging import handlers


class PipeHandler(handlers.QueueHandler):

    def __init__(self, pipe):
        super().__init__(pipe)

    def enqueue(self, record):
        return self.queue.send(record)


class PipeListener(handlers.QueueListener):

    # def __init__(self, pipe, *handlers, respect_handler_level=False):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dequeue(self, _):
        return self.queue.recv()
