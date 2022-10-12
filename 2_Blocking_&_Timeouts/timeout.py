import asyncio

async def asleeper(seconds, i=-1):
    if i != -1:
        print(f"a{i}\t{seconds}s")
    await asyncio.sleep(seconds)


async def wait():
    done, pending = await asyncio.wait([asleeper(1), asleeper(123)], timeout=2)
    print(done, pending)

async def wait_for():
    try:
        await asyncio.wait_for(asleeper(5), timeout=3)
    except asyncio.TimeoutError:
        print("Task failed")

async def asleeper_timeout(seconds, i=-1, timeout=4):
    if i != -1:
        print(f"a{i}\t{seconds}s")
    await asyncio.wait_for(asyncio.sleep(seconds), timeout=timeout)
    
# await asleeper_timeout(12, timeout=1)

if __name__ == "__main__":
    #asyncio.run(wait())

    asyncio.run(wait_for())

    #asyncio.run(asleeper_timeout(12, timeout=1))
