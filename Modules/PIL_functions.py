from PIL import Image

def drawProgressBar(d, x, y, w, h, progress, bg="black", fg="red"):
    # draw background
    d.ellipse((x+w, y, x+h+w, y+h), fill=bg)
    d.ellipse((x, y, x+h, y+h), fill=bg)
    d.rectangle((x+(h/2), y, x+w+(h/2), y+h), fill=bg)

    # draw progress bar
    w *= progress
    d.ellipse((x+w, y, x+h+w, y+h),fill=fg)
    d.ellipse((x, y, x+h, y+h),fill=fg)
    d.rectangle((x+(h/2), y, x+w+(h/2), y+h),fill=fg)

    return d


def moveImage(image1 : str, image2 : str):
    im1 = Image.open(image1)
    im2 = Image.open(image2)

    new = Image.new("RGBA", (480, 400), (0, 0, 0, 0))

    copy_im = new.copy()
    copy_im.paste(im1, (95, 50))
    copy_im.paste(im2, (0, 350))

    copy_im.save('./Images/send.png')

    
