
import tkinter as tk
from socket import socket
from threading import Thread
import random
import time


# Declaring global variables
recipients = []
user_names = []
address_map = {}
client_connection_map = {}
on_going_sleep_threads = {}


def accept_connection():
    """
    This function handles incoming connections
    :return: None
    References: 1. https://github.com/Darshak1997/Chat-Application/blob/master/server1.py
    """
    while True:
        client_socket, address = socket_object.accept()
        address_map[client_socket] = address

        Thread(target=handling, args=(client_socket,)).start()


def server_user_handling(client_socket):
    """
    This function receives user-name and checks if its valid and then sends a message to the client
    :param client_socket: Connection to send/receive data
    :return: connection and connected user-name
    References: 1. https://github.com/Darshak1997/Chat-Application/blob/master/server1.py
    """
    while True:
        user_name = client_socket.recv(100).decode("utf-8")
        if user_name in user_names:
            client_socket.send(str.encode("Undone"))  # User-name already exists
        else:
            user_names.append(user_name)
            on_going_sleep_threads[user_name] = False  # This variable maintains clients which are sleeping
            listbox.insert(tk.END, "'{}' connected".format(user_name))
            client_socket.send(str.encode("Done"))
            return client_socket, user_name


def disconnection(client_socket, username):
    """
    This functions handles disconnection and displaying message on the server message list
    :param client_socket: Connection
    :param username: user-name to be disconnected
    :return: None
    """
    while True:
        msg = client_socket.recv(100).decode("utf-8")
        if msg == username:
            del client_connection_map[username]
            user_names.remove(username)
            client_socket.close()
            listbox.insert(tk.END, "'{} disconnected'".format(username))
            break
        listbox.insert(tk.END, "'{}'".format(msg))
        on_going_sleep_threads[username] = False


def handling(client_socket):
    """
    Function to send random client random integer
    :param client_socket: Connection
    :return: None
    """
    client_socket, user_name = server_user_handling(client_socket)
    client_connection_map[user_name] = client_socket

    Thread(target=disconnection, args=(client_socket, user_name)).start()  # This thread waits for disconnection request
    while len(list(client_connection_map.keys())) >= 1:
        if list(client_connection_map.items()):
            while True:
                user_name, connection = random.choice(list(client_connection_map.items()))
                if on_going_sleep_threads[user_name] == False:
                    break
            on_going_sleep_threads[user_name] = True
            time_to_sleep = str(random.randint(3, 9))
            connection.send(bytes(time_to_sleep, "utf-8"))
            time.sleep(10)


def display_clients():
    """
    Function to handle display of clients in the server GUI
    :return:
    """
    client_list = ", ".join(list(client_connection_map.keys()))
    listbox.insert(tk.END, client_list)


if __name__ == "__main__":
    # Reference: https://www.youtube.com/watch?v=Lbfe3-v7yE0
    socket_object = socket(-1, -1)
    socket_object.bind(("127.0.0.1", 5858))
    socket_object.listen(3)

    thread = Thread(target=accept_connection)
    thread.start()

    # GUI
    # Creating window size and title
    window = tk.Tk()
    window.title("Server")
    window.geometry("400x300")

    # Creating list-box to view messages
    """
    1. https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
    """
    listbox = tk.Listbox(window, width=50)
    listbox.grid(row=0, column=0, columnspan=3, rowspan=3)

    # Attaching scroll-bar to list-box
    """
    References
    1. https://stackoverflow.com/questions/47368559/how-to-attach-my-scrollbar-to-my-listbox-widget
    """
    scroll_bar = tk.Scrollbar(window)
    listbox.config(yscrollcommand=scroll_bar.set)
    scroll_bar.grid(row=0, column=3, rowspan=3, sticky='NS')
    scroll_bar.config(command=listbox.yview)

    display_clients_button = tk.Button(window, text="Display clients", command=display_clients).grid(row=6, column=0)

    window.mainloop()




