import almetro.chart as chart
import almetro.table as table
from almetro.complexity import cn
from copy import deepcopy
import timeit


class Metro:
    def __init__(self, complexity):
        self.__start = timeit.default_timer()
        self.__elapsed_time = 0
        self.__experimental = {}
        self.__theoretical = {}
        self.__ratio = {}
        self.__complexity = complexity
        self.__processed = False

    @property
    def elapsed_time(self):
        return self.__elapsed_time

    @property
    def experimental(self):
        return deepcopy(self.__experimental)

    @property
    def theoretical(self):
        return deepcopy(self.__theoretical)

    @property
    def ratio(self):
        return deepcopy(self.__ratio)

    @property
    def complexity(self):
        return self.__complexity

    @property
    def processed(self):
        return self.__processed

    def register(self, size, timestats):
        self.__elapsed_time = timeit.default_timer() - self.__start
        self.__experimental[size] = min(timestats)
        self.__processed = False

    def chart(self):
        self.process()
        return chart.build_chart(self)

    def table(self):
        self.process()
        return table.build_table(self)

    def process(self):
        if not self.__processed:
            if not self.__complexity:
                raise ValueError('complexity must be provided')
            self.__theoretical = {}
            self.__ratio = {}
            for n, t_fn in self.__experimental.items():
                self.__theoretical[n] = self.__complexity.fn(n)
                self.__ratio[n] = t_fn / max(self.__theoretical[n], 0.1)
            self.__processed = True

    @staticmethod
    def new(complexity=cn):
        return Metro(complexity)
