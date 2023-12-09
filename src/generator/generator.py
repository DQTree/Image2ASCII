import os
import string

from PIL import Image, ImageDraw, ImageFont

#   Greyscale from:
#   https://paulbourke.net/dataformats/asciiart/

gray_scale70 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gray_scale10 = '@%#*+=-:. '


def image_create(width: int, height: int):
    return Image.new(mode="RGB", size=(width, height))

def image_read(path: string):
    return Image.open(path).convert(mode='L')

def pixel_to_ascii(image: Image):
    pixels = image.getdata()
    asciiStr = ""
    for pixel in pixels:
        asciiStr += gray_scale70[pixel//25]
    return asciiStr

def ascii2image(asciiStr: string, width: int, height: int, font_size: int, scale):
    image = Image.new("RGB", (width*scale, height*scale), color="white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    x, y = 0, 0

    for char in asciiStr:
        draw.text((x, y), char, font=font, fill="black")
        x += font_size
        if x >= image.width:
            x = 0
            y += font_size

    return image
def image2ascii(path: string):
    imageName, _ = os.path.splitext(path)
    baseImage = image_read(path)
    inAscii = pixel_to_ascii(baseImage)
    asciiLen = len(inAscii)
    asciiImage = ""

    asciiToImage = ascii2image(inAscii, baseImage.width, baseImage.height, 10, 10)
    for row in range(0, asciiLen, baseImage.width):
        asciiImage += inAscii[row:row+baseImage.width]+"\n"

    asciiToImage.save(f"{imageName}_image.png")
    with open(f"{imageName}_ascii.txt", "w") as f:
        f.write(asciiImage)

image2ascii("../testfolder/stolas_test.jpg")
