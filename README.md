# PNG_vs_JPEG_Compression

For PNG Compression:

Implementation of image compression using LZW has been implemented.

Working : 

1. encoderv4.py reads an image and performs LZW on it. Name of the image file has been asked to the user and it should be without extension.

2. comp.lzw file is created which is the encoded pixel values of the given input image.

3. decodedv4.py reads the encoded file, decodes it and recreates the image using pixel values.

4. output.png is the compressed output image file and it can be clearly seen that its size is less than the input file.

For JPEG compression:

Implementation of image compression using DCT has been implemented.

Working:

1. DCT_1(DCT).py reads an image and performs DCT, applies quantization and encodes it by run length encoding.

2. Encoded image file will be poped up after running the above file.

3. image.txt file will be created by encoding.
 
4. DCT_2(inverse_DCT) reads the encoded file, performs inverse DCT, applies dequantization, decodes it and recreates the image using decoded image pixel values.

5. Final file name will be "user file name+_compressedImage.jpg".

6. In the final output file image has block-artifacts which are visible.


Youtube video link:-
https://www.youtube.com/watch?v=Kj-U2hxwBtM
