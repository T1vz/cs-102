def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    enF=65
    enL=90
    enf=97
    enl=122
    needV=len(plaintext) - len(keyword)
    if (needV > 0):
        for i in range (needV):
            keyword+=keyword[i%needV]
    keyword=keyword.upper()
    for i in range (len(plaintext)):
        if (ord(plaintext[i]) >= enF and ord(plaintext[i]) <= enL ):
            shift = ord(keyword[i]) - 65
            char= ord(plaintext[i]) + shift
            if (char > enL):
                char=enF+char-enL-1
            ciphertext+=chr(char)
        elif (ord(plaintext[i]) >= enf and ord(plaintext[i]) <= enl ):
            shift = ord(keyword[i]) - 65
            char= ord(plaintext[i]) + shift
            if (char > enl):
                char=enf+char-enl-1
            ciphertext+=chr(char)
        else:
            ciphertext+=plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    enF=65
    enL=90
    enf=97
    enl=122
    needV=len(ciphertext) - len(keyword)
    if (needV > 0):
        for i in range (needV):
            keyword+=keyword[i%needV]
    keyword=keyword.upper()
    for i in range (len(ciphertext)):
        if (ord(ciphertext[i]) >= enF and ord(ciphertext[i]) <= enL ):
            shift = ord(keyword[i]) - 65
            char= ord(ciphertext[i]) - shift
            if (char < enF):
                char=enL-enF+char+1
            plaintext+=chr(char)
        elif (ord(ciphertext[i]) >= enf and ord(ciphertext[i]) <= enl ):
            shift = ord(keyword[i]) - 65
            char= ord(ciphertext[i]) - shift
            if (char < enf):
                char=enl-enf+char+1
            plaintext+=chr(char)
        else:
            plaintext+=ciphertext[i]
    return plaintext
