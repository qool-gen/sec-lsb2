
from PIL import Image, ImageChops
import math
delimiter = '###'

def text2binary(data):
    data_binary = []
    for i in data:
        data_binary.append(format(ord(i), '08b'))
    data_binary = ''.join(data_binary)
    return data_binary

def pixel2binary(pixel):
    pixel_binary = []
    for i in range(3):
        pixel_binary.append(bin(pixel[i])[2:].zfill(8))
    return pixel_binary

def binary2pixel(pixel_binary):
    pixel = []
    for i in range(3):
        pixel.append(int(pixel_binary[i],2))
    return pixel

def encode_pixel_binary(pixel_binary, data_binary):
    for i in range(len(data_binary)):
        px = list(pixel_binary[i])
        px[-1] = data_binary[i]
        pixel_binary[i] = ''.join(px)
    return pixel_binary
    
    
def encode(filename, data, filename_secret):
    print('\n---ENCODE---\n')
    
    data_binary = text2binary(data)
    data_len = len(data_binary)
    total_pixel_req = int(math.ceil(float(data_len)/3))
    img = Image.open(filename)
    width, height = img.size
    pixels = list(img.getdata())
    pixels_binary = []
    pixels_new = []
    
    print('data                 = {}'.format(data))
    print('data_binary          = {}'.format(data_binary))
    print('                     = ',end='')
    for i in range(len(data_binary)):
        print(data_binary[i],end='')
        if (i+1)%3 == 0:
            print(' ',end='')
    print('')
    print('data_binary_len      = {}'.format(data_len))
    print('img_size             = {}'.format(img.size))
    print('total_pixel          = {} = {}x{}'.format(img.size[0]*img.size[1], img.size[0], img.size[1]))
    print('total_pixel_required = {} = {}\n'.format(total_pixel_req,'data_binary_len/3'))
    
    for i in range(total_pixel_req):
			
        pixel_binary = pixel2binary(pixels[i])
            
        start = i*3
        stop = (i+1)*3
        data_binary_3bit = data_binary[start:stop]
            
        pixel_binary_old = pixel_binary.copy()
        pixel_binary = encode_pixel_binary(pixel_binary.copy(), data_binary_3bit)
        pixel_new = binary2pixel(pixel_binary)
        pixel_new.append(255)
        pixel_new = tuple(pixel_new)
            
        print('PIXEL {}'.format(i+1))
        print('pixel        = {}'.format(pixels[i]))
        print('pixel_binary = {}'.format(pixel_binary_old))
        print('data_binary  = {}'.format(data_binary_3bit))
        print('pixel_binary = {}'.format(pixel_binary))
        print('pixel        = {}'.format(pixel_new))
        print('')
        
        pixels_new.append(pixel_new)
    
    #update 
    for i in range(len(pixels_new)):
        #print(pixels[i],' vs ',pixels_new[i])
        pixels[i] = tuple(pixels_new[i])
    print('')
    
    img.putdata(pixels)
    img.save(filename_secret)   
    img.close()
        

def decode(filename_secret):
    print('\n---DECODE---\n')
    img = Image.open(filename_secret)
    pixels = list(img.getdata())
    
    data_binary_all = []
    for i in range(len(pixels)):
        pixel_binary = pixel2binary(pixels[i])
        #print(pixel_binary)
        for j in range(3):
            last_bit = pixel_binary[j][-1] 
            data_binary_all.append(last_bit)
    
    loop = int(len(data_binary_all)/8)
    data = []
    for k in range(loop):
        start = k*8
        stop = (k+1)*8
        data_binary = ''.join(data_binary_all[start:stop])
        #print(data_binary)
        txt = chr(int(data_binary,2))
        #print(txt)
        data.append(txt)
        
        if ''.join(data).endswith(delimiter):
            break
        
        if start > len(data_binary_all):
            break
    
    data = ''.join(data)
    print('data                 = {}'.format(data))
    
data = 'hi###'
print(data)

data_binary = text2binary(data)
print(data_binary,' ',len(data_binary),'\n')

filename = 'cat.png'
filename_secret = 'cat_secret.png'
encode(filename, data, filename_secret)

decode(filename_secret)

