from typing import List, Tuple
import warnings

from .validation cimport (  # noqa: E999, E211
    _validate_start_end_in_c,
    _validate_disjoint_in_c,
)


cdef class Span:
    '''Integer offsets (start_i, end_i) of a sequence

    Args:
        start (int): start index (inclusive)
        end (int): end index (exclusive)
    '''

    def __cinit__(self, unsigned int start, unsigned int end):
        _validate_start_end_in_c(start, end)
        self.start, self.end = start, end

    def __eq__(self, other):
        if not isinstance(other, Span):
            return False
        same_start = other.start == self.start
        same_end = other.end == self.end
        return same_start and same_end

    def __str__(self):
        return f"({self.start}, {self.end})"

    def __repr__(self):
        return f"Span({self.start}, {self.end})"

    def __hash__(self):
        return hash((self.start, self.end))


cdef class SpanGroup:

    def __init__(self):
        self._spans = []
        self._is_done = False

    cpdef void add(self, unsigned int start, unsigned int end):  # type: ignore
        cdef Span span
        span = Span(start=start, end=end)
        self._spans.append(span)

    cpdef void done(self) except *:

        cdef unsigned int n_spans = len(self._spans)

        if n_spans != 0:
            self._spans = _sorted_spans(self._spans)
            _validate_disjoint_in_c(self._spans)
            self._validate_contiguousness(self._spans)
        self._is_done = True

    cdef void _validate_contiguousness(self, list sorted_spans) except *:

        cdef unsigned int n_spans, idx
        cdef Span span_current, span_next

        n_spans = len(sorted_spans)

        if sorted_spans[0].start != 0:
            raise ValueError('Spans should start from 0')

        for idx in range(n_spans - 1):
            span_current = sorted_spans[idx]
            span_next = sorted_spans[idx + 1]
            if span_current.end != span_next.start:
                raise ValueError('Spans should be contiguous.')

    @classmethod
    def add_all(cls, list spans):  # type: ignore

        cdef SpanGroup span_group
        cdef tuple span
        cdef unsigned int start, end

        span_group = cls()

        for span in spans:
            if len(span) == 2:
                start, end = span
                span_group.add(start, end)
            else:
                raise ValueError('Number of elements should = 2.')
        span_group.done()
        return span_group

    cpdef bint is_empty(self):
        return len(self._spans) == 0

    def __eq__(self, other):
        self._warn_not_done()
        if not isinstance(other, SpanGroup):
            return False
        same_length = len(other) == len(self._spans)
        same_elements = set(other) == set(self._spans)
        return same_length and same_elements

    def __getitem__(self, value):
        if not self._is_done:
            raise RuntimeError('Please call `done` first.')
        return self._spans[value]

    def __len__(self):
        self._warn_not_done()
        return len(self._spans)

    def _warn_not_done(self):
        if not self._is_done:
            warnings.warn('SpanGroup needs validation, please call `done`.')

    def __repr__(self):
        return str(self.__class__.__name__)


cdef list _sorted_spans(list spans):
    return sorted(spans, key=lambda e: e.end)  # set -> list
