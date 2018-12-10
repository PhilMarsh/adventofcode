import sys
from collections import namedtuple


Node = namedtuple("Node", ["children", "meta"])

meta_sum = 0

def new_node(data):
    global meta_sum

    num_child = data[0]
    num_meta = data[1]
    children = list()

    data = data[2:]
    print(num_child, num_meta, meta_sum)
    for i in range(num_child):
        new_child, data = new_node(data)
        children.append(new_child)
    meta = data[:num_meta]
    remaining = data[num_meta:]

    meta_sum += sum(meta)

    return Node(children=children, meta=meta), remaining

data = list(int(i) for i in sys.stdin.read().strip("\n").split(" "))

root, remaining = new_node(data)

print(root.meta, remaining)


print(meta_sum)
