import multiprocessing
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


def compute_with_single_bar(
        fun: Callable[[T], V],
        items: List[T],
        num_processes: int = None,
) -> List[V]:
    return compute(
        fun=fun,
        items=items,
        num_processes=num_processes,
        single_bar=True,
    )


def batch_process(
        process_id: int,
        fun: Callable[[T], V],
        item_batch: List[T],
        queue: multiprocessing.Queue,
        with_bar: bool = False,
) -> None:
    if with_bar:
        collection = tqdm(item_batch, position=process_id)
    else:
        collection = item_batch

    for item in collection:
        queue.put(fun(item))


def compute_with_multiple_bars(
        fun: Callable[[T], V],
        items: List[T],
        num_processes: int = None,
) -> List[V]:
    return compute(
        fun=fun,
        items=items,
        num_processes=num_processes,
        single_bar=False,
    )


def compute(
        fun: Callable[[T], V],
        items: List[T],
        num_processes: int = None,
        single_bar: bool = False,
) -> List[V]:
    process_count: int = get_process_count(num_processes)

    processes = []
    manager = multiprocessing.Manager()
    queue = manager.Queue()

    for position in range(process_count):
        p = multiprocessing.Process(
            target=batch_process,
            args=(
                position,
                fun,
                items[position::process_count],
                queue,
                not single_bar,
            ),
        )
        p.start()
        processes.append(p)

    if single_bar:
        pbar = tqdm(total=len(items))
        pbar.update(0)

    results: List[V] = []
    while any(x.is_alive() for x in processes):
        while not queue.empty():
            results.append(queue.get(block=False))
            if single_bar:
                pbar.update(1)

    for process in processes:
        process.join()

    return results
