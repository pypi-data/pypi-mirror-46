from typing import List, Iterable


def get_kth_combination(
        iterables: List[Iterable],
        k: int,
    ):
    return get_kth_combination_in_c(
        iterables=iterables,
        k=k,
    )


cdef list get_kth_combination_in_c(  # noqa: E999
        list iterables,
        int k,
    ):
    cdef list output
    cdef int i, n_iters, chosen_id, k_in_suffix

    n_iters = len(iterables)
    output = []
    k_in_suffix = k

    for i in range(n_iters):
        iter_ = iterables[i]
        chosen_id = k_in_suffix % len(iter_)
        output.append(iter_[chosen_id])
        k_in_suffix = k_in_suffix // len(iter_)
    return output
