class Tensor:
    def __init__(self, dimension, data):
        self.dimension = dimension
        self.data = data

    def __str__(self):
        return " ".join([str(i) for i in self.data])


class Matrix(Tensor):
    def __init__(self, rows, columns, data):
        dimension = tuple([rows, columns])
        super().__init__(dimension, data)
        self.rows = rows
        self.columns = columns

    def conv_rc2i(self, row, column):
        return row * self.columns + column

    def conv_i2rc(self, i):
        return [i // self.columns, i % self.columns]

    def __str__(self):
        max_len = max(len(str(i)) for i in self.data)
        string = "["
        for i in range(self.rows):
            string += "\n"
            for j in range(self.columns):
                string += "  " + f"{self.data[self.conv_rc2i(i, j)]:{max_len}}"
            string += "\n"
        string += "]"
        return string

    @staticmethod
    def increase_up_to_size(number, size):
        if number < 0:
            multiplier = abs(number) // size + 1
            number += size * multiplier

        return number

    def get_row(self, row):
        data = [self.data[i] for i in range(row * self.columns, (row + 1) * self.columns)]
        return Matrix(1, self.columns, data)

    def get_rows(self, rows):
        data = []
        for i in rows:
            data.extend(self.get_row(self.increase_up_to_size(i, self.rows)).data)
        return Matrix(len(rows), self.columns, data)

    def transpond(self):
        data = [0 for _ in range(len(self.data))]
        m = Matrix(self.columns, self.rows, [])
        for i in range(len(self.data)):
            [r, c] = self.conv_i2rc(i)
            data[m.conv_rc2i(c, r)] = self.data[i]
        return Matrix(self.columns, self.rows, data)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.get_row(self.increase_up_to_size(item, self.rows))
        if isinstance(item, list):
            return self.get_rows(item)
        if isinstance(item, slice):
            step = item.step if item.step is not None else 1
            if step > 0:
                start = self.increase_up_to_size(item.start if item.start is not None else 0, self.rows)
                stop = self.increase_up_to_size(item.stop if item.stop is not None else self.rows, self.rows)
                rows = [i for i in range(start, stop, step)]
            else:
                start = self.increase_up_to_size(item.start if item.start is not None else self.rows - 1, self.rows)
                stop = self.increase_up_to_size(item.stop, self.rows) if item.stop is not None else -1
                rows = [i for i in range(start, stop, step)]
            return self.get_rows(rows)
        if isinstance(item, tuple):
            [rows, columns] = item
            if isinstance(rows, int) and isinstance(columns, int):
                return self.data[self.conv_rc2i(rows, columns)]
            rowed_matrix = self.__getitem__(rows)
            transponed = rowed_matrix.transpond()
            ans = transponed[columns]
            return ans.transpond()


def main():
    data = [i for i in range(100)]
    data[12] = 473
    m = Matrix(10, 10, data)
    print(m[[1, 4], [1, 4]])
    # t = Tensor(100, data)
    # print(t)


if __name__ == "__main__":
    main()
