from typing import List, Sequence, MutableSequence, Union

from .replacement cimport Replacement, ReplacementGroup  # noqa: E999


def _transform_sequence(
        input_seq: Union[str, List[str]],
        ReplacementGroup replacement_group,
        list output,
    ) -> Sequence:
    '''
    input_seq: list of str or pure str
    '''

    cdef unsigned int start, i
    cdef Replacement replacement

    start = 0
    i = 0
    for replacement in replacement_group:
        output[i] = input_seq[start: replacement.start]
        output[i + 1] = replacement.new_value
        start = replacement.end
        i += 2

    # tail
    output[-1] = input_seq[start:]

    return output


def _gen_inverse_replacement_group(
        input_seq: Union[str, List[str]],
        ReplacementGroup replacement_group,
    ) -> ReplacementGroup:
    '''
    input_seq: list of str or pure str
    '''

    cdef unsigned int n_replacement, start, dist
    cdef list dists
    cdef Replacement replacement
    cdef ReplacementGroup inverse_replacement_group

    inverse_replacement_group = ReplacementGroup()

    if replacement_group.is_empty():
        inverse_replacement_group.done()
        return inverse_replacement_group

    n_replacement = len(replacement_group)

    dists = get_dist_bt_replacement_group(replacement_group)
    dists.append(0)

    start = replacement_group[0].start

    for i in range(n_replacement):
        replacement = replacement_group[i]
        dist = dists[i]
        inverse_replacement_group.add(
            start=start,
            end=start + len(replacement.new_value),
            new_value=input_seq[replacement.start: replacement.end],
        )
        start += len(replacement.new_value) + dist
    inverse_replacement_group.done()
    return inverse_replacement_group


def get_dist_bt_replacement_group(ReplacementGroup replacement_group) -> List[int]:

    '''Compute the distance between replacement_group

    The distance is the length of sequence.

    Eg.
        Given [Replacement(0, 1, ''), Replacement(4, 7, '')]: [3]  # 4 - 1
        Given [Replacement(0, 3, ''), Replacement(3, 4, ''), Replacement(8, 11, '')]: [0, 4]
    Note that the length of output would be 1 less than that of input replacement_group.

    Arg:
        replacement_group (ReplacementGroup)

    Return:
        dist (ints)
    '''

    cdef unsigned int n_replacement, dist
    cdef list dists
    cdef Replacement current_replacement, next_replacement

    n_replacement = len(replacement_group)
    dists = [0] * (n_replacement - 1)

    for i in range(n_replacement - 1):
        current_replacement = replacement_group[i]
        next_replacement = replacement_group[i + 1]
        dist = next_replacement.start - current_replacement.end
        dists[i] = dist

    return dists
