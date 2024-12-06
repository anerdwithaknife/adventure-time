#!/usr/bin/env python3

import socket
import threading

# Printer's address and port
PRINTER_IP = "10.10.100.254"
PRINTER_PORT = 8899

# Local proxy server settings
LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 8899

def handle_connection(client_socket):
    # Connect to the printer
    printer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    printer_socket.connect((PRINTER_IP, PRINTER_PORT))
    
    def forward_data(source, destination, direction):
        while True:
            try:
                data = source.recv(4096)
                if not data:
                    break
                print(f"[{direction}] {data}")  # Log in hex format (or raw if preferred)
                destination.sendall(data)
            except Exception as e:
                print(f"Error forwarding {direction}: {e}")
                break

    # Start threads to forward data
    threading.Thread(target=forward_data, args=(client_socket, printer_socket, "FlashPrint -> Printer"), daemon=True).start()
    threading.Thread(target=forward_data, args=(printer_socket, client_socket, "Printer -> FlashPrint"), daemon=True).start()

def start_proxy():
    # Start the proxy server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCAL_HOST, LOCAL_PORT))
    server.listen(5)
    print(f"Proxy listening on {LOCAL_HOST}:{LOCAL_PORT}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection received from {addr}")
        threading.Thread(target=handle_connection, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    try:
        start_proxy()
    except KeyboardInterrupt:
        print("Shutting down proxy...")

