import builtins
import math
import webbrowser

import numpy as np
from lexer import Lexer
import Datatypes

def leet(message):
    char_mapping = {
        'a': '4', 'c': '(', 'd': '|)', 'e': '3',
        'f': 'ph', 'h': '|-|', 'i': '1', 'k': ']<',
        'o': '0', 's': '$', 't': '7', 'u': '|_|',
        'v': '\\/'}
    leetspeak = ''
    for char in message:  # Check each character:
        if char.lower() in char_mapping:
            leetspeak += char_mapping[char.lower()]
        else:
            leetspeak += char
    return Datatypes.String(leetspeak)

def midnight(*args):
    a, b, c = args
    sol = []
    if a == 0 and b == 0:
        return []
    elif a == 0:
        return [(-c) / b]
    try:
        x1 = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        sol.append(Datatypes.Number(x1))
        x2 = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        if x1 != x2:
            sol.append(Datatypes.Number(x2))
    except ValueError:
        pass
    return Datatypes.Array(sol)

def rick():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

def openURL(url):
    webbrowser.open(url)

def abs(value):
    return Datatypes.Number(math.fabs(value))

def input():
    return Datatypes.String(builtins.input())

def asString(object):
    return Datatypes.String(object)

def asNum(object):
    return Datatypes.Number(object)

def size(obj):
    return Datatypes.Number(len(obj))

def range(*args):
    return Datatypes.Array(list(np.arange(*args)))

def quit():
    exit()

def type(obj):
    return Datatypes.String(builtins.type(obj).__name__)

def asArr(obj):
    return Datatypes.Array(list(obj))

def arrOf(*args):
    return Datatypes.Array([*args])
    
def bool(obj):
    return Datatypes.Bool(obj)

def divMod(*args):
    return Datatypes.Array(list(builtins.divmod(*args)))

def change(*args):
    oxy_element = Datatypes.OXYGEN_DICT.get(args[0])
    if oxy_element is not None:
        Datatypes.OXYGEN_DICT[args[1]] = oxy_element
        del Datatypes.OXYGEN_DICT[args[0]]
    else:
        raise RuntimeError(f"Did not find any keyword or operator {args[0]}")

def macro(*args):
    Datatypes.MACROS.append([Lexer(args[0]).gen_tokens(include_macros=False),
                            Lexer(args[1]).gen_tokens(include_macros=False)])

def repr(obj):
    return Datatypes.String(builtins.repr(obj))

def fill(*args):
    return Datatypes.Array(list(np.full((1, args[1]), args[0])[0]))
