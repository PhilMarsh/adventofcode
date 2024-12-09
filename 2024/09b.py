import dataclasses
import itertools


_FREE_BLOCK = None


@dataclasses.dataclass
class _FileEntry:
    file_id: int
    file_size: int
    free_size_after: int


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
    for file_id, (file_size, free_size) in enumerate(
        itertools.zip_longest(disk_map[::2], disk_map[1::2], fillvalue=0)
    ):
        yield _FileEntry(file_id, file_size, free_size)


def _compact_file_entries(file_entries):
    file_entries = list(file_entries)

    source_index = len(file_entries) - 1
    while source_index > 0:
        source_entry = file_entries[source_index]
        for target_index in range(0, source_index):
            target_entry = file_entries[target_index]
            if target_entry.free_size_after < source_entry.file_size:
                continue

            # unsplice old file and empty space entries.
            file_entries[source_index - 1].free_size_after += (
                source_entry.file_size + source_entry.free_size_after
            )
            del file_entries[source_index]

            # splice in new file and free entries.
            source_entry.free_size_after = (
                target_entry.free_size_after - source_entry.file_size
            )
            target_entry.free_size_after = 0
            file_entries.insert(target_index + 1, source_entry)

            # don't update source_index because it is already the next entry now.
            break
        else:
            source_index -= 1

    return file_entries


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
