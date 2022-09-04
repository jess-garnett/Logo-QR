from tkinter import * #http://tkdocs.com/tutorial/firstexample.html
from tkinter import ttk
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import os
from math import ceil, floor
import pyqrcode # Import QRCode from pyqrcode https://www.geeksforgeeks.org/python-generate-qr-code-using-pyqrcode-module/
from PIL import Image
import sys


def generateQR(*args):
    try:
        ###Bring everything from the tk interface into variables that can be used.
        s=qr_string_entry.get()
        qr_filename=output_name_entry.get()+".png"
        color_fg=(int(fg_rgba_r.get()),int(fg_rgba_g.get()),int(fg_rgba_b.get()),int(fg_rgba_a.get()))#foreground color - default black:(0, 0, 0, 255)
        color_bg=(int(bg_rgba_r.get()),int(bg_rgba_g.get()),int(bg_rgba_b.get()),int(bg_rgba_a.get()))#background color - default white:(255, 255, 255, 255)
        #tuples are needed but are non-changable. Initializing them inside the function allows them to be reset everytime generate is run
        split_filepath=os.path.split(logo_filepath.get())
        os.chdir(split_filepath[0])
        #these two lines makes sure that the current working directory is the same as the logo file selected
        
        url = pyqrcode.create(s, error='H') #https://pythonhosted.org/PyQRCode/create.html
        # 'H' term allows for 30% of the code to be error correct. Would like to keep logo below 20%

        ###Figure out necessary scaling for QR code
        url.png('LogoQR_processor.png', scale = 1)#https://pythonhosted.org/PyQRCode/rendering.html?highlight=scale
        width, height = Image.open('LogoQR_processor.png').size #gets the width and height of the generated scale=1 QR code
        qr_width=width-8 #removes the safety area around the QR code
        qr_height=height-8 #removes the safety area around the QR code
        qr_area=(qr_height*qr_width)-(3*64) #multiples width*height and removes the alignment corners from the area
        qr_area_use=floor(qr_area*.2) #sets usable area to 20% of QR code area - gives buffer as error correction should allow up to 30%
        logo=Image.open(logo_filepath.get()) #opens the logo to be used
        lwidth, lheight = logo.size #gets the width and height of the logo
        logo_area=lwidth*lheight #calculates the area of the logo
        qr_scale=ceil((logo_area/qr_area_use)**.5)#determines scaling factor that would make the logo(at full scale) take up slightly less than 20% of the functional qr code area

        ###Create new QR code at correct scale and with the specified foreground and background
        url.png('LogoQR_processor.png', scale = qr_scale,module_color=color_fg,background=color_bg)
        qr_code=Image.open('LogoQR_processor.png') #opens the created QR code for processing
        qr_code=qr_code.convert("RGBA") #https://pillow.readthedocs.io/en/stable/reference/Image.html Converts to specified format for consistent merging

        ###Add a color_bg background on transparent logos. Still happens on non-transparent logos but has no effect
        logo=logo.convert("RGBA")
        logo_w_bg=Image.new("RGBA",logo.size,color_bg)
        logo_w_bg.paste(logo,mask=logo)

        ###Calculate where logo should go
        width_position=floor(((width*qr_scale)/2)-lwidth/2) #calculates width position for logo
        height_position=floor(((height*qr_scale)/2)-lheight/2) #calculates height position for logo

        ###Pastes the logo onto the QR code, saves the file, and shows the final result to the user.
        qr_code.paste(logo_w_bg,(width_position,height_position))
        qr_code.save(qr_filename)
        qr_code.show()

    except ValueError:
        pass
def getLogoFile():
    logo_filepath.set(askopenfilename(initialdir= os.getcwd()))#brings up file selection dialog
    split_filepath=os.path.split(logo_filepath.get())#splits selected filepath into head and tail
    logo_display.set("Logo File: "+split_filepath[1])#set display text to the tail end of the file path
    os.chdir(split_filepath[0])#change working directory to the head end of the file path
    ttk.Label(mainframe, text=logo_display.get()).grid(column=0, row=6, sticky=E, columnspan = 5)#Adds a label to override "No Logo"
    root.update()#updates the tkinter window


