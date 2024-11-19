import os

def get_image_dimensions(input_file):
    with open(input_file,"rb") as f:
        f.seek(39)
        data = f.read(6)
        signature = data.decode('utf-8')
        f.seek(49)
        data = f.read(2)
        width = int.from_bytes(data, byteorder='big') 
        f.seek(321)
        data = f.read(2)
        height = int.from_bytes(data, byteorder='big')
    f.close()
    if signature == 'KSA00F':
        header_size = 640
    elif signature == 'KSA00J':
        header_size = 685
    else:
        raise ValueError("ERROR: Ecountered unknown header.")

    return height, width, header_size