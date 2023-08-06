from threading import Thread, currentThread
from multiprocessing import Process, Queue, JoinableQueue, current_process
import numpy as np

q1 = Queue(maxsize=5)
q2 = Queue(maxsize=5)


def gen_id(ids):
    i = 0
    while True:
        yield ids[i]
        i += 1
        if i >= len(ids):
            np.random.shuffle(ids)
            i = 0


def func2(ids):
    thread = currentThread()
    gen = iter(gen_id(ids))
    while getattr(thread, "run", True):
        val = next(gen)
        print("thread:", thread.name, " q1size:", q1.qsize(), "ids:", val)
        q1.put(val)


def func(q1: JoinableQueue, q2: Queue):
    process = current_process()
    while True:
        d = q1.get()
        # print(d * d)
        q2.put(d * d)
        print("process:", process.name, "ids:", d, " q1size:", q1.qsize(), " q2size:", q2.qsize())


process_list = []


def pool_process():
    for i in range(2):
        p = Process(target=func, args=(q1, q2))
        # p = Process(target=self.process_function_train_proje, args=(bs, n_entity, neg_weight,))
        p.start()
        process_list.append(p)

thread = None

def gen():
    ids = np.random.permutation(10)
    worker = Thread(target=func2, args=(ids,))
    global thread
    thread = worker
    worker.start()
    pool_process()

    while True:
        val = q2.get()
        print("gen:", val, " q2size:", q2.qsize())
        yield val


def main():
    g = gen()
    for i in range(100):
        print("------------------------->b_id:",i,"batch_process:",next(g))
    print("Finished task!")
    thread.run=False
    for p in process_list:
        p.terminate()


if __name__ == '__main__':
    main()
