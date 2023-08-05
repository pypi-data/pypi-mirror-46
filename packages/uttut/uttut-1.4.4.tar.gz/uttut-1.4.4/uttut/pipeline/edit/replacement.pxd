cdef class Replacement:  # noqa: E999

    cdef public unsigned int start
    cdef public unsigned int end
    cdef public object new_value
    cdef public object annotation


cdef class ReplacementGroup:   # noqa: E999

    cdef list _replacements
    cdef bint _is_done

    cpdef void add(
        self,
        unsigned int start,
        unsigned int end,
        object new_value,
        object annotation=?,
    )
    cpdef void done(self, bint skip_sort=?) except *
    cpdef bint is_empty(self)

    cdef void _validate_new_values(self) except *
