import random


class Instance(object):

    def __init__(self, value, name, size):
        if value is None or name is None or size is None:
            raise ValueError('Your instance provider should provide a dict with name, size and value')
        self.value = value
        self.name = name
        self.size = size

    @property
    def label(self):
        return f'{self.name}:{self.size}'

    def __eq__(self, other):
        if other is not None and isinstance(other, Instance):
            return self.name == other.name and self.size == other.size
        return False

    def __str__(self):
        return f'name: {self.name}, size: {self.size}, value: {self.value}'


class InstanceProvider:

    def __init__(self, fn=None):
        """Provides a static instance creator.

        :param fn fn: A function that returns the instance
        """
        self.fn = fn

    def new_instance(self):
        """Provides a new instance value from fn.

        :returns: Instance type
        """
        return Instance(**self.fn())


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
        return Instance(name=f'growing', size=size, value={'instance': random.sample(range(size * 2), size)})


class GeneratorProvider(InstanceProvider):

    def __init__(self, generator):
        self.__generator = generator

    def new_instance(self):
        """Provides a new instance value from next(fn).

        :returns: dict
        """
        return Instance(**next(self.__generator))


class ValuesProvider(InstanceProvider):

    def __init__(self, values):
        self.__last = -1
        self.__values = values

    def new_instance(self):
        """Provides a new value from values.

        :returns: dict
        """
        self.__last += 1
        return Instance(**self.__values[self.__last])


def values(values):
    return ValuesProvider(values)


def generator(generator):
    return GeneratorProvider(generator)


def growing(initial_size=10, growth_rate=0.1, growth_size=0):
    return GrowingNumberSequenceProvider(initial_size=initial_size, growth_rate=growth_rate, growth_size=growth_size)
