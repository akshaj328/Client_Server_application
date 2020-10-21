# Client Server application using socket programming and thread management.

This project shows client server application in which the server can handle 3 simultaneous client connections. The client can connect to the server with a username which has to be unique. The server will randomly select a client and send that thread handling the client into sleep for some seconds. After completion of this time, the client will wake up.

All of this managed with a GUI using TkInter.

## Steps to run the program:
1.	Start Command prompt and enter: py -3.7 server.py
2.	Start another command prompt and enter: py -3.7 client.py
3.	Start another command prompt and enter: py -3.7 client.py
4.	Start another command prompt and enter: py -3.7 client.py
5.	In each Client GUI : Enter Your Username and hit send
6.	Click ‘Wake up’ if you want to terminate sleep period
7.	Click ‘Quit’ button to close connection
