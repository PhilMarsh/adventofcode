with open("input") as f:
    base_program = [
        int(i)
        for i in f.read().split(",")
    ]

def run(noun, verb):
    program = list(base_program)
    program[1] = noun
    program[2] = verb

    i = 0
    while program[i] != 99:
        opcode, a_i, b_i, res_i = program[i:i+4]
        if opcode == 1:
            program[res_i] = program[a_i] + program[b_i]
        elif opcode == 2:
            program[res_i] = program[a_i] * program[b_i]
        else:
            raise Exception(f"{i}: {opcode}")
        i += 4

    return program[0]

for n in range(100):
    for v in range(100):
        res = run(n, v)
        if res == 19690720:
            print(n, v)
            break
