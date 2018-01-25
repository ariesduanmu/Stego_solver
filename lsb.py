from PIL import Image

def extract(image_filename,
            alpha_plane = -1, 
            red_plane = 0, 
            green_plane = 0, 
            blue_plane = 0, 
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
    for r in range(row_data):
        for c in range(column_data):
            r, g, b, a = conv.getpixel((c, r))
            for current_bit in bit_plane_order:
                if current_bit = "R" and red_plane >= 0:
                    v.append((r & (1 << red_plane)) >> red_plane)
                elif current_bit = "G" and green_plane >= 0:
                    v.append((g & (1 << green_plane)) >> green_plane)
                elif current_bit = "B" and green_plane >= 0:
                    v.append((b & (1 << blue_plane)) >> blue_plane)
                elif current_bit = "A" and alpha_plane >= 0:
                    v.append((a & (1 << alpha_plane)) >> alpha_plane)
    
            