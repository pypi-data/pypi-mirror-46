import numpy


def subsequence_length(start, stop, step):
    """
    Return the length of the subsequence corresponding to a
    ``slice`` object with the given attributes applied to a sequence.
    """
    if (step > 0 and stop <= start) or (step < 0 and stop >= start):
        return 0
    else:
        if step > 0:
            return (stop - start - 1) // step + 1
        else:
            return (start - stop - 1) // (-step) + 1


def subarray_shape(base_shape, indices):
    shape = []
    for l, index in zip(base_shape, indices):
        if isinstance(index, slice):
            shape.append(subsequence_length(*index.indices(l)))
    return tuple(shape)


def normalized_slice(full_len, start, stop, step):
    """
    Returns a ``slice`` object with all possible concrete numerical values
    replaced with ``None``, while keeping invariant the effect of the slice
    on a sequence of length ``full_len``.
    """
    if (stop < 0 and step < 0) or (stop >= full_len and step > 0):
        stop = None

    if (start <= 0 and step > 0) or (start >= full_len - 1 and step < 0):
        start = None

    if step == 1:
        step = None

    return slice(start, stop, step)


def apply_slice(full_len, old_slice, new_slice):
    """
    Return a slice that, after being applied to a sequence of length ``full_len``,
    produces the same subsequence as a successive application of
    ``old_slice`` and ``new_slice``.
    """

    if full_len == 0:
        return slice(0, 0, None)

    old_start, old_stop, old_step = old_slice.indices(full_len)
    old_len = subsequence_length(old_start, old_stop, old_step)

    if old_len == 0:
        return slice(0, 0, None)

    new_start, new_stop, new_step = new_slice.indices(old_len)
    new_len = subsequence_length(new_start, new_stop, new_step)

    if new_len == 0:
        return slice(0, 0, None)

    start = old_start + new_start * old_step
    step = old_step * new_step

    stop1 = old_stop
    stop2 = old_start + old_step * new_stop

    stops = []
    if (step > 0) == (stop1 > start):
        stops.append(stop1)
    if (step > 0) == (stop2 > start):
        stops.append(stop2)

    stop = (max if step < 0 else min)(stops)

    return normalized_slice(full_len, start, stop, step)


def apply_index(full_len, old_index, new_index):
    if isinstance(new_index, slice):
        return apply_slice(full_len, old_index, new_index)
    else:
        start, stop, step = old_index.indices(full_len)
        return start + step * new_index


def index_str(index):
    """
    Return an index expression (``start:stop:step``) corresponding to the given slice.
    """
    if isinstance(index, slice):
        start_str, stop_str, step_str = [
            "" if s is None else str(s)
            for s in (index.start, index.stop, index.step)]

        parts = [start_str, stop_str] + ([] if index.step is None else [step_str])

        return ":".join(parts)
    else:
        return str(index)


def hash_index(index):
    if isinstance(index, slice):
        return hash(('slice', index.start, index.stop, index.step))
    else:
        return index


class View:
    """
    Represents a view of a multi-dimensional array produced by successive application
    of standard indexing (that is, slices or integer indices).

    :param base_shape: the shape of the original array.
    :param index: a sequence of slices or integer indices corresponding to each axis of the array.

    .. py:attribute:: base_shape

        The shape of the original array.

    .. py:attribute:: index

        A sequence of slices or integer indices corresponding to each axis of the array.

    """

    def __init__(self, base_shape, indices=None):
        self.base_shape = base_shape
        if indices is None:
            self.indices = tuple(slice(None) for i in range(len(base_shape)))
        else:
            self.indices = tuple(indices)
        self.shape = subarray_shape(self.base_shape, self.indices)

    def __getitem__(self, indices):

        if not isinstance(indices, tuple):
            indices = (indices,)

        if len(indices) < len(self.shape):
            indices = indices + (slice(None),) * (len(self.base_shape) - len(indices))
        elif len(indices) > len(self.shape):
            raise IndexError("too many indices for array")

        view_shape_idx = 0
        new_indices = []
        for base_shape_idx in range(len(self.base_shape)):
            old_index = self.indices[base_shape_idx]
            if isinstance(old_index, slice):
                new_index = indices[view_shape_idx]
                full_len = self.base_shape[base_shape_idx]
                new_indices.append(apply_index(full_len, old_index, new_index))
                view_shape_idx += 1
            else:
                new_indices.append(old_index)

        return View(self.base_shape, indices=new_indices)

    def __repr__(self):
        return "View({shape})[{slices}]".format(
            shape=self.base_shape, slices=",".join(index_str(s) for s in self.indices))

    def __eq__(self, other):
        return (
            self.base_shape == other.base_shape and
            all(s == os for s, os in zip(self.indices, other.indices)))

    def __hash__(self):
        return hash(
            ('View', self.base_shape)
            + tuple(hash_index(index) for index in self.indices))


def type_view(tp, view):
    view_len = len(view.base_shape)
    assert tp.shape[:view_len] == view.base_shape
    concrete_slices = [slice(*s.indices(l)) for s, l in zip(view.index, view.base_shape)]

    new_strides = (
        tuple(stride * s.step
            for stride, s in zip(tp.strides[:view_len], concrete_slices))
        + tp.strides[view_len:])
    new_offset = (
        tp.offset
        + sum(stride * s.start for stride, s in zip(tp.strides[:view_len], concrete_slices)))
    new_shape = (
        tuple(subsequence_length(s.start, s.stop, s.step) for s in concrete_slices)
        + tp.shape[view_len:])

    return Type(tp.dtype, new_shape, strides=new_strides, offset=new_offset)


def test_slice():

    rng = numpy.random.RandomState(123)

    max_len = 30

    l1 = []
    l2 = []

    for i in range(100000):
        print("*** test", i)

        length = rng.randint(1, max_len)

        old_start = rng.randint(-1, max_len)
        old_stop = rng.randint(-1, max_len)

        old_start = None if old_start == -1 else old_start
        old_stop = None if old_stop == -1 else old_stop

        new_start = rng.randint(-1, max_len)
        new_stop = rng.randint(-1, max_len)

        new_start = None if new_start == -1 else new_start
        new_stop = None if new_stop == -1 else new_stop

        old_step = rng.randint(-5, 6)
        old_step = None if old_step == 0 else old_step

        new_step = rng.randint(-5, 6)
        new_step = None if new_step == 0 else new_step

        old_slice = slice(old_start, old_stop, old_step)
        new_slice = slice(new_start, new_stop, new_step)

        a = numpy.arange(length)
        ref = a[old_slice][new_slice]
        test_slice = apply_slice(length, old_slice, new_slice)
        test = a[test_slice]

        l1.append(len(a[old_slice]))
        l2.append(len(ref))

        if ref.size != test.size or not (ref == test).all():
            print("length", length)
            print("old slice", old_slice)
            print("new slice", new_slice)
            print("result slice", test_slice)
            print("reference", ref)
            print("test", test)
            break

    l1 = numpy.array(l1)
    l2 = numpy.array(l2)

    print(l1.mean(), l1.std(), l1.min(), l1.max())
    print(l2.mean(), l2.std(), l2.min(), l2.max())


if __name__ == '__main__':

    #test_slice()

    i1 = View((10, 20))
    print(i1)

    i2 = i1[1:10, 1]
    print(i2)

    i3 = i2[2:4]
    print(i3)

