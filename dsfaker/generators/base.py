# -*- coding: utf-8 -*-
from functools import reduce
import operator

import numpy


class Generator():
    def get_single(self) -> float:
        """
        A function that returns a single element.
        Not implemented.
        """
        raise NotImplementedError("get_single not implemented")

    def stream_single(self) -> float:
        while True:
            yield self.get_single()

    def get_batch(self, batch_size: int) -> numpy.array:
        """
        A function that returns a single batch of elements.
        Not implemented.
        """
        raise NotImplementedError("get_batch not implemented")

    def stream_batch(self, batch_size: int) -> numpy.array:
        while True:
            yield self.get_batch(batch_size=batch_size)

    def __add__(self, other):
        return AddOperator(self, other)

    def __sub__(self, other):
        return SubOperator(self, other)

    def __truediv__(self, other):
        return TrueDivOperator(self, other)

    def __floordiv__(self, other):
        return FloorDivOperator(self, other)

    def __mul__(self, other):
        return MulOperator(self, other)

    def __pow__(self, other):
        return PowOperator(self, other)

    def __mod__(self, other):
        return ModOperator(self, other)

    def __and__(self, other):
        return AndOperator(self, other)

    def __or__(self, other):
        return OrOperator(self, other)

    def __xor__(self, other):
        return XorOperator(self, other)


class FiniteGenerator(Generator):
    finite = True

    def get_all(self, *args, **kwargs) -> numpy.array:
        """
        A function that returns all the elements.
        Not implemented.
        """
        raise NotImplementedError("get_all not implemented")


class InfiniteGenerator(Generator):
    finite = False
    pass


class BoundedGenerator(Generator):
    def __init__(self, generator: Generator, lb: float, ub: float):
        self.generator = generator
        self.lb = lb
        self.ub = ub

    def get_single(self):
        return numpy.clip(self.generator.get_single(), self.lb, self.ub)

    def get_batch(self, batch_size: int):
        return numpy.clip(self.generator.get_batch(batch_size=batch_size), self.lb, self.ub)


class UniqueValueGenerator(InfiniteGenerator):
    def __init__(self, value, dtype: numpy.dtype):
        self.value = value
        self.dtype = dtype

    def get_single(self) -> float:
        return self.value

    def get_batch(self, batch_size: int) -> numpy.array:
        return numpy.ones(batch_size, dtype=self.dtype) * self.value


class ApplyFunctionOperator(Generator):
    def __init__(self, function, generator: Generator):
        self.function = function
        self.generator = generator

    def get_single(self) -> float:
        return self.function(self.generator.get_single())

    def get_batch(self, batch_size: int) -> numpy.array:
        return self.function(self.generator.get_batch(batch_size=batch_size))


class AbsoluteOperator(ApplyFunctionOperator):
    def __init__(self, generator):
        super().__init__(numpy.absolute, generator)


class ReduceOperator(Generator):
    def __init__(self, *generators, reduce_lambda):
        self.generators = generators
        self.reduce_lambda = reduce_lambda

    def get_single(self) -> float:
        return reduce(lambda a, b: self.reduce_lambda(a.get_single(), b.get_single()), self.generators)

    def get_batch(self, batch_size: int) -> numpy.array:
        return reduce(lambda a, b: self.reduce_lambda(a.get_batch(batch_size=batch_size), b.get_batch(batch_size=batch_size)), self.generators)


class AddOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.add)


class SubOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.sub)


class TrueDivOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.truediv)


class FloorDivOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.floordiv)


class MulOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.mul)


class PowOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.pow)


class ModOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.mod)


class AndOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.and_)


class OrOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.or_)


class XorOperator(ReduceOperator):
    def __init__(self, *generators):
        super().__init__(*generators, reduce_lambda=operator.xor)
