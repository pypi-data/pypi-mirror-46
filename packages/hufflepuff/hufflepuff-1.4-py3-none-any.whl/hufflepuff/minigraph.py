import collections
import itertools
import shutil

def horizontal_resize(data, width):
    for x in range(width):
        i = int(x / width * len(data))
        j = int((x + 1) / width * len(data))
        yield sum(data[i:j], [])

def assign_labels(labels, y_buckets):
    # Intervals should be ascending.
    assert y_buckets == sorted(y_buckets)

    for label in labels:
        for i, (_, upper) in enumerate(y_buckets):
            if label <= upper:
                yield label, i
                break
        else:
            # This happens for floating point errors, because this function's
            # interface was poorly designed. Fortunately, we can just assert
            # that's what's happened, and recover correctly.
            assert abs(label - upper) < 0.001
            yield label, i

def minigraph(data, size=None, thresholds=()):
    if size is None:
        size = shutil.get_terminal_size()
    width, height = size
    assert height > 1

    thresholds = list(thresholds)

    min_data_y = min(min(column) for column in data)
    max_data_y = max(max(column) for column in data)

    min_y = min(min_data_y, min(thresholds))
    max_y = max(max_data_y, max(thresholds))
    # TODO: avoid this restriction
    assert min_y < max_y

    y_buckets = [
        (
            min_y + y / height * (max_y - min_y),
            min_y + (y + 1) / height * (max_y - min_y),
        )
        for y in range(height)
    ]

    labels = [min_data_y, max_data_y] + thresholds
    labels = set(labels)
    labels_width = max(len(str(y)) for y in labels)

    output = [
        [' '] * width
        for _ in range(height)
    ]
    for label, y in assign_labels(labels, y_buckets):
        label = str(label).rjust(labels_width)
        for x, c in enumerate(label):
            output[y][x] = c

    data_width = width - labels_width
    assert data_width > 0

    for x, column in enumerate(horizontal_resize(data, data_width)):
        for _, y in assign_labels(column, y_buckets):
            output[y][labels_width + x] = '+'

    for row in output[::-1]:
        print(''.join(row))
