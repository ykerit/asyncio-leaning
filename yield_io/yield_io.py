import socket

from loop_io import EventLoopIO

loop = EventLoopIO()

def run_serve(host='127.0.0.1', port=9010):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        yield 'READ_NOW', sock
        client_sock, addr = sock.accept()
        print('connection from: ', addr)
        loop.create_task(handle_client(client_sock))

def handle_client(sock):
    while True:
        yield 'READ_NOW', sock
        received_data = sock.recv(4096)
        if not received_data:
            break
        yield 'WRITE_NOW', sock
        sock.sendall(received_data)
        
    print('client disconnected: ', sock.getpeername())
    sock.close()

if __name__ == '__main__':
    loop.create_task(run_serve())
    loop.run()