from tkinter import *
from tkinter import filedialog
import PIL
from PIL import ImageTk, Image

window = Tk()
window.title("Billede Steganografi")
window.geometry('700x630')

path = "Image.png"

mywidth = 350

img = ImageTk.PhotoImage(Image.open(path))

billede = Label(window, height=400, width=0, image = img)
billede.place(x=350, y=300, anchor="center")

txt = Entry(window,width=30)
txt.place(x=140, y=560)

lbl4 = Label(window, text="")
lbl4.place(x=370, y=560)

def openbtn():
    global path
    path = filedialog.askopenfilename()
    path2 = Image.open(path)
    wpercent = (mywidth / float(path2.size[0]))
    hsize = int((float(path2.size[1]) * float(wpercent)))
    path2 = path2.resize((mywidth, hsize), PIL.Image.ANTIALIAS)
    path2 = ImageTk.PhotoImage(path2)
    billede.configure(image=path2)
    billede.image = path2

def savebtn():
    file = filedialog.asksaveasfilename()

def decode():
    imgdecode = Image.open(path, 'r')

    data = ''
    imgdata = iter(imgdecode.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3]]
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def decodee():
    print(path)
    decodetext=(decode())
    lbl4.configure(text=decodetext)

def genData(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                if (pix[j] % 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        # Eigh^th pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode():
    imageencode = Image.open(path, 'r')

    data = txt.get()
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = imageencode.copy()
    encode_enc(newimg, data)

    newimg.save(path)

    path3 = Image.open(path)
    wpercent = (mywidth / float(path3.size[0]))
    hsize = int((float(path3.size[1]) * float(wpercent)))
    path3 = path3.resize((mywidth, hsize), PIL.Image.ANTIALIAS)
    path3 = ImageTk.PhotoImage(path3)
    billede.configure(image=path3)
    billede.image = path3

lbl = Label(window, text="Billede steganografi", font=("Oswald", 35))
lbl.place(x=350, y=40, anchor="center")

lbl2 = Label(window, text="Indsæt tekst:")
lbl2.place(x=140, y=540)

lbl3 = Label(window, text="Besked i billedet:")
lbl3.place(x=370, y=540)

btnOpen = Button(window, text="Open", command=openbtn)
btnOpen.place(x=280, y=70)

btnSave = Button(window, text="Save", command=savebtn)
btnSave.place(x=360, y=70)

btnEncode = Button(window, text="Encode", command=encode)
btnEncode.place(x=200, y=510)

btnDecode = Button(window, text="Decode", command=decodee)
btnDecode.place(x=430, y=510)

window.mainloop()
