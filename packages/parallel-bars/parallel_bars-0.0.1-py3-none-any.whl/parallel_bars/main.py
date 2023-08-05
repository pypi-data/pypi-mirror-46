import multiprocessing
from multiprocessing.queues import Queue
from typing import TypeVar, List, Callable

from tqdm import tqdm

DEFAULT_PROCESS_COUNT: int = 2

T = TypeVar('T')
V = TypeVar('V')


def get_process_count(num_processes: int = None) -> int:
    if num_processes is not None:
        if num_processes >= 1:
            return num_processes
        raise ValueError("The num_processes should be >= 1")
    try:
        return multiprocessing.cpu_count()
    except NotImplementedError:
        return DEFAULT_PROCESS_COUNT


# TODO pass process id to the function
# TODO make results optionally ordered?

def compute_with_single_bar(
        fun: Callable[[T], V],
        items: List[T],
        num_processes: int = None,
) -> List[V]:
    pool = multiprocessing.Pool(processes=get_process_count(num_processes))

    return list(
        tqdm(
            pool.map(fun, items),
            total=len(items),
        )
    )


def batch_process(
        process_id: int,
        fun: Callable[[T], V],
        item_batch: List[T],
        queue: multiprocessing.Queue
) -> None:
    results = [
        fun(item) for item in tqdm(item_batch, position=process_id)
    ]
    queue.put(results)


def compute_with_multiple_bars(
        fun: Callable[[T], V],
        items: List[T],
        num_processes: int = None,
        ordered: bool = False,
) -> List[V]:
    process_count: int = get_process_count(num_processes)

    processes = []
    queue: Queue[List[T]] = multiprocessing.Queue()

    for position in range(process_count):
        p = multiprocessing.Process(
            target=batch_process,
            args=(
                position,
                fun,
                items[position::process_count],
                queue,
            ),
        )
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    results: List[V] = []
    while not queue.empty():
        results += queue.get()

    return results
