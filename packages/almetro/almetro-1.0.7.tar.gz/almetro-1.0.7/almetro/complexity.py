import math


class Complexity:
    def __init__(self, theoretical=lambda n=1: n, experimental=lambda n=1: n, text='O(n)', latex=r'$\mathcal{O}(n)$'):
        """Provides a complexity notation.

        :param theoretical fn: A function that calculates the theoretical cost
        :param experimental fn: A function that calculates the experimental cost
        :param string text: Description label
        :param string latex: Description label compatible with latex notation
        """
        self.__theoretical = theoretical
        self.__experimental = experimental
        self.__text = text
        self.__latex = latex

    @property
    def text(self):
        return self.__text

    @property
    def latex(self):
        return self.__latex if self.__latex else self.__text

    @property
    def theoretical(self):
        return self.__theoretical

    @property
    def experimental(self):
        return self.__experimental


cn = Complexity()
cn_quadratic = Complexity(theoretical=lambda n=1: n**2, text='O(n^2)', latex=r'$\mathcal{O}(n^2)$')
cn_cubic = Complexity(theoretical=lambda n=1: n**3, text='O(n^3)', latex=r'$\mathcal{O}(n^3)$')
cn_log_n = Complexity(theoretical=lambda n=1: n * math.log2(n), text='O(n lg n)', latex=r'$\mathcal{O}(n*\log{n})$')
clog_n = Complexity(theoretical=lambda n=1: math.log2(n), text='O(lg n)', latex=r'$\mathcal{O}(\log{n})$')
c_one = Complexity(theoretical=lambda n=1: 1, text='O(1)', latex=r'$\mathcal{O}(1)$')
