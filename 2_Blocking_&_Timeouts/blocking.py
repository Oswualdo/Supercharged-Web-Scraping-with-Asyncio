import time
import asyncio


def sleeper(seconds, i=-1):
    if i != -1:
        print(f"{i}\t{seconds}s")
    time.sleep(seconds)


async def asleeper(seconds, i=-1):
    if i != -1:
        print(f"a{i}\t{seconds}s")
    await asyncio.sleep(seconds)


if __name__ == "__main__":
    ## Select the mode to run this code

    ## execute the code in sync mode
    # sleeper(12)

    ## execute the code in async mode
    #asyncio.run(asleeper(12))

    loop = asyncio.get_event_loop()
    loop.create_task(asleeper(123))