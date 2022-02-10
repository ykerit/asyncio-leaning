import socket

from loop_no_io import EventLoopNoIO

loop = EventLoopNoIO()

def run_serve(host='127.0.0.1', port=9010):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        yield
        client_sock, addr = sock.accept()
        loop.create_task(handle_client(client_sock))

def handle_client(sock):
    while True:
        yield
        received_data = sock.recv(4096)
        print('received_data')
        if not received_data:
            break
        yield
        sock.sendall(received_data)
        print('send all')


    print('client disconnected: ', sock.getpeername())
    sock.close()

if __name__ == '__main__':
    loop.create_task(run_serve())
    loop.run()