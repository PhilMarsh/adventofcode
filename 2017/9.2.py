import sys

def score_string(s):
    skip_next = False
    in_garbage = False
    level = 0
    score = 0
    garbage_count = 0
    for c in s:
        if skip_next:
            skip_next = False
        elif c == "!":
            skip_next = True
        elif in_garbage:
            if c == ">":
                in_garbage = False
            else:
                garbage_count += 1
        elif c == "<":
            in_garbage = True
        elif c == "{":
            level += 1
            score += level
        elif c == "}":
            level -= 1
    return score, garbage_count

score, garbage = score_string(sys.argv[1])
print(garbage)
