import socket,os,os.path,time

SOCKET_PATH = "/tmp/unix_socket_odometry"
UPDATE_STRING = "UPDATE"
QUERY_STRING = "QUERY"
QUERY_SIZE = len(QUERY_STRING)
UPDATE_SIZE = len(UPDATE_STRING)

current_x = 0
current_y = 0

if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
sever.listen(5)

while(True):
    conn,addr = server.accept()

    data = conn.recv(1024)
    if(data[:QUERY_SIZE] == QUERY_STRING)
        formatted = str(x) + ';' + str(y) + '\n'
        conn.sendall(formatted)
    elif(data[:UPDATE_SIZE] == UPDATE_STRING)
        current_x,current_y = data[:UPDATE_SIZE+1].split(";")

    print
