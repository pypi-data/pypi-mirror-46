from typing import List
import warnings

from .validation cimport (  # noqa: E211, E999
    _validate_start_end_in_c,
    _validate_disjoint_in_c,
)


cdef class Replacement:

    '''Represents an edit to a Sequence such as a string or a list

    A sequence is a collection of objects that can be indexed in a linear fashion. E.g. a string

    A `Replacement` stores the data for substitution of values in a sequence.
    It represents the replacing a continuous slice of the sequence with the items of `new_value`.
    (The semantics are similar to Python's built-in slice assignment feature
     https://docs.python.org/3/reference/simple_stmts.html#assignment-statements ,
     but more restrictive in that negative integers are not allowed for `start` and `end`.)


    E.g.
    The transformation from "" to "abc": Replacement(0, 0, "abc")
    The transformation from "abc" to "aBc": Replacement(1, 2, "B")
    The transformation from "aBc" to "aBcdef": Replacement(3, 3, "def")
    The transformation from "aBcdef" to "": Replacement(0, 6, "")
    Note that insertion at position i is represented as Replacement(i, i, ...)
    ("Insertion at i" means that the original i-th element is moved to the right;
     similar to Python's list.insert)

    Args:
        start (int): start index (inclusive)
        end (int): end index (exclusive)
        new_value (obj): the new subsequence
        annotation (str, optional): an annotation for this replacement
    '''

    def __cinit__(
            self,
            unsigned int start,
            unsigned int end,
            object new_value,
            object annotation=None,
        ):
        _validate_start_end_in_c(start, end)
        self.start = start
        self.end = end
        self.new_value = new_value
        self.annotation = annotation

    def __eq__(self, other):
        same_start = other.start == self.start
        same_end = other.end == self.end
        same_new_values = other.new_value == self.new_value
        return same_start and same_end and same_new_values

    def __str__(self):
        cdef str output_str
        output_str = f"({self.start}, {self.end}) => '{self.new_value}'"
        return output_str

    def __repr__(self):
        cdef str representation
        representation = f"Replacement({self.start}, {self.end}, " \
            f"{self.new_value}, annotation={self.annotation})"
        return representation

    def __hash__(self):
        cdef int hash_num
        hash_num = hash((self.start, self.end))
        return hash_num


cdef class ReplacementGroup:   # noqa: E999

    def __cinit__(self):
        self._replacements = []
        self._is_done = False

    cpdef void add(  # type: ignore
            self,
            unsigned int start,
            unsigned int end,
            object new_value,
            object annotation=None,
        ):
        cdef Replacement replacement

        replacement = Replacement(
            start=start,
            end=end,
            new_value=new_value,
            annotation=annotation,
        )
        self._replacements.append(replacement)

    cpdef void done(self, bint skip_sort=False) except *:

        cdef unsigned int n_replacements

        self._replacements = list(set(self._replacements))

        n_replacements = len(self._replacements)

        if (n_replacements != 0) and (not skip_sort):
            self._validate_new_values()
            self._replacements = _sort_replacements(self._replacements)
            _validate_disjoint_in_c(self._replacements)

        self._is_done = True

    cdef void _validate_new_values(self) except *:
        target_type = type(self._replacements[0].new_value)
        for i, rep in enumerate(self._replacements):
            if not isinstance(rep.new_value, target_type):
                raise TypeError(
                    f"the new_value of {i}-th element is not a(an) {target_type.__name__}")

    @classmethod
    def add_all(cls, list replacements):  # type: ignore
        '''
        replacements = [
            (
                start: int,
                end: int,
                new_value: str or tokens,
                annotation: str, # optional
            ),
            ...
        ]
        '''
        cdef ReplacementGroup replacement_group
        cdef tuple replacement

        replacement_group = cls()
        for replacement in replacements:
            replacement_group.add(*replacement)
        replacement_group.done()
        return replacement_group

    cpdef bint is_empty(self):
        return len(self._replacements) == 0

    def __eq__(self, other):
        self._warn_not_done()
        if not isinstance(other, ReplacementGroup):
            return False
        same_length = len(other) == len(self._replacements)
        same_elements = set(other) == set(self._replacements)
        return same_length and same_elements

    def __getitem__(self, value):
        if not self._is_done:
            raise RuntimeError('Please call `done` first.')
        return self._replacements[value]

    def __len__(self):
        self._warn_not_done()
        return len(self._replacements)

    def _warn_not_done(self):
        if not self._is_done:
            warnings.warn('ReplacementGroup needs validation, please call `done`.')

    def __repr__(self):
        cdef int n_elements
        n_elements = len(self._replacements)
        return f"ReplacementGroup has {n_elements} elements"


cdef list _sort_replacements(list replacements):

    cdef Replacement e

    replacements = sorted(replacements, key=lambda e: e.end)
    replacements = sorted(replacements, key=lambda e: e.start)
    return replacements
