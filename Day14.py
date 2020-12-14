

with open('data/input-day14.txt', 'r') as fp:
    instructions = fp.readlines()


# Part 1 - Mask = data mask

mem = {}
and_mask = 0
or_mask = 0

for instruction in instructions :
    command, value = instruction.split(' = ')

    if command == 'mask' :
        or_mask = int(value.replace('X', '0'), 2)
        and_mask = int(value.replace('X', '1'), 2)

    else :
        address = int(command[3:].strip('[]'))
        mem[address] = (int(value) | or_mask) & and_mask

print(sum(mem.values()))


# Part 2 - Mask = Address mask

def getAddresses(mask, address) :
    addressBinary = '{:b}'.format(address).zfill(len(mask))

    newMask = ''.join([a if m == '0' else m for (m, a) in zip(mask, addressBinary)])

    floatCount = newMask.count('X')
    for i in range(0, pow(2, floatCount)) :
        result = newMask
        floatMask = '{:b}'.format(i).zfill(floatCount)
        for x in floatMask :
            result = result.replace('X', x, 1)
        yield result


mem = {}
for instruction in instructions :
    command, value = instruction.split(' = ')

    if command == 'mask' :
        mask = value.strip()

    else :
        address = int(command[3:].strip('[]'))
        for addr in getAddresses(mask, address) :
            mem[addr] = int(value)

print(sum(mem.values()))

