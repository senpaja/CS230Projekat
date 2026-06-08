from database import get_results
import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Publisher pokrenut")

while True:

    print("\n1 - Dodaj rezultat")
    print("2 - Prikazi rezultate")
    print("3 - Izlaz")

    choice = input("Izbor: ")

    if choice == "1":

        home = input("Domaci tim: ")
        away = input("Gostujuci tim: ")
        score = input("Rezultat: ")

        message = f"RESULT;{home};{away};{score}"

        client.send(message.encode())

    elif choice == "2":

        results = get_results()

        print("\n--- REZULTATI ---")

        if len(results) == 0:
            print("Nema rezultata.")

        for result in results:
            print(f"{result[0]} {result[2]} {result[1]}")

    elif choice == "3":
        print("Izlaz...")
        break

client.close()