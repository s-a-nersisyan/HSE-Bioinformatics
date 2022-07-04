import numpy as np
from multiprocessing import Pool


class Parallelizator:
    def __init__(self, func, args_list, n_processes, multiple_args=False):
        self.func = func
        self.multiple_args = multiple_args
        self.n_processes = n_processes
        self.args_chunks = list(np.array_split(args_list, n_processes))
        self.set_process_chunk()
        
    def set_process_chunk(self):
        # !TODO: THIS IS VERY BAD
        global process_chunk
        def process_chunk(args_chunk):
            results = []
            for arg in args_chunk:
                print(arg)
                results.append(self.func(*arg) if self.multiple_args else self.func(arg))

            return results
        
        self.process_chunk = process_chunk

    def parallelize(self):            
        with Pool(self.n_processes) as p:
            if self.multiple_args:
                results = p.starmap(
                    self.process_chunk,
                    self.args_chunks,
                )
            else:
                results = p.map(
                    self.process_chunk,
                    self.args_chunks,
                )

        return results
