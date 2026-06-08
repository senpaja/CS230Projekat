import socket
import threading
import json

from database import init_db, save_result
from middleware import log

HOST = "127.0.0.1"
PORT = 5000

subscribers = {}


def save_to_json(event):
    try:
        with open("results.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(event)

    with open("results.json", "w") as f:
        json.dump(data, f, indent=4)


def notify_subscribers(home, away, score):

    for subscriber, team in list(subscribers.items()):

        try:

            if team.lower() == "svi" \
               or team.lower() == home.lower() \
               or team.lower() == away.lower():

                subscriber.send(
                    f"NOVI REZULTAT: {home} {score} {away}".encode()
                )

        except:
            del subscribers[subscriber]


def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode()

            if message.startswith("SUBSCRIBE"):
                _, team = message.split(";")

                subscribers[client] = team

                log(f"Subscriber prati: {team}")

            elif message.startswith("RESULT"):
                _, home, away, score = message.split(";")

                event = {
                    "home_team": home,
                    "away_team": away,
                    "score": score
                }

                save_result(home, away, score)
                save_to_json(event)

                log(f"Rezultat primljen: {home} vs {away}")

                notify_subscribers(
                    home,
                    away,
                    score
                )

        except:
            break

    client.close()


def start_server():
    init_db()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    log("Server pokrenut")

    while True:
        client, addr = server.accept()

        log(f"Povezan klijent {addr}")

        thread = threading.Thread(
            target=handle_client,
            args=(client,)
        )

        thread.start()


if __name__ == "__main__":
    start_server()