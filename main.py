from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

window = Tk()
window.title("Billede Steganografi")
window.geometry('700x630')
path = "Image.png"
image = ImageTk.PhotoImage(Image.open(path))
image_width = 350

image_label = Label(window, height = 400, width = 0, image = image)
image_label.place(x = 350, y = 300, anchor = "center")

text = Entry(window, width = 30)
text.place(x = 140, y = 560)

text_2 = Label(window, text = "")
text_2.place(x = 370, y = 560)

# Åbner stifinder for at vælge et billede
def open_button():
    global path
    path = filedialog.askopenfilename()
    path2 = Image.open(path)
    wpercent = (image_width / float(path2.size[0]))
    hsize = int((float(path2.size[1]) * float(wpercent)))
    path2 = path2.resize((image_width, hsize), Image.ANTIALIAS)
    path2 = ImageTk.PhotoImage(path2)
    image_label.configure(image = path2)
    image_label.image = path2


# Gem billedet oven på det gamle
def save_button():
    file = filedialog.asksaveasfilename()


# Decode beskeden i billedet
def decode():
    image_decode = Image.open(path, 'r')
    image_data = iter(image_decode.getdata())
    message = ""

    # Decode pixels beskeden bliver returneret
    while (True):
        pixels = [value for value in image_data.__next__()[:3] +
                  image_data.__next__()[:3] +
                  image_data.__next__()[:3]]

        # Optæl bits fra det sidste bit af hvert pixel
        binary_str = ""
        for i in pixels[:8]:
            if (i % 2 == 0):
                binary_str += '0'
            else:
                binary_str += '1'

        # Konverter fra binær til ASCII og gem
        message += binary_to_ASCII(binary_str)

        # Check om beskeden er slut
        if (pixels[-1] % 2 == 1):
            text_2.configure(text = message)
            return message


# Konverter et byte fra binær til ASCII
def binary_to_ASCII(binary):
    ASCII = chr(int(binary, 2))
    return ASCII


# Konverter beskeden fra ASCII til binær
def ASCII_to_binary(message):
    binary = []
    for i in message:
        binary.append(format(ord(i), '08b'))
    return binary


# Modificer pixels ud fra beskeden i binær og returnerer dem
def modify_pixels(pixel, message):
    binary_message = ASCII_to_binary(message)
    binary_message_len = len(binary_message)
    pixel_iterator = iter(pixel)

    # Gennemgå hvert symbol i beskeden
    for i in range(binary_message_len):

        # Udvælger et sæt af 3 pixels med 9 modificerbare bits
        pixel = [value for value in pixel_iterator.__next__()[:3] +
                 pixel_iterator.__next__()[:3] +
                 pixel_iterator.__next__()[:3]]

        # Gennemgå hvert bit af symbolet
        for j in range(0, 8):

            # Juster pixel værdi ud fra hvert bit
            if (binary_message[i][j] == '0') and (pixel[j] % 2 == 1):
                if (pixel[j] % 2 == 1):
                    pixel[j] -= 1
            elif (binary_message[i][j] == '1') and (pixel[j] % 2 == 0):
                pixel[j] -= 1

        # Brug det sidste bit i hvert sæt til at bestemme om decoderen skal læse videre
        if (i == binary_message_len - 1):
            if (pixel[-1] % 2 == 0):
                pixel[-1] -= 1
        elif (pixel[-1] % 2 != 0):
            pixel[-1] -= 1

        # Returner en pixel af gangen
        pixel = tuple(pixel)
        yield pixel[0:3]
        yield pixel[3:6]
        yield pixel[6:9]


def insert_pixels(image, message):
    image_width = image.size[0]
    (x, y) = (0, 0)

    # Gentag for hver modificeret pixel
    for pixel in modify_pixels(image.getdata(), message):

        # Indsæt modificeret pixels i det nye billede
        image.putpixel((x, y), pixel)

        # Vælg positionen af den næste pixel
        if (x == image_width - 1):
            x = 0
            y += 1
        else:
            x += 1


# Encode en besked i det valgte billede
def encode():
    image = Image.open(path, 'r')
    message = text.get()
    message_len = len(message)
    if (message_len == 0):
        raise ValueError("There is no message")

    insert_pixels(image, message)
    image.save(path)

    path3 = Image.open(path)
    wpercent = (image_width / float(path3.size[0]))
    hsize = int((float(path3.size[1]) * float(wpercent)))
    path3 = path3.resize((image_width, hsize), Image.ANTIALIAS)
    path3 = ImageTk.PhotoImage(path3)
    image_label.configure(image = path3)
    image_label.image = path3


lbl = Label(window, text = "Billede steganografi", font = ("Oswald", 35))
lbl.place(x = 350, y = 40, anchor = "center")

lbl2 = Label(window, text = "Indsæt tekst:")
lbl2.place(x = 140, y = 540)

lbl3 = Label(window, text = "Besked i billedet:")
lbl3.place(x = 370, y = 540)

btnOpen = Button(window, text = "Open", command = open_button)
btnOpen.place(x = 280, y = 70)

btnSave = Button(window, text = "Save", command = save_button)
btnSave.place(x = 360, y = 70)

btnEncode = Button(window, text = "Encode", command = encode)
btnEncode.place(x = 200, y = 510)

btnDecode = Button(window, text = "Decode", command = decode)
btnDecode.place(x = 430, y = 510)

window.mainloop()
