import socket
from loop_async import EventLoopAsync

loop = EventLoopAsync()

async def run_serve(host='127.0.0.1', port=9010):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client_sock, addr = await loop.sock_accept(sock)
        print('connection from: ', addr)
        loop.create_task(handle_client(client_sock))

async def handle_client(sock):
    while True:
        received_data = await loop.sock_recv(sock, 4096)
        if not received_data:
            break
        await loop.sock_sendall(sock, received_data)

    print('client disconnected: ', sock.getpeername())
    sock.close()

if __name__ == '__main__':
    loop.create_task(run_serve())
    loop.run()