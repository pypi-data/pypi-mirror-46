from timeit import timeit


def test():
    data = [i for i in range(10000)]
    if len(data):
        data.pop()


def test2():
    data = [i for i in range(10000)]
    if len(data):
        data.pop(0)


if __name__ == '__main__':
    print(timeit("test()", setup="from __main__ import test", number=1000))
    print(timeit("test2()", setup="from __main__ import test2", number=1000))
