from collections import deque

class EventLoopNoIO:
    
    def __init__(self) -> None:
        self.tasks_ = deque([])

    def create_task(self, coro):
        self.tasks_.append(coro)

    def run(self):
        while self.tasks_:
            task = self.tasks_.popleft()
            try:
                next(task)
            except StopIteration:
                continue
            self.create_task(task)