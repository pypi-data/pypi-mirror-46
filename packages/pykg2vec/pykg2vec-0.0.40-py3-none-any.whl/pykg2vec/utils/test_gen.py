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

    def func3(self, ids):
        process = current_process()
        print(process.name, id(self.q1))
        print(process.name, id(self.q2))
        gen = iter(self.gen_id(ids))
        while True:
            val = next(gen)
            # print("thread:", process.name, " q1size:", q1.qsize(), "ids:", val)
            self.q1.put(val)
            l = []

            for i in range(self.q1.qsize()):
                l.append(self.q1.get())
            if l:
                print("q1 pool process:", process.name)
                print(l)
            for i in l:
                self.q1.put(i)
            # print("put in raw:: process:", process.name, "puts in raw queue:", val,"id of val", id(val))

    def func2(self, ids):
        thread = currentThread()
        gen = iter(self.gen_id(ids))
        while getattr(thread, "run", True):
            val = next(gen)
            print("thread:", thread.name, " q1size:", self.q1.qsize(), "id of val", id(val))
            self.q1.put(val)

    def func(self):
        process = current_process()
        print(process.name,id(self.q1))
        print(process.name, id(self.q2))

        while True:
            l=[]

            for i in range(self.q1.qsize()):
                l.append(self.q1.get())
            if l:
                print("q1 pool process:", process.name)
                print(l)
            for i in l:
               self.q1.put(i)
            d = self.q1.get()
            # print(d * d)
            self.q2.put(d)
            l=[]

            for i in range(self.q2.qsize()):
                l.append(self.q2.get())
            if l:
                print("q2 pool process:", process.name)
                print(l)
            for i in l:
               self.q2.put(i)
            # print("pool process:", process.name, "gets from raw queue:", d, "puts in  process queue:", d,"id of val", id(d))

    def pool_process(self):
        for i in range(2):
            p = Process(target=self.func, args=())
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
        worker=Process(target=self.func3, args=(ids,))
        worker.daemon = True
        worker.start()
        self.pool_process()

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
