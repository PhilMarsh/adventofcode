import bisect
import dataclasses
import heapq
import itertools


_FREE_BLOCK = None


@dataclasses.dataclass
class _FileEntry:
    file_id: int
    file_block: int
    file_size: int
    free_size_after: int

    @property
    def total_size(self):
        return self.file_size + self.free_size_after


class _Heap:
    def __init__(self, items=tuple()):
        self._heap = list(items)
        heapq.heapify(self._heap)

    def push(self, val):
        heapq.heappush(self._heap, val)

    def pop(self):
        return heapq.heappop(self._heap)

    def pushpop(self, val):
        return heapq.heappushpop(self._heap, val)

    def clear(self):
        self._heap.clear()

    def __iter__(self):
        return iter(self._heap)


def main():
    disk_map = _load_disk_map()
    file_entries = _yield_file_entries(disk_map)
    compacted_entries = _compact_file_entries(file_entries)
    compacted_blocks = _yield_file_blocks(compacted_entries)
    res = _block_checksum(compacted_blocks)
    print(res)


def _load_disk_map():
    with open("09.in") as file:
        return [int(i) for i in file.read().strip()]


def _yield_file_entries(disk_map):
    file_block = 0
    for file_id, (file_size, free_size) in enumerate(
        itertools.zip_longest(disk_map[::2], disk_map[1::2], fillvalue=0)
    ):
        entry = _FileEntry(
            file_id=file_id,
            file_block=file_block,
            file_size=file_size,
            free_size_after=free_size,
        )
        yield entry

        file_block += entry.total_size


def _compact_file_entries(file_entries):
    file_entries = sorted(file_entries, key=_file_block_sort_key)

    # the compressed disk map format only allows for free spaces of size [0,9].
    # obviously we don't care about 0s. we also don't care about larger spaces
    # that get created by compaction because we're only doing a single pass, so
    # we'll never go back and try to fit previous large files in the new larger
    # spaces.
    free_space_heaps = {size: _Heap() for size in range(1, 10)}
    for entry in file_entries:
        if entry.free_size_after:
            free_space_heaps[entry.free_size_after].push((entry.file_block, entry))

    source_index = len(file_entries) - 1
    while source_index > 0:
        source_entry = file_entries[source_index]

        donor_entry = _pop_donor_entry(free_space_heaps, source_entry)
        if donor_entry is None:
            source_index -= 1
            continue

        # rip file entry out of the list and heal behind it.
        file_entries[source_index - 1].free_size_after += source_entry.total_size
        del file_entries[source_index]

        # make room for file entry and insert it back into the list at its
        # new location.
        source_entry.file_block = donor_entry.file_block + donor_entry.file_size
        source_entry.free_size_after = (
            donor_entry.free_size_after - source_entry.file_size
        )
        donor_entry.free_size_after = 0
        bisect.insort(file_entries, source_entry, key=_file_block_sort_key)

        if (
            source_entry.free_size_after
            and file_entries[source_index] is not source_entry
        ):
            free_space_heaps[source_entry.free_size_after].push(
                (source_entry.file_block, source_entry)
            )

    return file_entries


def _pop_donor_entry(free_space_heaps, recipient_file_entry):
    """
    select the next valid donor from all heaps.
    """
    donor_candidates = _Heap()
    for donor_free_size, donor_heap in free_space_heaps.items():
        if donor_free_size < recipient_file_entry.file_size:
            continue

        try:
            donor_entry_block, donor_entry = donor_heap.pop()
            while donor_entry_block != donor_entry.file_block:
                # outdated donor.
                donor_entry_block, donor_entry = donor_heap.pop()
        except IndexError:
            # no more donors for this size.
            continue

        if donor_entry.file_block >= recipient_file_entry.file_block:
            # all remaining donors of this size are behind us.
            donor_heap.clear()
            continue

        donor_candidates.push((donor_entry.file_block, donor_entry))

    try:
        _, winner = donor_candidates.pop()
    except IndexError:
        return None

    # put the rest back.
    for _, loser in donor_candidates:
        free_space_heaps[loser.free_size_after].push((loser.file_block, loser))

    return winner


def _file_block_sort_key(file_entry):
    return file_entry.file_block


def _yield_file_blocks(file_entries):
    for entry in file_entries:
        for _ in range(entry.file_size):
            yield entry.file_id
        for _ in range(entry.free_size_after):
            yield _FREE_BLOCK


def _block_checksum(blocks):
    return sum(
        index * val for index, val in enumerate(blocks) if val is not _FREE_BLOCK
    )


if __name__ == "__main__":
    main()
