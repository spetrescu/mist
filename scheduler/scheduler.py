from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Any

class Scheduler:
    def __init__(self, max_workers: int = 10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.queue_counter = 0

    def schedule_tasks(self, tasks: List[Callable[..., Any]]) -> List[Any]:
        futures = [self.executor.submit(task) for task in tasks]
        self.queue_counter += len(futures)
        # print(self.queue_counter)
        results = []
        for future in as_completed(futures):
            results.append(future.result())
            self.queue_counter -= 1
        return results

    def get_queue_counter(self) -> int:
        return self.queue_counter
