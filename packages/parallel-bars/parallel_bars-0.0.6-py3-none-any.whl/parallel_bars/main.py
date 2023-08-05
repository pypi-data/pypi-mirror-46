import multiprocessing
from typing import TypeVar, List, Callable

from tqdm import tqdm

DEFAULT_PROCESS_COUNT: int = 2
DEFAULT_BATCH_SIZE: int = 64

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


def batch_process(
        process_id: int,
        fun: Callable[[T], V],
        item_batch: List[T],
        queue: multiprocessing.Queue,
        with_bar: bool = False,
        batch_size: int = DEFAULT_BATCH_SIZE,
) -> None:
    if with_bar:
        collection = tqdm(item_batch, position=process_id)
    else:
        collection = item_batch

    batch = []
    current_batch_size = 0
    for item_id, item in collection:
        batch.append((item_id, fun(item)))
        current_batch_size += 1

        if current_batch_size == batch_size:
            queue.put(batch)

            batch = []
            current_batch_size = 0
            
    if batch:
        queue.put(batch)


def compute(
        fun: Callable[[T], V],
        items: List[T],
        num_processes: int = None,
        single_bar: bool = False,
        in_order: bool = False,
        batch_size: int = DEFAULT_BATCH_SIZE,

) -> List[V]:
    process_count: int = get_process_count(num_processes)

    processes = []
    manager = multiprocessing.Manager()
    queue = manager.Queue()

    enumerated_items = list(enumerate(items))
    for position in range(process_count):
        p = multiprocessing.Process(
            target=batch_process,
            args=(
                position,
                fun,
                enumerated_items[position::process_count],
                queue,
                not single_bar,
                batch_size,
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
            results += queue.get(block=False)
            if single_bar:
                pbar.update(batch_size)

    for process in processes:
        process.join()

    if in_order:
        results = sorted(results, key=lambda x: x[0])

    return list(list(zip(*results))[1])


def compute_with_single_bar(
        fun: Callable[[T], V],
        items: List[T],
        num_processes: int = None,
        in_order: bool = False,
        batch_size: int = DEFAULT_BATCH_SIZE,

) -> List[V]:
    return compute(
        fun=fun,
        items=items,
        num_processes=num_processes,
        single_bar=True,
        in_order=in_order,
        batch_size=batch_size,
    )


def compute_with_multiple_bars(
        fun: Callable[[T], V],
        items: List[T],
        num_processes: int = None,
        in_order: bool = False,
        batch_size: int = DEFAULT_BATCH_SIZE,
) -> List[V]:
    return compute(
        fun=fun,
        items=items,
        num_processes=num_processes,
        single_bar=False,
        in_order=in_order,
        batch_size=batch_size,
    )
