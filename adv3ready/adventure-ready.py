from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import ping3
import threading
import time

def create_icon(color):
    image = Image.new("RGB", (64, 64), color)
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill=color)
    return image

def check_ip(icon, ip):
    while True:
        try:
            result = ping3.ping(ip, timeout=1)
            icon.icon = create_icon("green" if result else "red")
        except:
            icon.icon = create_icon("red")
        time.sleep(5)

# netsh wlan connect adventurer3

def main():
    ip_to_check = "10.10.100.254"
    icon = Icon("Adventure Time", create_icon("gray"))
    icon.menu = Menu(MenuItem("Exit", lambda: icon.stop()))
    
    thread = threading.Thread(target=check_ip, args=(icon, ip_to_check), daemon=True)
    thread.start()
    icon.run()

if __name__ == "__main__":
    main()

