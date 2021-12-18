#Importing required libraries.
import PIL
from skimage.io import imread
import numpy
import cv2
import struct
from io import StringIO

#taking the compressed file data in a variable.
input_file = 'comp.lzw'
file = open(input_file, "rb")

#Taking image name input from user and readng it.
Image_var = input("Enter the name of image to be compressed.\n")
im = imread(Image_var + '.tiff')

#Getting a tuple of dimensions of image.
x = im.shape

#Initializing some variables for decoding
max_size = pow(2, int(4096))
c_data = []
next_code = 256
d_data = ""
st = ""

# Reading the compressed file.
#Taking 4 values as a time as we have taken 4-bit packing to binary data.
while True:
    rec = file.read(4)
    if len(rec) != 4:
        break
    (data, ) = struct.unpack('>i', rec)
    c_data.append(data)

# Building and initializing the dictionary.
dict_size = 256
dictionary = {i: chr(i) for i in range(dict_size)}

#Iterating through all the codes.
#Implementing LZW Decompression algorithm.
for coded_val in c_data:
    if not (coded_val in dictionary):
        dictionary[coded_val] = st + (st[0])
    d_data += dictionary[coded_val]
    if not(len(st) == 0):
        dictionary[next_code] = st + (dictionary[coded_val][0])
        next_code += 1
    st = dictionary[coded_val]


#------------------------------------------------------------------------------------------------------------------------------------

#Writing decoded data in a file.
out = input_file.split(".")[0]
output_file = open(out + "_decoded.txt", "w")
for data in d_data:
    output_file.write(data)    
output_file.close()
file.close()


#--------------------------------------------------------------------------------------------------------------------------------------

#Opening file of decoded data.
with open('comp_decoded.txt') as f:
    lines = f.readlines()

#Converting the values from string to float for reconstructing the image.
data = []
for line in lines:
    tmp, t = [], line.split(' ')
    # print(type(t), t)
    for i in range(len(t)-1):
        tmp.append(float(t[i]))
    data.append(tmp)

#Deleting unnecessary data to reduce memory usage.
del lines, tmp

#Reconstructing image using decoded image pixel values.
data = numpy.asarray(data)
cv2.imwrite('output.png', data)