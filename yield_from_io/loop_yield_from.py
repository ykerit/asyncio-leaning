from collections import deque
import selectors

class EventLoopYieldFrom:

    def __init__(self):
        self.tasks_ = deque([])
        self.selt_ = selectors.DefaultSelector()

    def create_task(self, coro):
        self.tasks_.append(coro)

    def sock_recv(self, sock, n):
        yield 'READ_NOW', sock
        return sock.recv(n)
    
    def sock_sendall(self, sock, data):
        yield 'WRITE_NOW', sock
        sock.sendall(data)
    
    def sock_accept(self, sock):
        yield 'READ_NOW', sock
        return sock.accept()

    def run(self):
        while True:
            if self.tasks_:
                task = self.tasks_.popleft()
                try:
                    event, arg = next(task)
                except StopIteration:
                    continue
                if event == 'READ_NOW':
                    self.selt_.register(arg, selectors.EVENT_READ, task)
                elif event == 'WRITE_NOW':
                    self.selt_.register(arg, selectors.EVENT_WRITE, task)
                else:
                    raise ValueError('unknown event', event)
            else:
                for key, _ in self.selt_.select():
                    task = key.data
                    sock = key.fileobj
                    self.selt_.unregister(sock)
                    self.create_task(task)

