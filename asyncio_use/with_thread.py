import asyncio
import logging
import aiohttp
import functools
import multiprocessing
from queue import Queue
from random import random
import time
from concurrent.futures import ThreadPoolExecutor
from unittest import async_case

async def restart_host(msg):
    # simulation of i/o work
    await asyncio.sleep(0.5)
    logging.info('restart msg %s', msg)
    raise Exception()

async def save(msg):
    # simulation of i/o work
    await asyncio.sleep(1)
    logging.info('save to database %s', msg)

async def handle_message(msg):
    resa, resb = await asyncio.gather(
        restart_host(msg), save(msg), return_exceptions=True)
    if isinstance(resa, Exception):
        logging.error('caught exception')


def handle_message_sync(loop, msg):
    logging.info('pulled %s', msg)
    # loop.create_task(handle_message(msg))
    # loop.run_until_complete(handle_message(msg))
    asyncio.run_coroutine_threadsafe(handle_message(msg), loop)

def thread_consume(loop):
    time.sleep(1)
    print('hello')

async def run():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, 
            thread_consume, loop)
    

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
# asyncio.run(handle_message('hello'))
# asyncio.run(run())

async def sleep_test():
    loop = asyncio.get_event_loop()
    print('going to sleep')
    await loop.run_in_executor(None, time.sleep, 5)
    print('waking up')

async def parallel():
    await asyncio.gather(sleep_test(), sleep_test())

s = time.perf_counter()
asyncio.run(parallel())
elapsed = time.perf_counter() - s
print(f"{__file__} executed in {elapsed:0.2f} seconds.")

# async def count():
#     print("One")
#     await asyncio.sleep(1)
#     print("Two")

# async def main():
#     await asyncio.gather(
#         count(), count(), count()
#         )

# if __name__ == "__main__":
#     import time
#     s = time.perf_counter()
#     asyncio.run(main())
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in \
#         {elapsed:0.2f} seconds.")

# def count():
#     print("One")
#     time.sleep(1)
#     print("Two")

# def main():
#     for _ in range(3):
#         count()

# if __name__ == "__main__":
#     s = time.perf_counter()
#     main()
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in \
#         {elapsed:0.2f} seconds.")

# def exception_handler(loop, context):
#     logging.error(f'caught exception: exception')

# async def io_exception():
#     await asyncio.sleep(1)
#     raise Exception('sdsd')

# def main():
#     loop = asyncio.get_event_loop()
#     loop.set_exception_handler(exception_handler)
#     loop.create_task(io_exception())
#     try:
#         loop.run_forever()
#     finally:
#         loop.close()

# main()

# async def run_loop(tx, rx):
#     limit = 10
#     pending = set()
#     while True:
#         while len(pending) < limit:
#             task = tx.get_nowait()
#             fn, args, kwargs = task
#             pending.add(fn(*args, **kwargs))
#         done, pending = await asyncio.wait(pending, ...)
#         for future in done:
#             rx.put_nowait(await future)

# def bootstrap(tx, rx):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(run_loop(tx, rx))

# async def fetch_url(url):
#     return await aiohttp.request('GET', url)

# def main():
#     tx, rx = Queue(), Queue()
#     p = multiprocessing.Process(
#         target=bootstrap,
#         args=(tx, rx)
#     ).start()

#     urls = []

#     for url in urls:
#         task = fetch_url, (url, ), {}
#         tx.put_nowait(task)