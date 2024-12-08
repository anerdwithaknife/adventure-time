import argparse
from PIL import Image
import struct
  
def image_to_rgb565(input_image, output_raw):
    # Open the image file
    with Image.open(input_image) as img:
        # Ensure it's in RGBA mode
        img = img.convert("RGBA")
        width, height = img.size

        if width != 240 or height != 320:
            raise ValueError("Input image must be 240x320 pixels.")
            
        # Open the output file
        with open(output_raw, "wb") as rgb565_file:
            for y in range(height - 1, -1, -1):  # Flip vertically (if needed)
                for x in range(width - 1, -1, -1):  # Flip horizontally (if needed)
                    # Get pixel data (RGBA)
                    r, g, b, a = img.getpixel((x, y))

                    # Convert RGBA to RGB565
                    r5 = (r >> 3) & 0x1F  # 5 bits for red
                    g6 = (g >> 2) & 0x3F  # 6 bits for green
                    b5 = (b >> 3) & 0x1F  # 5 bits for blue
                    rgb565 = (r5 << 11) | (g6 << 5) | b5

                    # Write RGB565 in little-endian order
                    rgb565_file.write(struct.pack("<H", rgb565))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert image to RGB565 RAW format.")
    parser.add_argument("input", help="Input image file")
    parser.add_argument("output", help="Output FlashForge img file")
    args = parser.parse_args()

    image_to_rgb565(args.input, args.output)
