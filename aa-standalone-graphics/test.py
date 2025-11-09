from PIL import Image

im = Image.open("Reddit_Logo_Icon.svg-removebg-preview.png")

data = []
for (r,g,b,a) in im.getdata():
    if a > 100:
        data.append((255,255,255,0)) # 255,255,255,a
    else:
        data.append((255,255,255,255-a))

im.putdata(data)
im.save("reddit-circle.png")