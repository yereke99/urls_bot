'''
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

if __name__ == "__main__":
    asyncio.run(main())

'''

'''
import asyncio, time

async def fib(n):
    global count
    count = count + 1
    time.sleep(0.1)
    event_loop = asyncio.get_event_loop()
    if n > 1:
        task1 = asyncio.create_task(fib(n - 1))
        task2 = asyncio.create_task(fib(n - 2))
        await asyncio.gather(task1, task2)
        res = task1.result()+task2.result()
        print(res)
        return res

    return n

global count
count = 0
if __name__ == "__main__":
    asyncio.run(fib(10))

'''