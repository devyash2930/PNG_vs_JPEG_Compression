#Importing required libraries.
import PIL
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import struct

#Taking image name input from user and readng it.
Image_var = input("Enter the name of image to be compressed.\n")
im = imread(Image_var + '.tiff')

#Creating a file that stores pixel values of given image and opening it as an object.
input_file = (Image_var + 'p_val_file.txt')
textfile = open(input_file, "w")

#Getting a tuple of dimensions of image.
x = im.shape
#print(m,n) #Optional // Uncomment to display dimensions of image.

#Saving pixel values of image to a file.
for i in range(0,x[0]):
    for j in range(0,x[1]): 
        textfile.write(str(im[i, j]) + " ")
    textfile.write("\n")
textfile.close()

#Reopening the file and reading.
file = open(input_file)                 
data = file.read()

#Deleting data which is not needed now. 
del im

#Defining variables needed for LZW
max_size = pow(2, int(4096))
dict_size = 256

#Creating initial dictionary
dictionary = {chr(i): i for i in range(dict_size)}

#Iterating the whole data through a loop and making the lZW table.
#Implementing LZW Compression algorithm.
st = ""
c_data = []
for sym in data:
    st_p_sym = st + sym
    if st_p_sym in dictionary:
        st = st_p_sym
    else:
        c_data.append(dictionary[st])
        if(len(dictionary) <= max_size):
            dictionary[st_p_sym] = dict_size
            dict_size += 1
        st = sym
if st in dictionary:
    c_data.append(dictionary[st])

#Saving the encoded data to a file with .lzw format.
out = input_file.split(".")[0]
output_file = open("comp.lzw", "wb")
for data in c_data:
    output_file.write(struct.pack('>i',int(data)))#Interpret bytes as packed binary data.
#------------------------------------------------------------------------------------------------------------------

#Uncomment to see what encoded data without being packed as binary data looks like.
# textfile = open("n_file.txt", "w")
# for element in c_data:
#     textfile.write(str(element) + "\n")
# textfile.close()