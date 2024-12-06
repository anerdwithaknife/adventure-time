import struct
import sys

def parse_file_listing(data):
    marker, num_files = struct.unpack(">I I", data[:8])
    if marker != 0x44AAAA44:
        raise ValueError("Invalid file list marker")

    offset = 8
    filenames = []

    for _ in range(num_files):
        file_marker, name_length = struct.unpack(">I I", data[offset:offset+8])
        if file_marker != 0x3A3AA3A3:
            raise ValueError("Invalid file marker")
        offset += 8

        filename = data[offset:offset+name_length].decode("utf-8")
        filenames.append(filename)
        offset += name_length

    return filenames

def parse_thumbnail(data):
    marker, image_size = struct.unpack(">I I", data[:8])
    if marker != 0x2A2AA2A2:
        raise ValueError("Invalid thumbnail marker")

    with open("data.bmp", "wb") as tb:
        tb.write(data[8:])


if len(sys.argv) < 2:
    print("Usage: adv3fs [command] [args..]\n"
          "  ls             List files on printer\n"
          "  thumb [file]   Download thumbnail from printer")

if sys.argv[1] == "ls":
    with open("M661.dat", "rb") as f:
        response = f.read().split(b"\r\nok\r\n")
        print('\n'.join(parse_file_listing(response[1])))
    
if sys.argv[1] == "thumb":
    with open("M662-gx.dat", "rb") as f:
        response = f.read().split(b"\r\nok\r\n")
        parse_thumbnail(response[1])
    
