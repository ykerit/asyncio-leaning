import asyncio
import signal

async def shutdown(signal, loop):
    print('receive signal', signal.name)
    print('cleanup resource')
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print('shutdown complete')

async def coro_a():
    await asyncio.sleep(0.5)

async def coro_b():
    await asyncio.sleep(0.5)

def main():
    loop = asyncio.get_event_loop()
    signals = (signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))
    try:
        loop.create_task(coro_a())
        loop.create_task(coro_b())
        loop.run_forever()
    finally:
        print('cleaning up')
        loop.close()

if __name__ == '__main__':
    main()