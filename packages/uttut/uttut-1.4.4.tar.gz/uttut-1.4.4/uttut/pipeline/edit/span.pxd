cdef class Span:  # noqa: E999

    cdef public unsigned int start
    cdef public unsigned int end

cdef class SpanGroup:

    cdef list _spans
    cdef bint _is_done

    cpdef void add(self, unsigned int start, unsigned int end)
    cpdef void done(self) except *
    cpdef bint is_empty(self)

    cdef void _validate_contiguousness(self, list sorted_spans) except *
