"""
program: 2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0

literal translation:
    start:
    b = a % 8               # 2, 4
    b = b ^ 5               # 1, 5
    c = a // (2 ** b)       # 7, 5
    a = a // (2 ** 3)       # 0, 3
    b = b ^ 6               # 1, 6
    b = b ^ c               # 4, 3
    print(b % 8)            # 5, 5
    jnz start               # 3, 0

rearranged as a normal loop:
    while a != 0:
        b = (a % 8) ^ 5
        c = a // (2 ** b)
        d = b ^ 6 ^ c
        print(d % 8)

        a = a // 8

to find the original `a`, we'll step backward through the program, one loop
iteration at a time. for each iteration, we'll generate all possible `a` values
that the iteration _could have_ started with to end up with the known output.
this is effectively just a simple BFS/DFS problem with a _very weird_ "visit"
check. (it would also be _very hard_ to generalize to any arbitrary program
string.)


side-note: to print 16 instructions, we know `8^15 <= a < 8^16`, or `2^45 <= a < 2^48`.
"""

_PROGRAM = [2, 4, 1, 5, 7, 5, 0, 3, 1, 6, 4, 3, 5, 5, 3, 0]


def main():
    candidates = list(_find_initial_a(_PROGRAM))
    print(f"{candidates=}")
    print(min(candidates))


def _find_initial_a(program, reg_a=0):
    if not program:
        yield reg_a
        return

    *program, output = program
    next_reg_a_mod_0 = reg_a * 8
    for next_reg_a in range(next_reg_a_mod_0, next_reg_a_mod_0 + 8):
        if _program_one_iteration_output(next_reg_a) == output:
            yield from _find_initial_a(program, next_reg_a)


def _program_one_iteration_output(reg_a):
    b = (reg_a % 8) ^ 5
    c = reg_a // (2**b)
    d = b ^ 6 ^ c
    return d % 8


if __name__ == "__main__":
    main()
