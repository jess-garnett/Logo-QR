import pyqrcode as pyqr
from PIL import Image
from math import floor, ceil

def generate_qr(qr_string="Test String",color_fg=(0,0,0,255),color_bg=(255,255,255,255),qr_filename="qr_gen.png",logo_filepath="qr_logo.png",preview=True,confirm=True,error='H',logo_fraction=.2):
        url = pyqr.create(qr_string, error) #https://pythonhosted.org/PyQRCode/create.html
        # 'H' term allows for 30% of the code to be error correct. Would like to keep logo below 20%

        if logo_filepath is None: #if no logo is given then just save the qr code with the qr file name.
                url.png(qr_filename, scale = 1)
                return
        ###Figure out necessary scaling for QR code
        url.png('LogoQR_processor.png', scale = 1)#https://pythonhosted.org/PyQRCode/rendering.html?highlight=scale
        width, height = Image.open('LogoQR_processor.png').size #gets the width and height of the generated scale=1 QR code
        qr_width=width-8 #removes the safety area around the QR code
        qr_height=height-8 #removes the safety area around the QR code
        qr_area=(qr_height*qr_width)-(3*64) #multiples width*height and removes the alignment corners from the area
        qr_area_use=floor(qr_area*logo_fraction) #sets usable area to 20% of QR code area - gives buffer as error correction should allow up to 30%
        logo=Image.open(logo_filepath) #opens the logo to be used
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

        ###Pastes the logo onto the QR code, preview and saves or confirms and then saves.
        qr_code.paste(logo_w_bg,(width_position,height_position))
        if preview is True:
                qr_code.show()
        
        if confirm is False:
                qr_code.save(qr_filename)
        elif confirm is True:
                confirmation=input("Save to file:"+qr_filename+"[y,n]:")
                if confirmation=="y":
                        qr_code.save(qr_filename)

if __name__=="__main__":
        generate_qr(qr_string="https://github.com/jess-garnett/Logo-QR",qr_filename="test_qr_gen.png",logo_filepath="qr_logo.png")
        # generate_qr(qr_string="https://github.com/jess-garnett/Logo-QR",qr_filename="test_qr_gen.png",logo_filepath="qr_logo_transparent.png",color_bg=(0,0,0,0))