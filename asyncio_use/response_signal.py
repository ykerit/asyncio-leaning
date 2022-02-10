import asyncio

async def coro_a():
    await asyncio.sleep(0.5)

async def coro_b():
    await asyncio.sleep(0.5)

def main():
    loop = asyncio.get_event_loop()
    
    try:
        loop.create_task(coro_a())
        loop.create_task(coro_b())
        loop.run_forever()
    except KeyboardInterrupt:
        print('process interrput')
    finally:
        print('cleaning up')
        loop.close()

if __name__ == '__main__':
    main()
