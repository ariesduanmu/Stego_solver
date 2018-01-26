import matplotlib.pyplot as plt
from PIL import Image

def compare(original, intercepted):
    original_img = Image.open(original)
    intercepted_img = Image.open(intercepted)

    width, height = original_img.size
    conv_original = original_img.convert("RGBA").getdata()
    conv_intercepted = intercepted_img.convert("RGBA").getdata()

    for h in range(height):
        for w in range(width):
            r_o, g_o, b_o, a_o = conv_original.getpixel((w, h))
            r_i, g_i, b_i, a_i = conv_intercepted.getpixel((w, h))

            if (r_o, g_o, b_o, a_o) != (r_i, g_i, b_i, a_i):
                with open("change.txt",'a+') as f:
                    f.write("({}, {}) | original: {} -- intercepted: {}\n".format(w, h, (r_o, g_o, b_o, a_o), (r_i, g_i, b_i, a_i)))

if __name__ == "__main__":
    compare("bitsnbytes/original.png", "bitsnbytes/intercepted.png")
