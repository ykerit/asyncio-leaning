from cmath import sin
import socket
from loop_yield_from import EventLoopYieldFrom

loop = EventLoopYieldFrom()

def run_serve(host='127.0.0.1', port=9010):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client_sock, addr = yield from loop.sock_accept(sock)
        print('connection from: ', addr)
        loop.create_task(handle_client(client_sock))

def handle_client(sock):
    while True:
        received_data = yield from loop.sock_recv(sock, 4096)
        if not received_data:
            break
        yield from loop.sock_sendall(sock, received_data)

    print('client disconnected: ', sock.getpeername())
    sock.close()

if __name__ == '__main__':
    loop.create_task(run_serve())
    loop.run()