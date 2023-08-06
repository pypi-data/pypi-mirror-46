from .RainbowSim import _RainbowSim
import numpy as np

"""
Rainbow Equation of the form:

a_1*x_1 + a_2*x_2 + ... + a_i*x_i = b

where x is an element of 2D cartesian products.
"""


class RbCartesianSumsEq(_RainbowSim):
    def __init__(self, m, n, a, b=(0, 0), mod=False):
        if type(m) is not int or m < 1:
            raise TypeError("Scalar m can only be an integer greater than or equal to 1")
        self.M = m  # rows

        if type(n) is not int or n < 1:
            raise TypeError("Scalar n can only be an integer greater than or equal to 1")
        self.N = n  # columns

        for i in a:
            if type(i) is not int:
                raise TypeError("Vector a[] can only contain integers")
        self.a = a  # coefficients

        for i in b:
            if type(i) is not int:
                raise TypeError("Vector b[] can only contain integers")
        self.b = Point(b[0], b[1])

        if type(mod) is not bool:
            raise TypeError("Boolean mod must be either", True, "for Zn or", False, "for [n].")
        self.mod = mod

        super(RbCartesianSumsEq, self).__init__(m * n, len(a), RbCartesianSumsEq, (m, n, a, b))

    def _invert(self, i):
        """
        Invert object from index.

        :param i: Index to be inverted
        :return: Object from index
        """
        x = (i) // self.N + 1
        y = 1 + (i % self.N)
        return Point(x, y)

    def _is_valid_set(self, set):
        """
        Determine whether or not a given set is valid (satisfies equation).

        :param set: Set to be tested
        :return: Boolean for whether or not set is valid
        """
        sum = Point(0, 0)
        for a, point in zip(self.a, set):
            temp = sum
            sum += a * point
        if self.mod:
            return sum % [self.M, self.N] == self.b or sum == self.b
        return sum == self.b

    def equation(self):
        """
        Get a string-representation of the current equation.

        :return:
        string: Algebraic form of equation with a-coefficients and b-value
        """
        eq = ""
        for i in self.a:
            eq += str(i) + "x + "
        eq = eq[:-2] + "= " + str(self.b) + ", M = " + str(self.M) + ", N = " + str(self.N) + ", mod =" + str(self.mod)
        return eq

    def print_extreme_matrices(self, quantity=-1):
        """
        Print, in matrix form, to console the extreme colorings.

        :param quantity: Quantity of colorings to be printed (default = -1 to print all)
        :return: None
        """
        if self.start != -1:
            temp = self.colorings.head
            i = 0
            while temp is not None and (i < quantity or quantity < 0):
                matrix = [temp.data[i * self.N:(i + 1) * self.N] for i in
                          range((len(temp.data) + self.N - 1) // self.N)]
                print(np.matrix(matrix), "\n")
                temp = temp.next
                i += 1
        print()

    def print_set_matrices(self, nums=-1):
        """
        Print, in matrix form, to console the sets generated.

        :param nums: List of numbers whose sets will be printed (default = -1 to print all)
        :return: None
        """
        # TODO UPDATE FUNCTIONALITY
        sum = self.sets[self.n].head.next
        i = 0
        while sum is not None:
            matrix = [["*" for _ in range(self.N)] for _ in range(self.M)]
            for i in sum.data:
                p = self._invert(i)
                matrix[p.x - 1][p.y - 1] = "0"
            print(np.matrix(matrix), "\n")
            sum = sum.next
            i += 1
        return

    def print_sets(self, nums=-1):
        """
        Print to console the sets generated.

        :param nums: List of numbers whose sets will be printed (default = -1 to print all)
        :return: None
        """
        # TODO see if you can simplify this method
        print('Sets Generated:', end='')
        if nums is -1 and self.mod:
            nums = list(range(self.n))
        elif nums is -1 and not self.mod:
            nums = list(range(1, self.n + 1))
        for n in nums:
            if self.mod:
                temp = self.sets[n].head.next
            else:
                temp = self.sets[n - 1].head.next
            if self.mod:
                print('\n', n, ':', temp, end='')
            else:
                if temp is not None:
                    print('\n', n, ':',
                          '[%s]' % ', '.join(map(str, [self._invert(i) for i in temp.data])), end='')
                else:
                    print('\n', n, ':', temp, end='')
            if temp is not None:
                temp = temp.next
                while temp is not None:
                    if self.mod:
                        print(',', temp, end='')
                    else:
                        print(',', '[%s]' % ', '.join(map(str, [self._invert(i) for i in temp.data])),
                              end='')
                    temp = temp.next
        print("\n")


class Point:
    def __init__(self, x, y):
        if int(x) != x:
            raise TypeError("Points cannot have parameter of type double: x")
        if int(y) != y:
            raise TypeError("Points cannot have parameter of type double: y")
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        raise IndexError("Point object can only have two indices, 0 and 1 (x and y).")

    def __mod__(self, other):
        return Point(self.x % other[0], self.y % other[1])

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]