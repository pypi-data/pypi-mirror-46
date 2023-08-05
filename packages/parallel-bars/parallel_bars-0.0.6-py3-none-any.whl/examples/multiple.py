import main


def fun(x):
    return sum(i ** 10000 for i in range(x))


items = list(range(100, 1000))

if __name__ == '__main__':
    main.compute_with_multiple_bars(fun, items, num_processes=4)
