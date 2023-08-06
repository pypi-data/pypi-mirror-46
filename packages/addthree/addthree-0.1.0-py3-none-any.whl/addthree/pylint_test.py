"""
necessary docstring
"""
from string import ascii_letters, punctuation, digits

SHIFT = 3
CHOICE = "hello"
WORD = "please"
LETTERS = ascii_letters + punctuation + digits
ENCODED = ''

if CHOICE == "encode":
    for letter in WORD:
        if letter == '':
            ENCODED = ENCODED + ' '
        else:
            x = LETTERS.index(letter) + SHIFT
            ENCODED = ENCODED + LETTERS[x]

if CHOICE == "decode":
    for letter in WORD:
        if letter == ' ':
            ENCODED = ENCODED + ' '
        else:
            x = LETTERS.index(letter) - SHIFT
            ENCODED = ENCODED + LETTERS[x]
            print(ENCODED)

def hello(name):
    """
    function docstring
    """
    print(name)
