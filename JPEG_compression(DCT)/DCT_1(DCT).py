import cv2
import numpy as np
import math
from tkinter.filedialog import*
# import zigzag functions
from zigzag import *


def Quintize(DCT_MAT):
    # Quantization Matrix
    # Here we have used default quantization table of JPEG which is also known as Luminance Quantization Table
    QUANTIZATION_MAT = np.array(
        [[16, 11, 10, 16, 24, 40, 51, 61],
         [12, 12, 14, 19, 26, 58, 60, 55],
         [14, 13, 16, 24, 40, 57, 69, 56],
         [14, 17, 22, 29, 51, 87, 80, 62],
         [18, 22, 37, 56, 68, 109, 103, 77],
         [24, 35, 55, 64, 81, 104, 113, 92],
         [49, 64, 78, 87, 103, 121, 120, 101],
         [72, 92, 95, 98, 112, 100, 103, 99]])
    Array_DCT = np.zeros(shape=(8, 8))
    # performing Quantization
    for k in range(8):
        for l in range(8):
            Array_DCT[k][l] = int(DCT[k][l] / QUANTIZATION_MAT[k][l])
    return Array_DCT

def get_run_length_encoding(image):
    string = []
    i = 0
    sk = 0     # in order to skip zeros and store number of zeros

    bitstring = ""
    image = image.astype(int)
    print("Image_Shape is hear::")
    print(image.shape[0])
    while i < image.shape[0]:
        if image[i] != 0:
            string.append((image[i], sk))
            bitstring = bitstring + str(image[i]) + " " + str(sk) + " "
            sk = 0
        else:
            sk = sk + 1
        i = i + 1

    return bitstring


# defining block size
block_size = 8



filepath = askopenfilename()

image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)  # Reading the image in grayscale
#image_save2 = cv2.imwrite('Grayscale_Image.jpg',image) # Saving the Grayscale image file into our folder



[h, w] = image.shape    # getting dimensions of the image i.e height and width

height = h      # Original height of the matrix
width = w       # Original width of the matrix


h = np.float32(h)   # Converting height to get precision for 32bit number
w = np.float32(w)   # Converting width to get precision for 32bit number

# Dividing the total height and width to form a matrix of 8x8 submatrix
bh = math.ceil(h / block_size)     # bh = no. of blocks needed along height
bh = np.int32(bh)

bw = math.ceil(w / block_size)      # bh = no. of blocks needed along width
bw = np.int32(bw)


# Padding the image with zeros, so even if the image dimensions are not divisible by block size, they become divisible.

H = block_size * bh     # height of padded image

W = block_size * bw     # width of padded image

# creating a zero matrix of size of H,W
paddedImg = np.zeros((H, W))

# copying the values of img into paddedImg[0:h,0:w]
for i in range(height):
        for j in range(width):
                pixel = image[i,j]
                paddedImg[i,j] = pixel

cv2.imwrite('uncompressed.jpg', np.uint8(paddedImg))   # saving the padded image before compression


# Encoding
# step 1: Divide the image into 8x8 blocks
# step 2: apply 2D Discrete Cosine Transform(DCT) to each divided blocks
# step 3: perform quantization on each block
# step 4: perform zigzag scan to reorder the resultant blocks (i.e here each 8x8 matrix is reordered to 1x64 matrix)
# step 5: reshape each 1x64 matrix to 8x8 blocks to form and observe encoded image

for i in range(bh):

    # starting and ending row index of block
    rowIndex1 = i * block_size
    rowIndex2 = rowIndex1 + block_size

    for j in range(bw):
        # starting and ending column index of block
        col_ind_1 = j * block_size
        col_ind_2 = col_ind_1 + block_size

        # step 1: Divide the image into 8x8 blocks
        block = paddedImg[rowIndex1: rowIndex2, col_ind_1: col_ind_2]

        # step 2: apply 2D Discrete Cosine Transform(DCT) to each divided blocks
        DCT = cv2.dct(block)
        # print()
        # print(DCT)
        # print()
        # step 3: performing Quantization on each block

        # performing Quantization
        DCT_normalized = Quintize(DCT)

        # print(DCT_normalized.shape)
        # step 4: perform zigzag scan to reorder the resultant blocks (i.e here each 8x8 matrix is reordered to 1x64 matrix)
        reordered = zigzag(DCT_normalized)

        # step 5: reshape each 1x64 matrix to 8x8 blocks to form and observe encoded image
        reshaped = np.reshape(reordered, (block_size, block_size))

        # copy reshaped matrix into paddedImg on current block
        paddedImg[rowIndex1: rowIndex2, col_ind_1: col_ind_2] = reshaped


cv2.imshow('encoded image', np.uint8(paddedImg))

arranged = paddedImg.flatten()

# performing Run length Encoding to skip the repeating zeros and storing encoded data in text file

bitstring = get_run_length_encoding(arranged)

# padddedImg.shape[0] and paddedImg.shape[1] are dimensions of image and semicolon denotes the end of file
bitstring = str(paddedImg.shape[0]) + " " + str(paddedImg.shape[1]) + " " + bitstring + ";"

# Writing image to image.txt
imgFile = open("image.txt", "w")
imgFile.write(bitstring)
imgFile.close()

cv2.waitKey(0)
cv2.destroyAllWindows()