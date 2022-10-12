import time

iteration_times = [1, 3, 2, 4]


def sleeper(seconds, i=-1):
    if i != -1:
        print(f"iteration: {i}\ttime: {seconds}s")
    time.sleep(seconds)


def run():
    for i, second in enumerate(iteration_times):
        sleeper(second, i=i)


if __name__ == "__main__":
    run()
