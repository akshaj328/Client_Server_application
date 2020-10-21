
import tkinter as tk
from socket import socket
from threading import Thread
import time

# Reference: https://www.youtube.com/watch?v=Lbfe3-v7yE0
socket_object = socket(-1, -1)
socket_object.connect(("127.0.0.1", 5858))

sleep_killer_flag = False


def send_user_name():
    """
    This function handles user-names of the client. User-name is sent to server and the reply from server determines
    weather to accept the user-name or not.
    :return: None
    References: 1. https://github.com/Darshak1997/Chat-Application/blob/master/client1.py
    """
    user_name = username.get()  # Get the user-name from input field
    socket_object.send(bytes(user_name, "utf-8"))
    connected_message = str(socket_object.recv(1024).decode("utf8"))
    if connected_message == "Undone":  # if user-name is invalid
        username.set("")  # empty user-name field
        listbox.insert(tk.END, "User name already exists.. enter again")
    else:
        listbox.insert(tk.END, "Connected!!")
        Thread(target=sleeping).start()  # Start a thread which handles sleeping


def sleeping():
    """
    This function handles sleeping and waking up of threads

    :return: None
    """
    while True:
        temp = socket_object.recv(100)
        time_to_sleep = temp.decode("utf-8")
        time_to_sleep = int(time_to_sleep)
        message = "Sleeping {} seconds in client side".format(time_to_sleep)
        listbox.insert(tk.END, message)
        for second in range(1, time_to_sleep + 1):
            time.sleep(1)
            listbox.insert(tk.END, "Sleeping for more {} seconds".format(time_to_sleep - second))
            if sleep_killer_flag:  # If this flag becomes True, then interrupt detected
                listbox.insert(tk.END, "Interrupt detected.. waking up")
                thread_killer()  # Resets the flag
                break
        socket_object.send(bytes("Client {} waited {} seconds for server".format(username.get(), time_to_sleep), "utf-8"))


def thread_killer():
    """
    This function toggles sleep killing flag
    :return: None
    """
    global sleep_killer_flag
    sleep_killer_flag = True if not sleep_killer_flag else False


def disconnect():
    """
    Handle disconnection of clients
    :return: None
    References: 1. https://github.com/Darshak1997/Chat-Application/blob/master/client1.py
    """
    listbox.insert(tk.END, "Disconnected")
    user_name = username.get()
    socket_object.send(bytes(user_name, "utf-8"))
    socket_object.close()


if __name__ == '__main__':
    Thread().start()

    # GUI
    # Creating window size and title
    window = tk.Tk()
    window.title("Client")
    window.geometry("400x300")

    # Creating input for user-name
    """
    Reference: 1. https://pythonexamples.org/python-tkinter-login-form/
    """
    usernameLabel = tk.Label(window, text="User Name").grid(row=2, column=0)
    username = tk.StringVar()
    usernameEntry = tk.Entry(window, textvariable=username).grid(row=2, column=1)

    # Creating buttons for send, quit and resume thread operations
    send_button = tk.Button(window, text="Send", command=send_user_name).grid(row=4, column=0)
    quit_button = tk.Button(window, text="Quit", command=disconnect).grid(row=4, column=1)
    wake_button = tk.Button(window, text="Wake up", command=thread_killer).grid(row=14, column=0)

    # Creating list-box to view messages
    """
    1. https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
    """
    listbox = tk.Listbox(window, width=50)
    listbox.grid(row=10, column=0, columnspan=3, rowspan=3)

    # Attaching scroll-bar to list-box
    """
    References
    1. https://stackoverflow.com/questions/47368559/how-to-attach-my-scrollbar-to-my-listbox-widget
    """
    scroll_bar = tk.Scrollbar(window)
    listbox.config(yscrollcommand=scroll_bar.set)
    scroll_bar.grid(row=10, column=3, rowspan=3, sticky='NS')
    scroll_bar.config(command=listbox.yview)

    window.mainloop()


