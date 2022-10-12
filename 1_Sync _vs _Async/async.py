import time
import asyncio

start = time.time()
iteration_times = [1, 3, 2, 1]


async def a_sleeper(seconds, i=-1):
    if i != -1:
        print(f"iteration: {i}\ttime: {seconds}s")
    await asyncio.sleep(seconds)  # coroutine

    ellap = time.time() - start
    print(f"{i} done {ellap}")
    return "abc"


async def a_run():
    results = []
    for i, second in enumerate(iteration_times):
        results.append(
            asyncio.create_task(a_sleeper(second, i=i))
        )
    return results


async def main():
    results = await a_run()
    print(results)
    end = time.time() - start

    print(end)

if __name__ == "__main__":
    asyncio.run(main())
