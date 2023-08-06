import random


class InstanceProvider:

    def __init__(self, fn=None):
        """Provides a static instance creator.

        :param fn fn: A function that returns the instance
        """
        self.fn = fn

    def new_instance(self):
        """Provides a new instance value from fn.

        :returns: any type of instance
        """
        return self.fn()


class GrowingNumberSequenceProvider(InstanceProvider):

    def __init__(self, initial_size=10, growth_rate=0.1, growth_size=0):
        """Provides a growing int sequence without repetition instance creator.

        :param int initial_size: number of elements in the instance. Default is 10.
        :param int growth_rate: growth rate of instance per iteration. Default is 0.1 (10%).
        :param int growth_rate: growth initial_size of instance per iteration. Default is 0.
        """
        self.iterations = 0
        self.initial_size = initial_size
        self.growth = growth_size if growth_size > 0 else initial_size * growth_rate

    def new_instance(self):
        """Provides a new int list as an instance.

        :returns: one int list. For example: [1, 3]
        :rtype: list(int)
        """
        size = int(self.initial_size + (self.iterations * self.growth))
        self.iterations += 1
        return {'instance': random.sample(range(size * 2), size), 'size': size}


class GeneratorProvider(InstanceProvider):

    def new_instance(self):
        """Provides a new instance value from next(fn).

        :returns: dict
        """
        return next(self.fn())


def generator(fn=None):
    return GeneratorProvider(fn)


def growing(initial_size=10, growth_rate=0.1, growth_size=0):
    return GrowingNumberSequenceProvider(initial_size=initial_size, growth_rate=growth_rate, growth_size=growth_size)
