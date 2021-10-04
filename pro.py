from PIL import Image 

img = Image.open("me.jpg") 

size = w,h = img.size
data = img.load()



for x in range(w):
    for y in range(h):
        
        print ([bin (it)[2:].zfill(2).upper() for it in data[x,y]])
        