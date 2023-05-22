import sys


class DiophantineSystem:
    def __init__(self, file):
        with open(file, 'r') as f:
            rows = f.read().splitlines()
            matrix = []
            dimensions = rows[0].split()
            self.r = 0
            self.n = int(dimensions[0])
            self.m = int(dimensions[1])
            self.x = []
            for i in range(1, self.n + 1):
                if len(rows[i].split()) != self.m:
                    raise Exception("Incorrect matrix!")
                line = [int(x) for x in rows[i].split()]
                matrix.append(line)
        self.matrix = matrix
        self.form_A()
        self.form_C()
        self.divide_last()
        self.get_solutions()
        self.print_solutions()

    def print_solutions(self):
        n = self.n - self.m + 1
        s = len(self.x)
        for i in range(n):
            print(self.x[s - 1][i], end="\t")
            for j in range(0, s - 1):
                print(self.x[j][i], end="\t")
            print()
        print("x0", end="\t")
        for i in range(1, s):
            print(f"t{i}", end="\t")

    def get_solutions(self):
        for i in range(0, self.n - self.m + 1):
            if self.matrix[i][self.m - 1] != 0:
                return None
        for j in range(self.r, self.m):
            x = []
            for i in range(self.n - self.m + 1, self.n):
                x.append(self.matrix[i][j])
            self.x.append(x)
        return self.x

    def divide_last(self):
        for i in range(0, self.n - self.m + 1):
            if self.matrix[i][i] != 0:
                k = self.matrix[i][self.m - 1]//self.matrix[i][i]
                self.subtract(self.m - 1, i, k)
            else:
                self.r = i
                break
            self.r = i + 1


    def form_A(self):
        for i in range(self.n):
            self.matrix[i][self.m - 1] = -self.matrix[i][self.m - 1]
        for i in range(self.m - 1):
            line = [0 for j in range(self.m)]
            line[i] = 1
            self.matrix.append(line)
        self.n += self.m - 1

    def form_C(self):
        for i in range(self.n):
            while not self.is_zero(i):
                index = self.find_min(self.matrix[i], i)
                if self.matrix[i][index] == 0:
                    continue
                if self.matrix[i][index] < 0:
                    self.inverse(index)
                if index != i:
                    self.swap_column(i, index)
                self.divide(i)

    def is_zero(self, i):
        for j in range(i + 1, self.m - 1):
            if self.matrix[i][j] != 0:
                return False
        return True

    def divide(self, row):
        for i in range(row + 1, self.m - 1):
            d = self.matrix[row][i]//self.matrix[row][row]
            self.subtract(i, row, d)

    def subtract(self, i, j, d):
        for k in range(self.n):
            self.matrix[k][i] -= self.matrix[k][j] * d

    def inverse(self, i):
        for row in self.matrix:
            row[i] = -row[i]

    def swap_column(self, i, j):
        for k in range(self.n):
            temp = self.matrix[k][i]
            self.matrix[k][i] = self.matrix[k][j]
            self.matrix[k][j] = temp

    def find_min(self, row, k):
        abs_row = [abs(row[i]) for i in range(k, self.m - 1)]
        min_el = 0
        for x in abs_row:
            if x > 0:
                min_el = x
                break
        index = 0
        for i in range(0, len(abs_row)):
            if 0 < abs_row[i] < min_el:
                min_el = abs_row[i]
                index = i
        return index + k

    def print_m(self):
        for i in range(self.n):
            for j in range(self.m):
                print(self.matrix[i][j], end=" ")
            print()


def main():
    try:
        DiophantineSystem(sys.argv[1])
    except Exception as msg:
        print(msg)


if __name__ == '__main__':
    main()
