import numpy as np
def inverse(a, b):
    g, x, y = EEA(a,b)
    if g!=1 :
        return None
    else:
        return x % b

def EEA(a,b):
    r0, r = a, b
    x0, x = 1, 0
    y0, y = 0,1

    while r!= 0:
        q = r0 // r
        r0, r = r, r0 % r
        x0, x = x, x0 - q * x
        y0, y = y, y0 - q * y
    
    return r0, x0, y0

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

def matInv(keyMat):
    """Calculate the inverse of the key matrix."""
    det = int(round(np.linalg.det(keyMat)))  # Round to avoid floating point issues
    det_inv = inverse(det, 26)

    if det == 0 or inverse(det, 26) is None:
        raise ValueError("Key matrix is not invertible modulo 26")
    
    adjoint = np.round(det * np.linalg.inv(keyMat)).astype(int) % 26
    inv_mat = (det_inv * adjoint) % 26
    return inv_mat

def genCipherTextMat(cipherText, n, ch):
    """Generate ciphertext matrix with row or column convention."""
    cipherTextIndex = text_to_num(cipherText)

    if ch == 1:  # Row-wise
        rows = len(cipherTextIndex) // n
        return np.array(cipherTextIndex).reshape(rows, n)
    else:  # Column-wise
        cols = len(cipherTextIndex) // n
        return np.array(cipherTextIndex).reshape(cols, n).T  # Transpose
    
def decryption(A, B):
    """Perform matrix multiplication and modulo 26 operation for decryption."""
    result = A @ B % 26
    return result

n = int(input("Enter the size of matrix (n x n): "))
key = input("Enter the key for decryption: ")
cipherText = input("Enter the ciphertext: ")
keymat = keyMatGen(key, n)
InvKey = matInv(keymat)
ch = int(input("Enter 1 for row convention and any other number for column: "))
cipherTextMat = genCipherTextMat(cipherText, n, ch)
print("Ciphertext Matrix:\n", cipherTextMat)
if ch == 1:
    plainTextMat = decryption(cipherTextMat, InvKey)
    plainText = num_to_text(plainTextMat.flatten())
else:
    plainTextMat = decryption(InvKey, cipherTextMat)
    plainText = num_to_text(plainTextMat.flatten('F'))
print("Cipher Matrix: ", cipherTextMat)
print("Plaintext Matrix:\n", plainTextMat)
print("Plaintext:", plainText)