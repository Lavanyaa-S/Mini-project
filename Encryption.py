from matplotlib import pyplot as plt
import random
import eccoperations as ec
import matrixoperations as mx
import pixelextraction as px
import numpy as np
import skimage.color
import skimage.io

#Declaring the parameters of the elliptic curve function: E: y^2=x^3+x+3 mod 31
a=1
b=3
p=31
G=(1,6) #Generator points.


#step 1 of encryption process: Key Generation
def Key_generation():
    # PRIVATE KEY:choosing a private key PriKey_Self belonging to the range [1,p-1]
    PriKey_Self = 13
    print("private key:", PriKey_Self)
    # Computing the public key of user :PubKey_Self
    PubKey_Self = ec.double_and_add(PriKey_Self, G, p, a)
    print("Public key of Self:", PubKey_Self)
    # computing the initial Key : initial_key_Ki
    t = input("Enter the public key of opponent:")
    #compute the public key
    PubKey_Opp = tuple(int(x) for x in t.split())
    initial_key_Ki = ec.double_and_add(PriKey_Self, PubKey_Opp, p, a)
    print("Initial key Of A: ", initial_key_Ki)
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
    print("pixel values after encryption process:")
    for row in encrypted_values:
        print(' '.join('{:3}'.format(value) for value in row))
    print("Images are as follows:")
    return encrypted_values


def histogram_image(pixel_Matrix,ciphered_image_pixels):
    histogram1, bin_edges = np.histogram(pixel_Matrix, bins=256, range=(0, 256))
    histogram2, bin_edges = np.histogram(ciphered_image_pixels, bins=256, range=(0, 256))

    plt.subplot(1, 2, 1)  # row 1, col 2 index 1
    plt.title("Original image Histogram")
    plt.xlabel("grayscale value")
    plt.ylabel("pixel count")
    plt.xlim([0.0, 256.0])  # <- named arguments do not work here
    plt.plot(bin_edges[0:-1], histogram1)

    plt.subplot(1, 2, 2)  # index 2
    plt.title("Ciphered image Histogram")
    plt.xlabel("grayscale value")
    plt.ylabel("pixel count")
    plt.xlim([0.0, 256.0])  # <- named arguments do not work here
    plt.plot(bin_edges[0:-1], histogram2)
    plt.show()


def image_display(pixel_Matrix,ciphered_image_pixels):
    # Original image
    plt.rcParams["figure.figsize"] = [7.00, 4.50]
    plt.rcParams["figure.autolayout"] = True
    data1 = pixel_Matrix
    plt.subplot(1, 2, 1)
    plt.title("Original image")
    plt.imshow(data1, cmap="gray")

    # ciphered image
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2 = ciphered_image_pixels
    plt.subplot(1, 2, 2)
    plt.title("Ciphered image")
    plt.imshow(data2, cmap="gray")
    plt.show()

#calling the functions
keymat=Key_generation()
print(np.array(keymat))
pixel_Matrix=px.pixval()
ciphered_image_pixels=encrypt_to_cipher(keymat,pixel_Matrix)
image_display(pixel_Matrix,ciphered_image_pixels)
histogram_image(pixel_Matrix,ciphered_image_pixels)
