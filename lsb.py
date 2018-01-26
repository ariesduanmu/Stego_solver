from PIL import Image

def extract(image_filename,
            alpha_plane = [], 
            red_plane = [0], 
            green_plane = [0], 
            blue_plane = [0], 
            order = 0, 
            bit_plane_order = "RGBA"):
    '''
       alpha_plane/red_plane/green_plane/blue_plane: -1 ~ 7, -1 means ignore this plane
       order: 0 = row, 1 = column
       bit_plane_order: RGBA/RBGA/GBRA/GRBA/BRGA/BGRA/...
    '''
    img = Image.open(image_filename)
    width, height = img.size
    conv = img.convert("RGBA").getdata()

    row_data = height if order == 0 else width
    column_data = width if order == 0 else height

    if order == 0:
        v = []
        for h in range(height):
            for w in range(width):
                v += extract_data(conv,w, h, alpha_plane, red_plane, green_plane, blue_plane, bit_plane_order)
    else:
        v = []
        for w in range(width):
            for h in range(height):
                v += extract_data(conv,w, h, alpha_plane, red_plane, green_plane, blue_plane, bit_plane_order)
                
    return v

def extract_data(image, width, height, alpha_plane, red_plane, green_plane, blue_plane, bit_plane_order):
    v = []
    r, g, b, a = image.getpixel((width, height))
    planes = {"R":[r, red_plane], 
              "G":[g, green_plane], 
              "B":[b, blue_plane],
              "A":[a, alpha_plane]}

    for current_bit in bit_plane_order:
        current_plane = planes[current_bit][1]
        if len(current_plane) > 0:
            for plane in current_plane:
                v.append((planes[current_bit][0] & (1 << plane)) >> plane)
    return v

def difference(original, intercepted, order = 0):
    original_img = Image.open(original)
    intercepted_img = Image.open(intercepted)

    width, height = original_img.size
    conv_original = original_img.convert("RGBA").getdata()
    conv_intercepted = intercepted_img.convert("RGBA").getdata()

    r_difference, g_difference, b_difference, a_difference = [], [], [], []
    if order == 0:

        for h in range(height):
            for w in range(width):
                r, g, b, a = extract_difference(conv_original, conv_intercepted, w, h)
                r_difference += [r]
                g_difference += [g]
                b_difference += [b]
                a_difference += [a]
    else:
        for w in range(width):
            for h in range(height):
                r, g, b, a = extract_difference(conv_original, conv_intercepted, w, h)
                r_difference += [r]
                g_difference += [g]
                b_difference += [b]
                a_difference += [a]
            

    return r_difference, g_difference, b_difference, a_difference

def extract_difference(conv_original, conv_intercepted, width, height):
    r_o, g_o, b_o, a_o = conv_original.getpixel((width, height))
    r_i, g_i, b_i, a_i = conv_intercepted.getpixel((width, height))
    return r_i - r_o, g_i - g_o, b_i - b_o, a_i - a_o

def assemble(v, filte = True):
    message = b""
    v = ''.join(map(str, v))
    for i in range(0, len(v), 8):
        n = int(v[i:i+8], 2)
        if filte:
            if 33 <= n <= 126:
                message += bytes([n])
        else:
            message += bytes([n])
    return message

if __name__ == "__main__":
    #image_filename = "BAND.JPG"
    #image_filename = "bitsnbytes/intercepted.png"
    #print(extract(image_filename, [], [], [], [0], 1 )[:416])

    r,g,b,a = difference("bitsnbytes/original.png", "bitsnbytes/intercepted.png", 1)

    print(assemble(b[:416], False))

    
            