#Python TCP Client B
import socket

host = socket.gethostname()
port = 2008
BUFFER_SIZE = 2000
MESSAGE = raw_input("tcpClient: Enter message / Enter exit:")

tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientB.connect((host, port))


while MESSAGE != 'exit':
        tcpClientB.send(MESSAGE)
        data = tcpClientB.recv(BUFFER_SIZE)
        #print("Client received data:", data)
        print(data)
        MESSAGE = raw_input("tcpClient: Enter message to continue / Enter exit:")

tcpClientB.close()

#use dictionaries to display available seat nos
"""
AF_INET is an address family that is used to designate the type of addresses that your socket can communicate with (in this case, Internet Protocol v4 addresses). When you create a socket, you have to specify its address family, and then you can only use addresses of that type with the socket. The Linux kernel, for example, supports 29 other address families such as UNIX (AF_UNIX) sockets and IPX (AF_IPX), and also communications with IRDA and Bluetooth (AF_IRDA and AF_BLUETOOTH, but it is doubtful you'll use these at such a low level).

For the most part, sticking with AF_INET for socket programming over a network is the safest option. There is also AF_INET6 for Internet Protocol v6 addresses.
"""
