with open("input") as f:
    program = [
        int(i)
        for i in f.read().split(",")
    ]

program[1] = 12
program[2] = 2

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

print(program[0])
