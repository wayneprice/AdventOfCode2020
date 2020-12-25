publickey1 = 11404017
publickey2 = 13768789

def transform(subject_number, loopsize):
    value = 1
    while loopsize > 0 :
        value = (value * subject_number) % 20201227
        loopsize -= 1
    return value

def find_loop_size(subject_number, public_key) :
    loopsize = 0
    value = 1
    while value != public_key :
        value = (value * subject_number) % 20201227
        loopsize += 1
    return loopsize

print('searching')
loopsize1 = find_loop_size(7, publickey1)
loopsize2 = find_loop_size(7, publickey2)

print('Loop sizes:', loopsize1, loopsize2)

print('Encrypt 1:', transform(publickey1, loopsize2))
print('Encrypt 2:', transform(publickey2, loopsize1))
