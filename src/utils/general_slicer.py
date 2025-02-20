from dataclasses import dataclass
from typing import Callable, Any, List

import numpy as np


@dataclass
class SliceManipulator:
    size_func: Callable[[Any], int]
    slice_func: Callable[[Any, int, int], Any]
    concat_func: Callable[[List[Any]], Any]

    @classmethod
    def create_numpy_manipulator(cls, axis: int):
        def slice_numpy(x, start, end, slice_axis):
            indices = [slice(None)] * len(x.shape)
            indices[slice_axis] = slice(start, end)
            return x[tuple(indices)]

        manipulator = SliceManipulator(
            size_func=lambda x: x.shape[axis],
            slice_func=lambda x, start, end: slice_numpy(x, start, end, axis),
            concat_func=lambda x: np.concatenate(x, axis=axis),
        )
        return manipulator

@dataclass
class SliceContext:
    slice_size: int
    data_manipulator: SliceManipulator
    last_remainder: Any = None

    @classmethod
    def create_numpy_slice_context(cls, slice_size: int, slice_axis: int):
        context = SliceContext(
            slice_size=slice_size,
            data_manipulator=SliceManipulator.create_numpy_manipulator(slice_axis),
        )
        return context

    def flush(self):
        remainder = self.last_remainder
        self.last_remainder = None
        return remainder


def slice_data(context: SliceContext, data):
    slice_func = context.data_manipulator.slice_func

    remainder_size = 0
    remainder_data = context.last_remainder
    context.last_remainder = None
    if remainder_data is not None:
        remainder_size = context.data_manipulator.size_func(remainder_data)
    input_size = context.data_manipulator.size_func(data)
    slice_start = -remainder_size
    while slice_start + context.slice_size <= input_size:
        outputs = []
        slice_end = slice_start + context.slice_size
        if slice_start < 0:
            if slice_end < 0:
                outputs.append(slice_func(remainder_data, remainder_size+slice_start, remainder_size+slice_end))
            else:
                outputs.append(slice_func(remainder_data, remainder_size+slice_start, remainder_size))
                if slice_end > 0:
                    outputs.append(slice_func(data, 0, slice_end))
        else:
            outputs.append(slice_func(data, slice_start, slice_end))
        if len(outputs) > 1:
            yield context.data_manipulator.concat_func(outputs)
        else:
            yield outputs[0]
        slice_start += context.slice_size
    remainders = []
    if slice_start < 0:
        remainders.append(slice_func(remainder_data, remainder_size+slice_start, remainder_size))
        if input_size > 0:
            remainders.append(data)
    elif slice_start < input_size:
        remainders.append(slice_func(data, slice_start, input_size))
    if len(remainders) > 1:
        context.last_remainder = context.data_manipulator.concat_func(remainders)
    elif len(remainders) == 1:
        context.last_remainder = remainders[0]
