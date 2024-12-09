_FREE_BLOCK = object()


def main():
    disk_map = _load_disk_map()
    map_blocks = _yield_map_blocks(disk_map)
    compacted_blocks = _yield_compacted_blocks(map_blocks)
    res = _block_checksum(compacted_blocks)
    print(res)


def _load_disk_map():
    with open("09.in") as file:
        return [int(i) for i in file.read().strip()]


def _yield_map_blocks(disk_map):
    for index, size in enumerate(disk_map):
        if _map_index_is_file(index):
            file_id = _map_index_file_id(index)
            for _ in range(size):
                yield file_id
        else:
            for _ in range(size):
                yield _FREE_BLOCK


def _map_index_is_file(index):
    return index % 2 == 0


def _map_index_file_id(index):
    return index // 2


def _yield_compacted_blocks(blocks):
    """
    don't bother yielding trailing empty blocks.
    """
    blocks = list(blocks)
    target_index = 0
    source_index = len(blocks) - 1
    while target_index <= source_index:
        if blocks[target_index] is not _FREE_BLOCK:
            yield blocks[target_index]
            target_index += 1
        elif blocks[source_index] is _FREE_BLOCK:
            source_index -= 1
        else:
            yield blocks[source_index]
            target_index += 1
            source_index -= 1


def _block_checksum(blocks):
    return sum(index * val for index, val in enumerate(blocks))


if __name__ == "__main__":
    main()
