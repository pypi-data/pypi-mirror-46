from functools import reduce
from math import factorial

def pymutation(
    elements: list,
    event: list,
    combination: bool = False
):
    if len(event) > len(elements):
        raise ValueError('event can\'t be longer than elements')

    cache = {}

    for condition in event:
        if cache.get(condition) is not None:
            continue
        cache[condition] = {}
        for element in elements:
            if cache[condition].get(element) is None:
                cache[condition][element] = 0
            if callable(condition) and condition(element):
                cache[condition][element] += 1
            elif condition == element:
                cache[condition][element] += 1

    if combination:
        func = nCr
    else:
        func = nPr

    event_set = set(event)
    return int(reduce((lambda x, y: x * y), map(lambda x: func(sum(cache[x].values()), event.count(x)), event_set)))

def nPr(n, r):
    return factorial(n) / factorial(n - r)

def nCr(n, r):
    return factorial(n) / (factorial(r) * factorial(n - r))
