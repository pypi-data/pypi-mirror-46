from socket import AF_INET, socket, SOCK_STREAM  # AF_INET & SOCK_STREAM for TCP sockets
from threading import Thread


def accept_incoming_connections():
    """
    Håndtering af opkoblende klienter

    :return:
    """
    while True:  # Uendeligt loop for indkommende klienter
        client, client_address = SERVER.accept()  # Logning af klienten
        print("%s:%s er tilkoblet." % client_address)
        client.send(bytes("Velkommen til serveren! Indtast dit brugernavn og tryk Enter.", "utf8"))
        addresses[client] = client_address  # Gemmer klientadressen
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Tager client socket som argument
    """
    Håndtering af opkoblede klienter

    :param client: klientens socket, bestående af adressen(HOST & PORT nummer)
    :return:
    """
    name = client.recv(BUFSIZ).decode("utf8")  # Logning af brugernavn
    welcome = 'Velkommen %s! Tast {quit} for at afslutte.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s er tilkoblet serveren." % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name  # Gemmer brugernavnet

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):  # Broadcast
            broadcast(msg, name + ": ")
        # TODO: klient til klient chat - Husk at vende rækkefølgen i den ydre if/else sætning
        # elif msg == bytes("{@}", "utf8"):  # @brugernavn for Klient til Klient chat
        #     for client in addresses:
        #         if addresses[client] == ": "
        #             client.send(msg)
        else:  # Quit
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]  # Fjern klienten fra listen af tilsluttede klienter
            broadcast(bytes("%s har forladt serveren." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix er til navneidentifikation
    """
    Håndtering af offentlige beskeder

    :param msg: Indeholder beskeden
    :param prefix: Indeholder afsender
    :return:
    """
    for sock in clients:  # Sender beskeden til alle klienter
        sock.send(bytes(prefix, "utf8") + msg)


# ---- Håndtering af constants ----
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# ---- Opstart af server samt  ----
if __name__ == "__main__":
    SERVER.listen(5)
    print("Venter på klienter...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
# .join på ACCEPT_THREAD sørger for at serveren står og venter, i stedet for at gå videre til næste linie og lukke ned
    SERVER.close()