###Initializes the tkinter root, gives it a title and icon
root = Tk()
root.title("LogoQR WR1 by Jess Garnett")
base_path = getattr(sys, '_MEIPASS','.')+'/' #https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
root.iconbitmap(base_path+"JM3D_Logo_Mini.ico") #https://pyinstaller.org/en/stable/spec-files.html#:~:text=The%20spec%20file%20tells%20PyInstaller,contents%20of%20the%20spec%20file.

###Setup main frame of tkinter
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

###Setup content row
ttk.Label(mainframe, text="QR Contents:").grid(column=0, row=0, sticky=E)
qr_string = StringVar()
qr_string_entry = ttk.Entry(mainframe, width=6, textvariable=qr_string)
qr_string_entry.insert(END, "QR Content")
qr_string_entry.grid(column=1, row=0, sticky=(W, E),columnspan=4)

###Setup foreground color row
ttk.Label(mainframe, text="Foreground RGBA:").grid(column=0, row=2, sticky=E)
fg_rgba = ["","","",""]
fg_rgba_r = ttk.Entry(mainframe, width=6, textvariable=fg_rgba[0])
fg_rgba_r.insert(END, "0")
fg_rgba_r.grid(column=1, row=2, sticky=(W, E))
fg_rgba_g = ttk.Entry(mainframe, width=6, textvariable=fg_rgba[1])
fg_rgba_g.insert(END, "0")
fg_rgba_g.grid(column=2, row=2, sticky=(W, E))
fg_rgba_b = ttk.Entry(mainframe, width=6, textvariable=fg_rgba[2])
fg_rgba_b.insert(END, "0")
fg_rgba_b.grid(column=3, row=2, sticky=(W, E))
fg_rgba_a = ttk.Entry(mainframe, width=6, textvariable=fg_rgba[3])
fg_rgba_a.insert(END, "255")
fg_rgba_a.grid(column=4, row=2, sticky=(W, E))

###Setup background color row
ttk.Label(mainframe, text="Background RGBA:").grid(column=0, row=3, sticky=E)
bg_rgba = ["","","",""]
bg_rgba_r = ttk.Entry(mainframe, width=6, textvariable=bg_rgba[0])
bg_rgba_r.insert(END, "255")
bg_rgba_r.grid(column=1, row=3, sticky=(W, E))
bg_rgba_g = ttk.Entry(mainframe, width=6, textvariable=bg_rgba[1])
bg_rgba_g.insert(END, "255")
bg_rgba_g.grid(column=2, row=3, sticky=(W, E))
bg_rgba_b = ttk.Entry(mainframe, width=6, textvariable=bg_rgba[2])
bg_rgba_b.insert(END, "255")
bg_rgba_b.grid(column=3, row=3, sticky=(W, E))
bg_rgba_a = ttk.Entry(mainframe, width=6, textvariable=bg_rgba[3])
bg_rgba_a.insert(END, "255")
bg_rgba_a.grid(column=4, row=3, sticky=(W, E))

###Setup logo select button and logo display field
logo_filepath=StringVar()
ttk.Button(mainframe, text="Select Logo", command=getLogoFile).grid(column=0, row=5, sticky=W)
logo_display=StringVar()
logo_display.set("No Logo")
ttk.Label(mainframe, text=logo_display.get()).grid(column=0, row=6, sticky=E, columnspan = 5)

###Setup output row
ttk.Label(mainframe, text="Output:").grid(column=0, row=7, sticky=E, columnspan = 1)
output_name=StringVar()
output_name_entry= ttk.Entry(mainframe, textvariable=output_name)
output_name_entry.insert(END, "QR_Logo")
output_name_entry.grid(column=1, row=7, sticky=(E),columnspan=3)
ttk.Label(mainframe, text=".png").grid(column=4, row=7, sticky=W, columnspan = 1)

###Setup generate button
ttk.Button(mainframe, text="Generate", command=generateQR).grid(column=0, row=8, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

qr_string_entry.focus()#brings cursor to the qr_string_entry box when program is run

root.mainloop()#initializes the tkinter main loop

#to convert it all into a .exe https://stackoverflow.com/questions/5458048/how-can-i-make-a-python-script-standalone-executable-to-run-without-any-dependen
#running pyinstaller the .spec file.
#pyinstaller LogoQR_WR1.spec