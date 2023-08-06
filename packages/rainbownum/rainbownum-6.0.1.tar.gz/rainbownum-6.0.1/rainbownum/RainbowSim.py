from .LinkedLists import SetLinkedList
from .LinkedLists import ColoringLinkedList
import time, sys, warnings, multiprocessing as mp, queue, itertools


def _generate_process(initialize, params, start, time_limit, coloring, used, loop, queue):
    eq = initialize(*params)
    eq.set_time_limit(time_limit)
    eq.start = start
    eq._gen_colorings(coloring, used, loop, queue)
    return


class _RainbowSim:
    def __init__(self, n, k, initialize, params):
        if type(n) is not int or n < 1:
            raise TypeError("Scalar n must be an integer greater than or equal to 1")
        self.n = n

        if type(k) is not int or k < 2:
            raise TypeError("Scalar k must be an integer greater than or equal to 2")
        self.k = k

        self.initialize = initialize
        self.params = params

        self._generate_sets()

        self.colorings = ColoringLinkedList()

        self.timeLimit = 43200  # 12 hours
        self.start = 0

        self.queue = mp.Queue()
        self.processes = []
        self.cores = mp.cpu_count()
        if self.cores == 1:
            self.splits = 1
        elif self.cores == 2:
            self.splits = 2  # two processes
        elif self.cores <= 8:
            self.splits = 3  # five processes
        elif self.cores <= 16:
            self.splits = 4  # 13? processes
        else:
            self.splits = 5
        if "win" in sys.platform and sys.version_info[0] != 3 or sys.version_info[1] != 7 or sys.version_info[2] != 0:
            warnings.warn("WARNING: Windows users must use Python 3.7.0 to take advantage of multiprocessing.")
            self.splits = 1

    def _generate_sets(self):
        """
        Generate sets for color solving.

        :return: None
        """
        self.sets = [SetLinkedList() for _ in range(self.n + 1)]
        for combination in itertools.combinations(list(range(self.n)), self.k):
            for permutation in itertools.permutations(combination, self.k):
                set = [self._invert(p) for p in permutation]
                if self._is_valid_set(set):
                    self._add_set(permutation)
                    break

    def _gen_colorings(self, coloring, used, loop, queue):
        if time.time() - self.start > self.timeLimit:
            return
        if loop == self.n:
            return
        for i in range(0, self.n):
            if i != 0 and used[i - 1] == 0:
                if loop == self.splits:
                    temp = self.colorings.head
                    i = 1
                    while temp is not None:
                        i += 1
                        queue.put([temp.data, self.colorings.maxColors])
                        temp = temp.next
                return
            used[i] += 1
            coloring[loop] = i
            if self._contains_rainbow_sum(coloring, loop):
                used[i] -= 1
                continue
            if loop == self.splits - 1:
                p = mp.Process(target=_generate_process, args=(self.initialize, self.params, self.start, self.timeLimit, coloring.copy(), used.copy(), loop + 1, self.queue))
                self.processes.append(p)
                p.start()
            else:
                self._gen_colorings(coloring, used, loop + 1, queue)
            if loop == self.n - 1:
                colors = 0
                for j in used:
                    if j == 0:
                        break
                    colors += 1
                colors = max(coloring) + 1
                self.colorings.add_coloring(coloring, colors)
            used[i] -= 1

    def _contains_rainbow_sum(self, coloring, new):
        """
        Check whether coloring contains rainbow set in sets containing specific index.

        :param coloring: Coloring to be checked for rainbow sets
        :param new: Index contained in sets to check
        :return: Boolean describing whether or not coloring contains a rainbow set at index
        """
        temp = self.sets[new].head.next
        while temp is not None:
            skip = False
            used = [0 for _ in range(self.n)]
            unique = True
            for i in temp.data:
                if i > new:
                    skip = True
                    break
                used[coloring[i]] += 1
                if used[coloring[i]] > 1:
                    unique = False
            if skip:
                temp = temp.next
                continue
            if unique:
                return True
            temp = temp.next
        return False

    def _add_set(self, set):
        """
        Add set to SetLinkedList.

        :param set: Set to be added
        :return: None
        """
        for i in set:
            self.sets[i].add_set(set)
        self.sets[self.n].add_set(set)

    def _extreme_colorings(self, quantity=-1):
        """
        Print to console the extreme colorings.

        :param quantity: Quantity of colorings to be printed (default = -1 to print all)
        :return: None
        """
        if self.start != -1:
            temp = self.colorings.head
            i = 0
            while temp is not None and (i < quantity or quantity < 0):
                if i == 0:
                    print(temp, end='')
                else:
                    print(',', temp, end='')
                temp = temp.next
                i += 1
        print()

    def _sets(self, nums=-1, invert=False):
        """
        Print to console the sets generated.

        :param nums: List of numbers whose sets will be printed (default = -1 to print all)
        :return: None
        """
        print('Sets Generated:', end='')
        if nums < 0:
            nums = list(range(self.n))
        for n in nums:
            temp = self.sets[n].head.next
            if invert:
                print('\n', n, ':', list(self._invert(i) for i in temp.data), end='')
            else:
                print('\n', n, ':', temp, end='')
            temp = temp.next
            while temp is not None:
                if invert:
                    print(',', list(self._invert(i) for i in temp.data), end='')
                else:
                    print(',', temp.data, end='')
                temp = temp.next
        print('\n')

    def _invert(self, i):
        """
        Default invert method.

        :param i: Index to be inverted
        :return: Index unchanged
        """
        return i

    def _is_valid_set(self, set):
        """
        Default valid set checker method.

        :param set: Set to be checked for validity
        :return: Boolean describing set validity
        """
        return False

    def run(self):
        """
        Find extreme colorings.

        :return:    1 if time limit WAS NOT reached
                    0 if time limit WAS reached
        """
        self.start = time.time()
        coloring = [-1 for _ in range(self.n)]
        coloring[0] = 0
        used = [0 for _ in range(self.n)]
        used[0] = 1

        self._gen_colorings(coloring, used, 1, self.queue)

        temp_colorings = []
        running = self.processes
        while running:
            try:
                while 1:
                    temp_colorings.append(self.queue.get(False))
            except queue.Empty:
                pass
            time.sleep(0.5)  # Give tasks a chance to put more data in
            if not self.queue.empty():
                continue
            running = [p for p in running if p.is_alive()]

        temp_colorings.sort()
        for data in temp_colorings:
            self.colorings.add_coloring(data[0], data[1])

        if time.time() - self.start > self.timeLimit:
            print("\nRb(" + self.equation() + ", n = " + str(self.n) + ") computation exceed time limit.")
            return None
        print("\nRb(" + self.equation() + ", n = " + str(self.n) + ") = ", str(self.colorings.maxColors + 1))
        print("Total colorings:", self.colorings.len)
        print("Time:", time.time() - self.start)
        return 1

    def check_coloring(self, coloring):
        """
        Check coloring for rainbow sets.

        :param coloring: Coloring to be checked
        :return: None
        """
        for i in range(1, self.n):
            if self._contains_rainbow_sum(coloring, i) is True:
                print("INVALID: Coloring", coloring, "for n =", self.n, "contains rainbow sums :(")
                return
        print("VALID: Coloring", coloring, "for n =", self.n, "works! Yippee!")

    def set_time_limit(self, t):
        """
        Set time limit for maximum computation time.

        :param t: Time limit in seconds
        :return: None
        """
        self.timeLimit = t

    def time_limit_reached(self):
        """
        Check whether time limit has been reached.

        :return: Boolean describing whether time limit has been reached.
        """
        # TODO bug in time_limit_reached likely due to multiprocessing
        return self.start < 0

    def print_extreme_colorings(self, quantity=-1):
        """
        Default method to print extreme colorings.

        :return: None
        """
        self._extreme_colorings(quantity)

    def print_sets(self, nums=-1):
        """
        Default method to print sets.

        :return: None
        """
        self._sets(nums, True)

    def disable_multiprocessing(self):
        self.splits = 0
