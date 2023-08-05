import queue


def qput(q,v):
    if q.full():
        q.get()
    q.put(v)
