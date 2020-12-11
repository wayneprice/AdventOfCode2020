

preamble_size = 25


def find_pair(values, search) :
    for i in range(0, len(values)) :
        for j in range(i, len(values)) :
            if values[i] + values[j] == search and values[i] != values[j] :
                return True
    return False


def find_invalid(values) :
    for idx in range(preamble_size, len(values)) :
        if not find_pair(values[idx-preamble_size:idx], values[idx]) :
            return values[idx]

    return None


def find_contiguous(values, search) :
  i = 0
  j = 1
  sum = values[i] + values[j]
  while sum != search :
    if sum > search :
      sum -= values[i]
      i += 1
    elif sum < search :
      j += 1
      sum += values[j]
  if sum == search :
    return min(values[i:j+1]) + max(values[i:j+1])
  return None

  
with open('data/input-day9.txt', 'r') as fp:
    values = list(map(int, fp.readlines()))

invalid_value = find_invalid(values)
print(invalid_value)
print(find_contiguous(values, invalid_value))

