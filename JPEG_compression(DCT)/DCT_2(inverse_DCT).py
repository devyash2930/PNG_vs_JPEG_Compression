import cv2
import numpy as np
import math
from tkinter.filedialog import*
from zigzag import *

def multiply(mat1):
    QUANTIZATION_MAT = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                 [12, 12, 14, 19, 26, 58, 60, 55],
                                 [14, 13, 16, 24, 40, 57, 69, 56],
                                 [14, 17, 22, 29, 51, 87, 80, 62],
                                 [18, 22, 37, 56, 68, 109, 103, 77],
                                 [24, 35, 55, 64, 81, 104, 113, 92],
                                 [49, 64, 78, 87, 103, 121, 120, 101],
                                 [72, 92, 95, 98, 112, 100, 103, 99]])
    result = np.zeros(shape=(8,8))
    for r in range(8):
        for c in range(8):
            result[r][c] = mat1[r][c] * QUANTIZATION_MAT[r][c]
    return result

# defining block size
block_size = 8

# Reading image.txt to decode it as image
with open('image.txt', 'r') as myfile:
    image = myfile.read()

imgData = image.split()     # splits text data into space separated characters

# getting height and width of image
h = int(''.join(filter(str.isdigit, imgData[0])))
w = int(''.join(filter(str.isdigit, imgData[1])))


# construct array of zeros to perform further operations
array = np.zeros(h*w).astype(int)

k = 0
i = 2
j = 0

# transferring the data of image.txt to array

while k < array.shape[0]:

    if(imgData[i] == ';'):
        break

    # checking if the data is negative because sometimes DCT results negative
    if "-" not in imgData[i]:
        array[k] = int(''.join(filter(str.isdigit, imgData[i])))
    else:
        array[k] = -1*int(''.join(filter(str.isdigit, imgData[i])))

    if(i+3 < len(imgData)):
        j = int(''.join(filter(str.isdigit, imgData[i+3])))

    if j == 0:
        k = k + 1
    else:
        k = k + j + 1

    i = i + 2

array = np.reshape(array,(h,w))

i = 0
j = 0
k = 0

# initializing array for constructing compressed image
paddedImg = np.zeros((h, w))

while i < h:
    j = 0
    while j < w:

        # step 1: Iterating whole image data(or pixels) by taking 64 values at a time
        temp_string = array[i:i+8, j:j+8]

        # step 2: performing inverse zigzag to convert 1x64 matrix to 8x8 blocks
        block = inverse_zigzag(temp_string.flatten(), int(block_size),int(block_size))

        # step 3: performing dequantization
        de_quantized = multiply(block)

        # step 4: performing inverse 2D DCT to each 8x8 blocks
        paddedImg[i:i+8, j:j+8] = cv2.idct(de_quantized)

        j = j + 8
    i = i + 8

# to keep values in 8-bit (i.e. 0  to 255)
paddedImg[paddedImg > 255] = 255
paddedImg[paddedImg < 0] = 0


# saving compressed image
#savepath = asksaveasfilename()
cv2.imwrite('compressedImage.jpg', np.uint8(paddedImg))
