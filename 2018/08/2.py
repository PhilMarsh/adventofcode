import sys
from collections import namedtuple


Node = namedtuple("Node", ["children", "meta", "value"])

def new_node(data):
    num_child = data[0]
    num_meta = data[1]
    children = list()

    data = data[2:]
    print(num_child, num_meta)
    for i in range(num_child):
        new_child, data = new_node(data)
        children.append(new_child)
    meta = data[:num_meta]
    remaining = data[num_meta:]
    if num_child == 0:
        value = sum(meta)
    else:
        value = sum(children[i-1].value for i in meta if i <= num_child)

    return Node(children=children, meta=meta, value=value), remaining

data = list(int(i) for i in sys.stdin.read().strip("\n").split(" "))

root, remaining = new_node(data)

print(root.meta, remaining)


print(root.value)
