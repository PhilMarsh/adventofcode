from collections import defaultdict
import sys

def yield_bridges(comp_lookup, in_port=0):
    for out_port in set(comp_lookup[in_port]):
        component = (in_port, out_port)
        head = (component,)
        yield head
        comp_lookup[in_port].discard(out_port)
        comp_lookup[out_port].discard(in_port)
        for tail in yield_bridges(comp_lookup, out_port):
            yield head + tail
        comp_lookup[in_port].add(out_port)
        comp_lookup[out_port].add(in_port)

def bridge_strength(bridge):
    return sum(
        port
        for component in bridge
        for port in component
    )

components_lookup = defaultdict(set)
for line in sys.stdin.readlines():
    i, o = line.strip().split("/")
    i = int(i)
    o = int(o)
    components_lookup[i].add(o)
    components_lookup[o].add(i)

# print(sorted(components_lookup.items()))

bridges = {
    bridge_strength(b): b
    for b in yield_bridges(components_lookup)
}

# print(bridges)

print(max(bridges))