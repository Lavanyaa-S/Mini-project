from matplotlib import pyplot as plt
import encryption1 as enc
import eccoperations as ec
import matrixoperations as mx
import pixelextraction as px
import numpy as np
import skimage.color
import skimage.io
import math

#declaring the parameters of the elliptic curve function: E: y^2=x^3+x+3 mod 31
a=1
b=3
p=31
G=(1,6) #Generator points

#step 1 of encryption process: Key Generation
def keys_generation_d():
    # PRIVATE KEY:choosing a private key PriKey_Self belonging to the range [1,p-1]
    #PriKey_Self=random.randint(1,p-1)
    PriKey_Self = 17
    # To illustrate and use to match the value in paper.
    print("private key:", PriKey_Self)
    # Computing the public key of user :PubKey_Self
    PubKey_Self = ec.double_and_add(PriKey_Self, G, p, a)
    print("Public key of Self:", PubKey_Self)
    # computing the initial Key:initial_key_Ki
    t = input("Enter the public key of opponent:")
    #compute the public key
    PubKey_Opp = tuple(int(x) for x in t.split())
    initial_key_Ki = ec.double_and_add(PriKey_Self, PubKey_Opp, p, a)
    print("Initial key Of A: ", initial_key_Ki)
    # computation of self invertible matrix
    self_invertible_Matrix = mx.inverse_key_formation(initial_key_Ki, a, b, p, G)
    return self_invertible_Matrix


#Encrypting the pixel values
def decrypt_to_original(keymat1,ciphered_image_pixels):
    L = []
    for i in range(256):
        for j in range(0, 256, 4):
            temp0 = []
            temp1 = ciphered_image_pixels[i]  # getting the first row of the key matrix
            temp2 = temp1[j:j + 4]  # creating an array containing four consecutive elements
            temp0.append(temp2)  # to create a 2D array
            temp3 = mx.transpose(temp0)  # transpose function to create a [4x1] matrix to multiply it with key matrix
            encrpart = mx.matrix_multiplication(keymat1, temp3)
            for k in encrpart:
                ele = k[0] % 256
                L.append(ele)
    decrypted_values = []
    for a in range(0, len(L), 256):
        temp4 = []
        for b in range(a, a + 256):
            temp4.append(L[b])
        decrypted_values.append(temp4)
    print("pixel values after decryption process:")
    for row in decrypted_values:
        print(' '.join('{:3}'.format(value) for value in row))
    return decrypted_values

#display of images
def image_display(decrypted_image_pixels):
    # Original image
    plt.rcParams["figure.figsize"] = [7.00, 4.50]
    plt.rcParams["figure.autolayout"] = True
    data1 = enc.pixel_Matrix
    plt.subplot(1, 3, 1)
    plt.title("Original image")
    plt.imshow(data1, cmap="gray")

    # ciphered image
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2 = enc.ciphered_image_pixels
    plt.subplot(1, 3, 2)
    plt.title("Ciphered image")
    plt.imshow(data2, cmap="gray")

    # Deciphered image
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data3 = decrypted_image_pixels
    plt.subplot(1, 3, 3)
    plt.title("Deciphered image")
    plt.imshow(data1, cmap="gray")

    plt.show()


def histogram_image(pixel_Matrix,ciphered_image_pixels,decrypted_image_pixels):
    histogram1, bin_edges = np.histogram(pixel_Matrix, bins=256, range=(0, 256))
    histogram2, bin_edges = np.histogram(ciphered_image_pixels, bins=256, range=(0, 256))
    histogram3, bin_edges = np.histogram(decrypted_image_pixels, bins=256, range=(0, 256))

    plt.subplot(1, 3, 1)  # row 1, col 2 index 1
    plt.title("Original image Histogram")
    plt.xlabel("grayscale value")
    plt.ylabel("pixel count")
    plt.xlim([0.0, 256.0])
    plt.plot(bin_edges[0:-1], histogram1)

    plt.subplot(1, 3, 2)  # index 2
    plt.title("Ciphered image Histogram")
    plt.xlabel("grayscale value")
    plt.ylabel("pixel count")
    plt.xlim([0.0, 256.0])
    plt.plot(bin_edges[0:-1], histogram2)

    plt.subplot(1, 3, 3)  # index 2
    plt.title("Decrypted image Histogram")
    plt.xlabel("grayscale value")
    plt.ylabel("pixel count")
    plt.xlim([0.0, 256.0])
    plt.plot(bin_edges[0:-1], histogram3)
    plt.show()

def entropycalc(ciphered_image_pixels):
    countofpixel=[]
    for i in range(256):
        countofpixel.append(0)
    for a in range(256):
        for b in range(256):
            ind=ciphered_image_pixels[a][b]
            countofpixel[ind]+=1
    entropy=0
    for x in countofpixel:
        if x==0:
            x+=1
        p_of_x=(x/65536)
        ele=(1/p_of_x)
        log_of_p=math.log(ele,2)
        prod=(p_of_x * log_of_p)
        entropy+=prod
    return entropy

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def uaci(pixel1,pixel2):
    value=0.0
    for x in range(0,256):
        for y in range(0,256):
            value=(abs(pixel1[x][y]-pixel2[x][y])/255)+value

    value=(value/(256*256))*100
    return value

#calling the functions
keymat1=keys_generation_d()
print(np.array(keymat1))
pixel_Matrix=px.pixval()
ciphered_image_pixels=enc.ciphered_image_pixels
decrypted_image_pixels=decrypt_to_original(keymat1,ciphered_image_pixels)
image_display(decrypted_image_pixels)
histogram_image(pixel_Matrix,ciphered_image_pixels,decrypted_image_pixels)
entropy=entropycalc(ciphered_image_pixels)
psnr_value=PSNR(np.array(pixel_Matrix), np.array(decrypted_image_pixels))
uaci_value=uaci(np.array(pixel_Matrix), np.array(ciphered_image_pixels))
print("Entropy of the image from our project:",entropy)
print("PSNR of the image from our project:",psnr_value)
print("UACI of the image from our project:",uaci_value)
