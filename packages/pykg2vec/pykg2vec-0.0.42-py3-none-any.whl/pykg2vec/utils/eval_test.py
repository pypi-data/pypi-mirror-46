import timeit
import numpy as np
from processing import Pool

arr = list(np.random.permutation(range(1000000)))

for j in range(10):
    val = arr[0]
    np.random.shuffle(arr)
    start_time = timeit.default_timer()
    for i in range(len(arr)):
        if arr[i] == val:
            print("found it!")
    print('Time:[%.4f sec]' % (timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    for i in range(len(arr)):
        if arr[i] == val:
            print("found it!")
    print('bisect: -->Time:[%.4f sec]' % (timeit.default_timer() - start_time))


def eval_batch_head(id_replace_head, tr_h, e1, e2, r_rev):
    hrank = 0
    fhrank = 0

    for j in range(len(id_replace_head)):
        val = id_replace_head[-j - 1]
        if val == e1:
            break
        else:
            hrank += 1
            fhrank += 1
            if val in tr_h[(e2, r_rev)]:
                fhrank -= 1

    return hrank, fhrank


def eval_batch_tail(id_replace_tail, hr_t, e1, r, e2):
    trank = 0
    ftrank = 0

    for j in range(len(id_replace_tail)):
        val = id_replace_tail[-j - 1]
        if val == e2:
            break
        else:
            trank += 1
            ftrank += 1
            if val in hr_t[(e1, r)]:
                ftrank -= 1
    return trank, ftrank


