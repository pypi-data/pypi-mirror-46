import random
from typing import List, Tuple, Union
from functools import reduce
from operator import mul

from .elements import (Datum, Entity)
from .toolkits.get_kth_combination import get_kth_combination
from .toolkits.partition_by_entities import partition_by_entities


__all__ = [
    'expand_by_entities',
]


def _aggregate_entities(
        list segments,  # noqa: E999
        list entity_labels,
    ):
    cdef list entities = []
    cdef int pointer = 0
    cdef int len_segment

    for seg, entity_label in zip(segments, entity_labels):
        len_seg = len(seg)
        if entity_label is None:
            pointer += len_seg
            continue

        entity = Entity(
            label=entity_label,
            value=seg,
            start=pointer,
            end=pointer + len_seg
        )
        entities.append(entity)
        pointer += len_seg
    return entities


def expand_by_entities(
        datum,
        sampling_method=None,
        bint include_orig=False,
    ):
    if not datum.has_entities():
        return [datum]

    if sampling_method is None:
        sampling_method = lambda n_combinations: list(range(n_combinations))  # noqa: E731
        # return all possible combinations

    parts, entity_labels = partition_by_entities(datum, include_orig)

    n_combinations = reduce(mul, [len(part) for part in parts])

    ints = sampling_method(n_combinations)

    result = []
    for idx in ints:
        segments = get_kth_combination(parts, idx)

        utterance = ''.join(segments)
        entities = _aggregate_entities(segments, entity_labels)
        new_datum = Datum(
            utterance=utterance,
            intents=datum.copy_intents(),
            entities=entities,
        )
        result.append(new_datum)
    return result
