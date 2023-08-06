from .RainbowSim import _RainbowSim

"""
Rainbow Equation of the form:

a_1*x_1 * a_2*x_2 * ... * a_i*x_i = b

where x is an element of the positive integers.
"""


class RbProductsEq(_RainbowSim):
    def __init__(self, n, a, b=0, mod=False):
        for i in a:
            if type(i) is not int:
                raise TypeError("Vector a[] can only contain integers")
        self.a = a

        if type(b) is not int:
            raise TypeError("Scalar b can only be an integer.")
        self.b = b

        if type(mod) is not bool:
            raise TypeError("Boolean mod must be either", True, "for Zn or", False, "for [n].")
        self.mod = mod

        super(RbProductsEq, self).__init__(n, len(a), RbProductsEq, (n, a, b, mod))

    def _invert(self, i):
        """
        Invert object from index.

        :param i: Index to be inverted
        :return: Object from index
        """
        if self.mod:
            return i
        return i + 1

    def _is_valid_set(self, set):
        """
        Determine whether or not a given set is valid (satisfies equation)

        :param set: Set to be tested
        :return: Boolean for whether or not set is valid
        """
        product = 1
        for a, num in zip(self.a, set):
            product *= a * num
        if self.mod:
            return product % self.n == self.b or product == self.b
        return product == self.b

    def equation(self):
        """
        Get a string-representation of the current equation.

        :return:
        string: Algebraic form of equation with a-coefficients and b-value
        """
        eq = ""
        for i in self.a:
            eq += str(i) + "x * "
        eq = eq[:-2] + "= " + str(self.b) + ", mod = " + str(self.mod)
        return eq
