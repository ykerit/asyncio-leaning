
# def start_yield():
#     print('start')
#     while True:
#         print('asdasd')
#         yield

# g = start_yield()
# next(g)
# next(g)

def reader():
    for i in range(4):
        yield '<<< %s' % i

def reader_wrapper(coro):
    for i in coro:
        yield i

def writter():
    while True:
        w = yield
        print('>>>', w)

def writter_wrapper(coro):
    yield from coro

# w = writter()
# wrap = writter_wrapper(w)
# wrap.send(None)
# for i in range(4):
#     wrap.send(i)

# wrap = reader_wrapper(reader())
# for i in wrap:
#     print(i)

# gen1 -> gen2 -> gen3 -> gen1

from collections import deque

tasks = deque([])

def generator_1():
    print('generator_1')
    yield
    tasks.append(generator_2())


def generator_2():
    print('generator_2')
    yield
    tasks.append(generator_3())

def generator_3():
    print('generator_3')
    yield
    tasks.append(generator_1())

tasks.append(generator_1())
while tasks:
    task = tasks.popleft()
    try:
        next(task)
    except StopIteration:
        continue
    tasks.append(task)
    