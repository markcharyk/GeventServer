def echo(socket, address):
    """a simple echoing handler for incoming client connections

    It will be used for each incoming connection on a separate greenlet.
    """
    buffsize = 16
    while True:
        data = socket.recv(buffsize)
        if data:
            socket.sendall(data)
        else:
            socket.close()
            break

if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 10000), echo)
    print('Starting echo server on port 10000')
    server.serve_forever()
