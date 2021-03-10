from concurrent.futures import as_completed
import multiprocessing
from concurrent.futures.process import ProcessPoolExecutor


class ThisIsThreadThing:

    def __init__(self):
        self.executor = ProcessPoolExecutor(max_workers=(multiprocessing.cpu_count() - 1))

    def submit(self, function, parameters):
        self.executor.submit(function, parameters)
