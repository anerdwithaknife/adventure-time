import struct

# Define image dimensions
width = 240
height = 320

# Open the raw RGBA file
with open("splash.raw", "rb") as rgba_file:
    rgba_data = rgba_file.read()

# Prepare the RGB565 output file
with open("splash.img", "wb") as rgb565_file:
    img_pixels = []
    for y in range(height):
        for x in range(width):
            # Calculate the RGBA offset
            offset = (y * width + x) * 4
            r, g, b, a = rgba_data[offset : offset + 4]

            # Convert RGBA to RGB565
            r5 = (r >> 3) & 0x1F  # 5 bits for red
            g6 = (g >> 2) & 0x3F  # 6 bits for green
            b5 = (b >> 3) & 0x1F  # 5 bits for blue
            rgb565 = (r5 << 11) | (g6 << 5) | b5

            # Write in little-endian order
            # rgb565_file.write(struct.pack("<H", rgb565))
            img_pixels.append(struct.pack("<H", rgb565))

    img_pixels.reverse()
    rgb565_file.write(b"".join(img_pixels))
