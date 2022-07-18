import random
import eccoperations as ec
import matrixoperations as mx
import pixelextraction as px
from matplotlib import pyplot as plt
import numpy as np
import skimage.color
import skimage.io

#declaring the parameters of the elliptic curve function: E: y^2=x^3+x+3 mod 31
a=1
b=3
p=31
G=(1,6) #Generator points
#step 1 of encryption process: Key Generation
def Key_generation():
    # PRIVATE KEY:choosing a private key PriKey_Self belonging to the range [1,p-1]
    #PriKey_Self=random.randint(1,p-1)
    PriKey_Self = 13
    # Computing the public key of user :PubKey_Self
    PubKey_Self = ec.double_and_add(PriKey_Self, G, p, a)
    # computing the initial Key:initial_key_Ki
    PubKey_Opp = (24,5)
    initial_key_Ki = ec.double_and_add(PriKey_Self, PubKey_Opp, p, a)
    # computation of self invertible matrix
    self_invertible_Matrix = mx.inverse_key_formation(initial_key_Ki, a, b, p, G)
    return self_invertible_Matrix


#Encrypting the pixel values
def encrypt_to_cipher(keymat,pixel_Matrix):
    L = []
    for i in range(256):
        for j in range(0, 256, 4):
            temp0 = []
            temp1 = pixel_Matrix[i]  # getting the first row of the key matrix
            temp2 = temp1[j:j + 4]  # creating an array containing four consecutive elements
            temp0.append(temp2)  # to create a 2D array
            temp3 = mx.transpose(temp0)  # transpose function to create a [4x1] matrix to multiply it with key matrix
            encrpart = mx.matrix_multiplication(keymat, temp3)
            for k in encrpart:
                ele = k[0] % 256
                L.append(ele)
    encrypted_values = []
    for a in range(0, len(L), 256):
        temp4 = []
        for b in range(a, a + 256):
            temp4.append(L[b])
        encrypted_values.append(temp4)
    return encrypted_values


#calling the functions
keymat=Key_generation()
pixel_Matrix=px.pixval()
ciphered_image_pixels=encrypt_to_cipher(keymat,pixel_Matrix)
