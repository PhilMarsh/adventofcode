import collections
import re
import sys

LINE_REGEX = re.compile(
    r'(?P<name>\w+) \((?P<weight>\d+)\)( -> (?P<children>[\w, ]+))?'
)

Program = collections.namedtuple(
    "Program",
    ["name", "weight", "child_names"]
)

def parse_program(line):
    m = LINE_REGEX.match(line)
    child_names = list()
    if m.group("children"):
        child_names = m.group("children").split(", ")
    return Program(
        name=m.group("name"),
        weight=int(m.group("weight")),
        child_names=child_names
    )

def find_root_name(programs):
    # values are parents;  keys are children
    # root is the parent (value) that is not a child (key)
    all_children = set(
        child
        for p in programs.values()
        for child in p.child_names
    )
    (parent,) = set(programs.keys()) - all_children
    return parent

class BadWeight(Exception):
    def __init__(self, parent, bad_child, bad_subtree_weight,
                 balanced_subtree_weight):
        self.parent = parent
        self.bad_child = bad_child
        self.bad_subtree_weight = bad_subtree_weight
        self.balanced_subtree_weight = balanced_subtree_weight

def get_total_weight(programs, root=None):
    if root is None:
        root = programs[find_root_name(programs)]
    if not root.child_names:
        return root.weight
    child_weights = collections.defaultdict(list)
    for child_name in root.child_names:
        child = programs[child_name]
        weight = get_total_weight(programs, child)
        child_weights[weight].append(child)
    if len(child_weights) == 1:
        (per_child_weight,) = child_weights.keys()
        return (
            root.weight
            + (len(root.child_names) * per_child_weight)
        )
    (good_weight, good_children), (bad_weight, bad_children) = child_weights.items()
    if len(good_children) == 1:
        (good_weight, good_children), (bad_weight, bad_children) \
        = (bad_weight, bad_children), (good_weight, good_children)
    (bad_child,) = bad_children
    raise BadWeight(
        parent=root,
        bad_child=bad_child,
        bad_subtree_weight=bad_weight,
        balanced_subtree_weight=good_weight
    )
    
programs = {
    p.name: p
    for p in (
        parse_program(line)
        for line in sys.argv[1].splitlines()
    )
}

try:
    get_total_weight(programs)
except BadWeight as ex:
    weight_error = ex.balanced_subtree_weight - ex.bad_subtree_weight
    corrected_child_weight = ex.bad_child.weight + weight_error
    print(corrected_child_weight)
else:
    print("wat.")
