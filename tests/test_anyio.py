from anyio import sleep, create_task_group, run
import random


async def sometask(num: int) -> None:
    print("Task", num, "running")
    await sleep(random.uniform(8, 20))
    print("Task", num, "finished")


async def main() -> None:
    async with create_task_group() as tg:
        for num in range(20):
            tg.start_soon(sometask, num)

    print("All tasks finished!")


run(main)
