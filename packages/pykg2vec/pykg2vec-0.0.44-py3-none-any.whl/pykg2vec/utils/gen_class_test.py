from threading import Thread, currentThread
from multiprocessing import Process, Queue, JoinableQueue, current_process
import numpy as np


class Gen:
    def __init__(self):
        self.q1 = Queue(maxsize=5)
        self.q2 = Queue(maxsize=5)
        self.process_list = []
        self.thread = None

    def gen_id(self, ids):
        i = 0
        while True:
            yield ids[i]
            i += 1
            if i >= len(ids):
                np.random.shuffle(ids)
                i = 0

    def func3(self, ids, q1: Queue):
        process = current_process()
        gen = iter(self.gen_id(ids))
        while True:
            val = next(gen)
            # print("thread:", process.name, " q1size:", q1.qsize(), "ids:", val)
            q1.put(val)
            print("put in raw:: process:", process.name, "puts in raw queue:", val)

    def func2(self, ids):
        thread = currentThread()
        gen = iter(self.gen_id(ids))
        while getattr(thread, "run", True):
            val = next(gen)
            # print("thread:", thread.name, " q1size:", self.q1.qsize(), "ids:", val)
            self.q1.put(val)

    def func(self, q1: JoinableQueue, q2: Queue):
        process = current_process()
        while True:
            d = q1.get()
            # print(d * d)
            q2.put(d)
            print("pool process:", process.name, "gets from raw queue:", d, "puts in  process queue:", d)

    def pool_process(self, q1, q2):
        for i in range(2):
            p = Process(target=self.func, args=(q1, q2))
            # p = Process(target=self.process_function_train_proje, args=(bs, n_entity, neg_weight,))
            p.daemon =True
            p.start()
            self.process_list.append(p)


    def __iter__(self):
        # val = next(self.gen())
        return self.gen()

    def gen(self):
        ids = np.random.permutation(20)
        # worker = Thread(target=self.func2, args=(ids,))
        # self.thread = worker
        # worker.start()
        worker=Process(target=self.func3, args=(ids, self.q1))
        worker.daemon = True
        worker.start()
        self.pool_process(self.q1, self.q2)

        while True:
            val = self.q2.get()
            # print("gen:", val, " q2size:", self.q2.qsize())
            yield val


def main():
    g = iter(Gen())
    for i in range(20):
        next(g)
        # print("------------------------->b_id:", i, "batch_process:", next(g))
    print("Finished task!")
    # g.thread.run = False
    # for p in g.process_list:
    #     p.terminate()


if __name__ == '__main__':
    main()
