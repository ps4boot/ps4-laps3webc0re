#!/usr/bin/env python3
import argparse
import socket
import struct
import os
import time
from progress.bar import Bar

MAGIC = 0x0000EA6E
CHUNK_SIZE = 4096
RETRY_INTERVAL = 5  # Sekunden zwischen den Versuchen

def send_file(ip, port, file_path):
    try:
        stats = os.stat(file_path)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))

        # Send magic
        sock.sendall(struct.pack('<I', MAGIC))
        # Send filesize
        sock.sendall(struct.pack('<Q', stats.st_size))

        # Send file
        bar = Bar('Uploading', max=stats.st_size)
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(CHUNK_SIZE)
                if not data:
                    break
                sock.sendall(data)
                bar.next(len(data))
        bar.finish()
        sock.close()
        print("Datei erfolgreich gesendet.")

    except ConnectionRefusedError:
        print(f"Port {port} nicht erreichbar. Warte {RETRY_INTERVAL} Sekunden...")
    except Exception as e:
        print(f"Fehler beim Senden: {e}")

def main(args):
    file_abs_path = os.path.abspath(args.file)
    while True:
        send_file(args.ip, args.port, file_abs_path)
        time.sleep(RETRY_INTERVAL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a file over TCP.')
    parser.add_argument('-i', '--ip', required=True, help='The target IP address.')
    parser.add_argument('-p', '--port', type=int, default=9045, help='The target port number.')
    parser.add_argument('-f', '--file', required=True, help='The file to send.')
    main(parser.parse_args())
