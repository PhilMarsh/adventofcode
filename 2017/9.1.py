import sys

def score_string(s):
    skip_next = False
    in_garbage = False
    level = 0
    score = 0;
    for c in s:
        if skip_next:
            skip_next = False
        elif c == "!":
            skip_next = True
        elif in_garbage:
            if c == ">":
                in_garbage = False
            # ignore anything else
        elif c == "<":
            in_garbage = True
        elif c == "{":
            level += 1
            score += level
        elif c == "}":
            level -= 1
    return score

print(score_string(sys.argv[1]))
