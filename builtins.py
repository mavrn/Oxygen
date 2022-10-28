import Datatypes

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