import Datatypes
import math

def leet(message):
    charMapping = {
    'a': '4', 'c': '(', 'd': '|)', 'e': '3',
    'f': 'ph', 'h': '|-|', 'i': '1', 'k': ']<',
    'o': '0', 's': '$', 't': '7', 'u': '|_|',
    'v': '\\/'}
    leetspeak = ''
    for char in message:  # Check each character:
        if char.lower() in charMapping:
            leetspeak += charMapping[char.lower()]
        else:
            leetspeak += char
    return Datatypes.String(leetspeak)

def midnight(a,b,c):
    sol = []
    if a == 0 and b == 0:
        return []
    elif a == 0:
        return [(-c)/b]      
    try:
        x1 = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
        sol.append(x1)
        x2 = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
        if(x1 != x2):
            sol.append(x2)
    except ValueError:
        pass
    return Datatypes.Array(sol)