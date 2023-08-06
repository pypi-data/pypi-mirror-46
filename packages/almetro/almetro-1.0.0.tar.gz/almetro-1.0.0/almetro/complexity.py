import math


class Complexity:
    def __init__(self, fn=lambda n: n, text='O(n)', latex=r'$\mathcal{O}(n)$'):
        """Provides a complexity notation.

        :param fn fn: A function that calculates the cost
        :param string text: Description label
        :param string latex: Description label compatible with latex notation
        """
        self.__fn = fn
        self.__text = text
        self.__latex = latex

    @property
    def text(self):
        return self.__text

    @property
    def latex(self):
        return self.__latex if self.__latex else self.__text

    @property
    def fn(self):
        return self.__fn


cn = Complexity()
cn_quadratic = Complexity(lambda n: n**2, text='O(n^2)', latex=r'$\mathcal{O}(n^2)$')
cn_cubic = Complexity(lambda n: n**3, text='O(n^3)', latex=r'$\mathcal{O}(n^3)$')
cn_log_n = Complexity(lambda n: n * math.log2(n), text='O(n lg n)', latex=r'$\mathcal{O}(n*\log{n})$')
clog_n = Complexity(lambda n: math.log2(n), text='O(lg n)', latex=r'$\mathcal{O}(\log{n})$')
c_one = Complexity(lambda n: 1, text='O(1)', latex=r'$\mathcal{O}(1)$')
