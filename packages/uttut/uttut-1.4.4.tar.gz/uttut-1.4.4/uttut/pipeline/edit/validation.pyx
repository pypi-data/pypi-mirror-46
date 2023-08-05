def _validate_start_end(start, end):
    _validate_start_end_in_c(start, end)


def _validate_disjoint(sorted_objs):
    _validate_disjoint_in_c(sorted_objs)


cdef void _validate_start_end_in_c(unsigned int start, unsigned int end) except *:  # noqa: E999
    if start > end:
        raise ValueError("start cannot be greater than end")


cdef void _validate_disjoint_in_c(list sorted_objs) except *:
    '''
    An object must have two integer properties `start` and `end`.
    '''
    cdef unsigned int current

    current = sorted_objs[0].end  # type: ignore
    for obj in sorted_objs[1:]:
        if obj.start < current:  # type: ignore
            raise ValueError(f"overlapped")
        current = obj.end  # type: ignore
