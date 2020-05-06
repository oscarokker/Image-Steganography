from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

window = Tk()
window.title("Billede Steganografi")
window.width = 700
window.height = 640
window.geometry("700x640")


class ImageSteganography:
    # Opstil klassens variabler
    def __init__(self):
        self.path = "Image.png"
        self.image = ImageTk.PhotoImage(Image.open(self.path))
        self.image_width = 360

        self.image_label = Label(window, height=400, width=0, image=self.image)
        self.image_label.place(x=window.width/2, y=320, anchor="center")

        self.entry_message = Entry(window, width=24)
        self.entry_message.place(x=140, y=588)

        self.text_encode_done = Label(window, text="", font=("Oswald", 10))
        self.text_encode_done.place(x=140, y=608)

        self.text_decoded_message = Label(window, text="", font=("Oswald", 10))
        self.text_decoded_message.place(x=400, y=588)

        self.text_open = Label(window, text="")
        self.text_open.place(x=220, y=104, anchor="center")

        self.text_save = Label(window, text="")
        self.text_save.place(x=480, y=104, anchor="center")

        static_text_1 = Label(window, text="Billede steganografi", font=("Oswald", 36))
        static_text_1.place(x=350, y=32, anchor="center")

        static_text_2 = Label(window, text="Indsæt besked:", font=("Oswald", 12))
        static_text_2.place(x=140, y=564)

        static_text_3 = Label(window, text="Beskeden i billedet:", font=("Oswald", 12))
        static_text_3.place(x=400, y=564)

        self.init_buttons()

    # Åbn stifinder for at vælge et billede
    def open_button(self):
        global path
        self.path = filedialog.askopenfilename()
        path2 = Image.open(self.path)
        wpercent = (self.image_width / float(path2.size[0]))
        hsize = int((float(path2.size[1]) * float(wpercent)))
        path2 = path2.resize((self.image_width, hsize), Image.ANTIALIAS)
        path2 = ImageTk.PhotoImage(path2)
        self.image_label.configure(image=path2)
        self.image_label.image = path2
        self.text_open.configure(text="Billede hentet")

    # Gem billedet oven på det gamle
    def save_button(self):
        filedialog.asksaveasfilename()
        self.text_save.configure(text="Billede gemt")

    # Decode beskeden i billedet
    def decode(self):
        image_decode = Image.open(self.path, 'r')
        image_data = iter(image_decode.getdata())
        message = ""

        # Gentag indtil beskeden kan blive retuneret
        while True:
            pixels = [value for value in image_data.__next__()[:3] +
                      image_data.__next__()[:3] +
                      image_data.__next__()[:3]]

            # Optæl det sidste bit af hver pixelværdi
            binary_str = ""
            for i in pixels[:8]:
                if i % 2 == 0:
                    binary_str += '0'
                else:
                    binary_str += '1'

            # Konverter fra binær til ASCII og gem
            message += self.binary_to_ascii(binary_str)

            # Check om beskeden er slut
            if pixels[-1] % 2 == 1:
                self.text_decoded_message.configure(text=message)
                return message

    # Konverter et byte fra binær til ASCII
    def binary_to_ascii(self, binary):
        ascii = chr(int(binary, 2))
        return ascii

    # Konverter beskeden fra ASCII til binær
    def ascii_to_binary(self, message):
        binary = []
        for i in message:
            binary.append(format(ord(i), '08b'))
        return binary

    # Modificer pixels ud fra beskeden i binær og returnerer dem
    def modify_pixels(self, pixel, message):
        binary_message = self.ascii_to_binary(message)
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
                if binary_message[i][j] == '0' and pixel[j] % 2 == 1:
                    if pixel[j] % 2 == 1:
                        pixel[j] -= 1
                elif binary_message[i][j] == '1' and pixel[j] % 2 == 0:
                    pixel[j] -= 1

            # Brug det sidste bit i hvert sæt til at bestemme om decoderen skal læse videre
            if i == binary_message_len - 1:
                if pixel[-1] % 2 == 0:
                    pixel[-1] -= 1
            elif pixel[-1] % 2 != 0:
                pixel[-1] -= 1

            # Returner en pixel af gangen
            pixel = tuple(pixel)
            yield pixel[0:3]
            yield pixel[3:6]
            yield pixel[6:9]

    # Udvælg pixels og indsæt modificerede pixels i billedet
    def insert_pixels(self, image, message):

        self.image_width = image.size[0]
        (x, y) = (0, 0)

        # Gentag for hver modificeret pixel
        for pixel in self.modify_pixels(image.getdata(), message):

            # Indsæt modificeret pixels i det nye billede
            image.putpixel((x, y), pixel)

            # Vælg positionen af den næste pixel
            if x == self.image_width - 1:
                x = 0
                y += 1
            else:
                x += 1

    # Encode en besked i det valgte billede
    def encode(self):
        image = Image.open(self.path, 'r')
        message = self.entry_message.get()
        message_len = len(message)
        if message_len == 0:
            raise ValueError("Type in a message")

        self.insert_pixels(image, message)
        image.save(self.path)

        path3 = Image.open(self.path)
        wpercent = self.image_width / float(path3.size[0])
        hsize = int((float(path3.size[1]) * float(wpercent)))
        path3 = path3.resize((self.image_width, hsize), Image.ANTIALIAS)
        path3 = ImageTk.PhotoImage(path3)
        self.image_label.configure(image=path3)
        self.image_label.image = path3

        self.text_encode_done.configure(text="Encoding færdig!")

    # Opstil knapperne, og hvilken metode de kører når de bliver klikket
    def init_buttons(self):
        btn_open = Button(window, text="Open", command=self.open_button)
        btn_open.place(x=220, y=80, anchor="center")

        btn_save = Button(window, text="Save", command=self.save_button)
        btn_save.place(x=480, y=80, anchor="center")

        btn_encode = Button(window, text="Encode", command=self.encode)
        btn_encode.place(x=220, y=544, anchor="center")

        btn_decode = Button(window, text="Decode", command=self.decode)
        btn_decode.place(x=480, y=544, anchor="center")


ImageSteganography()
window.mainloop()
