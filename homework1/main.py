from matrix import Matrix


def main():
    data = [i for i in range(100)]
    data[12] = 473
    m = Matrix(tuple([10, 10]), data)
    print(m[[1, 4], [1, 4]])


if __name__ == "__main__":
    main()
