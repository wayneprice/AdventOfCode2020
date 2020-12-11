

def read_program() :
    program = []
    with open('data/input-day8.txt' , 'r') as fp:
        for line in fp :
            instruction, data = line.split()
            program.append((instruction, int(data)))
    return program


def find_infinite_loop(program) :
    executed = {}
    pc = 0
    acc = 0
    while True :
        instruction, data = program[pc]
        if pc in executed :
            break

        executed[pc] = True
        if instruction == 'acc' :
            pc += 1
            acc += data
        elif instruction == 'jmp' :
            pc += data
        elif instruction == 'nop' :
            pc += 1

    return acc


def run_program(program) :
    success = True
    order = 0
    executed = {}
    pc = 0
    acc = 0
    while pc < len(program) :
        instruction, data = program[pc]
        if pc in executed :
            break

        executed[pc] = order
        order += 1

        if instruction == 'acc' :
            pc += 1
            acc += data
        elif instruction == 'jmp' :
            pc += data
        elif instruction == 'nop' :
            pc += 1

    if pc != len(program) :
        success = False

    return success, acc


def find_corrupted_instruction(program) :
    for idx in range(len(program)) :
        temp = list(program)
        if temp[idx][0] == 'acc' :
            continue
        elif temp[idx][0] == 'nop' :
            temp[idx] = ('jmp', temp[idx][1])
        elif temp[idx][0] == 'jmp' :
            temp[idx] = ('nop', temp[idx][1])

        status, acc = run_program(temp)
        if status :
            return acc

    return None


program = read_program()

print(find_infinite_loop(program))
print(find_corrupted_instruction(program))



