from PIL import Image

im = Image.open("logos/sdp.png")

im2 = Image.open("logos/sd.png")
im2 = im2.resize((80,80))
print(im2.size)
data = []
for (r,g,b,a) in im.getdata():
    pass
    # print(r,g,b,a)
    # if a != 0:
    #     data.append((240,240,240,a))
    # else:
    #     data.append((r,g,b,a))

im.putdata(data)
im2.save("logos/sdp.png")
im2.show()