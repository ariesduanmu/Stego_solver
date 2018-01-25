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

    v = []
    for row in range(row_data):
        for column in range(column_data):
            r, g, b, a = conv.getpixel((column, row))
            for current_bit in bit_plane_order:
                if current_bit == "R" and len(red_plane) > 0:
                    for r_plane in red_plane:
                        v.append((r & (1 << r_plane)) >> r_plane)
                elif current_bit == "G" and len(green_plane) > 0:
                    for g_plane in green_plane:
                        v.append((g & (1 << g_plane)) >> g_plane)
                elif current_bit == "B" and len(blue_plane) > 0:
                    for b_plane in blue_plane:
                        v.append((b & (1 << b_plane)) >> b_plane)
                elif current_bit == "A" and len(alpha_plane) > 0:
                    for a_plane in alpha_plane:
                        v.append((a & (1 << a_plane)) >> a_plane)
    return assemble(v)

def assemble(v):
    message = ""
    v = ''.join(map(str, v))
    for i in range(0, len(v), 8):
        n = int(v[i:i+8], 2)
        if 33 <= n <= 126:
            message += chr(n)
    return message

if __name__ == "__main__":
    image_filename = "BAND.JPG"
    print(extract(image_filename, [], [], [], [] ))

    
            