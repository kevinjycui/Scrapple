mappings = {
    'CH': 'K',
    'LL': 'W',
    'RR': 'Ŕ'
}

def serialize(word):
    for m, s in mappings.items():
        word = word.replace(m, s).replace(m.lower(), s.lower())
    return word

def deserialize(word):
    for m, s in mappings.items():
        word = word.replace(s, m).replace(s.lower(), m.lower())
    return word