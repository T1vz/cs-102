import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    if (shift > 35):
        shift= shift % 35
    enF=65
    enL=90
    enf=97
    enl=122
    for i in range (len(plaintext)):
        if (ord(plaintext[i]) >= enF and ord(plaintext[i]) <= enL ):
            char= ord(plaintext[i]) + shift
            if (char > enL):
                char=enF+char-enL-1
            ciphertext+=chr(char)
        elif (ord(plaintext[i]) >= enf and ord(plaintext[i]) <= enl ):
            char= ord(plaintext[i]) + shift
            if (char > enl):
                char=enf+char-enl-1
            ciphertext+=chr(char)
        else:
            ciphertext+=plaintext[i]
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    if (shift > 35):
        shift= shift % 35
    enF=65
    enL=90
    enf=97
    enl=122
    for i in range (len(ciphertext)):
        if (ord(ciphertext[i]) >= enF and ord(ciphertext[i]) <= enL ):
            char= ord(ciphertext[i]) - shift
            if (char < enF):
                char=enL-enF+char+1
            plaintext+=chr(char)
        elif (ord(ciphertext[i]) >= enf and ord(ciphertext[i]) <= enl ):
            char= ord(ciphertext[i]) - shift
            if (char < enf):
                char=enl-enf+char+1
            plaintext+=chr(char)
        else:
            plaintext+=ciphertext[i]
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
