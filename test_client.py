import socket
import sys


def run_client(msg):
    # Socket set-up
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
        )
    address = ('127.0.0.1', 10000)
    client_socket.connect(address)

    # Send the message to the server
    client_socket.sendall(msg)
    client_socket.shutdown(socket.SHUT_WR)

    message = receive_data(client_socket)

    # Socket tear-down
    client_socket.close()
    return message


def receive_data(conn):
    accu = ''
    while True:
        buff = conn.recv(32)
        accu += buff
        if not buff:
            return accu


if __name__ == '__main__':
    # If there is a command line argument -> get it
    try:
        msg = sys.argv[1]
    # If no CLA -> prompt for a message
    except IndexError:
        msg = raw_input("> ")

    print run_client(msg)
