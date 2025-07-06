import numpy as np
def text_to_num(text):
    """Convert text to numbers (A=0, B=1, ..., Z=25)."""
    return [ord(char) - ord('A') for char in text]

def num_to_text(nums):
    """Convert numbers back to text."""
    return ''.join(chr(num + ord('A')) for num in nums)

def keyMatGen(key, n):
    """Generate key matrix of size n x n."""
    key = key.upper().replace(" ", "")
    key = (key * ((n * n) // len(key) + 1))[:n * n]  # Repeat key if needed
    keyIndex = text_to_num(key)
    return np.array(keyIndex).reshape(n, n)

def genPlainTextMat(plainText, n, ch):
    """Generate plaintext matrix with row or column convention."""
    plainText = plainText.upper().replace(" ", "")
    while len(plainText) % n != 0:
        plainText += 'Z'  # Padding for message that is not exactly divisible by the matrix size
    
    plainTextIndex = text_to_num(plainText)
    
    if ch == 1:
        rows = len(plainTextIndex) // n
        return np.array(plainTextIndex).reshape(rows, n)
    else:
        cols = len(plainTextIndex) // n
        return np.array(plainTextIndex).reshape(cols, n).T
    
def encryption(A, B):
    """Perform matrix multiplication and modulo 26 operation."""
    result = A @ B % 26
    return result

n = int(input("Enter the size of matrix (n x n): "))
key = input("Enter the key for encryption: ")
pt = input("Enter the message: ")
keymat = keyMatGen(key, n)
ch = (int(input("Enter 1 for row convention and any other number for column: ")))
ptmat = genPlainTextMat(pt, n, ch)

if ch == 1:
    cipherMat = encryption(ptmat, keymat)
    cipherText = num_to_text(cipherMat.flatten())
else:
    cipherMat = encryption(keymat, ptmat)
    cipherText = num_to_text(cipherMat.flatten('F'))
print("PlaintextMatrix: ", ptmat)
print("CiphertextMatrix: ", cipherMat)
print("Ciphertext:", cipherText)