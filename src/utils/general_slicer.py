from dataclasses import dataclass
from typing import Callable, Any, List

import numpy as np
from loguru import logger


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
    sliced_sample_num: int = 0      # num of input data
    next_slice_start_id: int = 0
    last_slice_size: int = 0

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
        self.sliced_sample_num = 0
        self.next_slice_start_id = 0
        self.last_slice_size = 0
        return remainder

    def update_start_id(self, data_start_id: int, force_update: bool = False):
        if self.sliced_sample_num == 0 or force_update:
            self.next_slice_start_id = data_start_id
            logger.warning(f"Update slicer start id to {data_start_id}")

    def get_last_slice_start_index(self):
        return self.next_slice_start_id - self.last_slice_size

    def get_next_slice_start_index(self):
        return self.next_slice_start_id


def slice_data(context: SliceContext, data):
    # TODO update slice start id
    slice_func = context.data_manipulator.slice_func

    remainder_size = 0
    remainder_data = context.last_remainder
    context.last_remainder = None
    if remainder_data is not None:
        remainder_size = context.data_manipulator.size_func(remainder_data)
    input_size = context.data_manipulator.size_func(data)
    context.sliced_sample_num += input_size
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
            result = context.data_manipulator.concat_func(outputs)
        else:
            result = outputs[0]
        context.last_slice_size = context.data_manipulator.size_func(result)
        context.next_slice_start_id += context.last_slice_size
        yield result
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
