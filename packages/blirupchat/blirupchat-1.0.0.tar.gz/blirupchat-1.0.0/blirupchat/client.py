from socket import AF_INET, socket, SOCK_STREAM  # AF_INET & SOCK_STREAM for TCP sockets
from threading import Thread
import tkinter as tk


def receive():
    """
    Håndtering af indkommende beskeder

    :return:
    """
    while True:  # Uendeligt loop for indkommende beskeder
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")  # recv venter på indkommende beskeder
            msg_list.insert(tk.END, msg)  # Tilføjer beskeden til listen vist i chatvinduet
        except OSError:  # Undtagelse for hvis klienten forlader chatten
            break


def send(event=None):
    """
    Håndtering af udgående beskeder

    :param event: binder send_button-knappen til send-metoden gennem tkinter.
    :return:
    """
    msg = my_msg.get()  # Tager beskeder fra inputfeltet
    my_msg.set("")  # Nulstiller inputfeltet
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """
    Håndtering af afslutning

    :param event: binder lukning af klienten til on_closing metoden gennem tkinter
    :return:
    """
    my_msg.set("{quit}")
    send()
# Sætter og sender en sidste Quit-besked for at lukke forbindelsen mellem klient og server korrekt


# ---- Håndtering af klienten ----
top = tk.Tk()
top.title("Python Chat")  # Titel på klientvinduet
top.protocol("WM_DELETE_WINDOW", on_closing)
messages_frame = tk.Frame(top)  # Chatvinduet
my_msg = tk.StringVar()  # Inputfeltet i klienten
my_msg.set("Indtast din besked her.")
scrollbar = tk.Scrollbar(messages_frame)  # Scrollbaren i klienten

# ---- Håndtering af chatvinduet ----
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

# ---- Håndtering af inputfeltet ----
entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(top, text="Send", command=send)  # Binder send_button-knappen til send-metoden
send_button.pack()

# ---- Forbindelse til serveren ----
HOST = input('Indtast host: ')
PORT = input('Indtast port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# ---- Opstart af klienten ----
receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()  # Starter klienten
