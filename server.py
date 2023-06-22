import socket
import multiprocessing as mp
import threading

SERVER_IP = "localhost"
UDP_PORT = 9090
TCP_PORT = 9091
processes = []


def cleanup():
    for proccess in processes:
        proccess.terminate()
    for proccess in processes:
        proccess.join()


def handle_tcp_client(client, address):
    print(f"TCP server connected to client {address}")
    while True:
        try:
            if message := client.recv(1024):
                print(f"{client.getpeername()} sent a message")
                client.send(message)
            else:
                break
        except (KeyboardInterrupt):
            client.close()
            print(f"Zatvorio sam konekciju sa klijentom {client.getpeername()}")
            break


def start_udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((SERVER_IP, UDP_PORT))
    while True:
        try:
            message, address = server.recvfrom(1024)
            print(f"UDP Server: Got a message from {address}")
            server.sendto(message, address)
        except (KeyboardInterrupt):
            print("Shutting down UDP server...")
            server.close()
            break


def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, TCP_PORT))
    server.listen(3000)
    while True:
        try:
            client, address = server.accept()
            thread = threading.Thread(target=handle_tcp_client, args=(client, address))
            thread.start()
        except KeyboardInterrupt:
            print("Shutting down TCP server...")
            server.close()
            break
        except socket.timeout:
            pass


def main():
    try:
        print("Server started...")
        p1 = mp.Process(target=start_udp_server)
        p2 = mp.Process(target=start_tcp_server)
        processes.extend((p1, p2))
        p1.start()
        p2.start()
        for proccess in processes:
            proccess.join()
    except KeyboardInterrupt:
        print("Shutting down server...")
        cleanup()


if __name__ == "__main__":
    main()
