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
        weight=m.group("weight"),
        child_names=child_names
    )

def build_child_to_parent_lookup(programs):
    return {
        child_name: parent.name
        for parent in programs
        for child_name in parent.child_names
    }

def find_root_parent(lookup):
    # values are parents;  keys are children
    # root is the parent (value) that is not a child (key)
    (parent,) = set(lookup.values()) - set(lookup.keys())
    return parent


programs = (
    parse_program(line)
    for line in sys.argv[1].splitlines()
)

print(
    find_root_parent(
        build_child_to_parent_lookup(programs)
    )
)
