from PIL import Image
def pixval():
    img = Image.open("lena.png").convert('L')  # convert image to 8-bit grayscale
    WIDTH, HEIGHT = img.size
    data = list(img.getdata()) # convert image data to a list of integers
    # convert that to 2D list (list of lists of integers)
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

    return data
