import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            break


team = input("Koji tim pratite? ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(f"SUBSCRIBE;{team}".encode())

thread = threading.Thread(
    target=receive_messages,
    args=(client,)
)

thread.start()

print(f"Pretplaceni ste na tim: {team}")

while True:
    pass