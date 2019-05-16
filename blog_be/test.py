import socket


add = ('127.0.0.1',8000)
sock = socket.socket()
sock.bind(add)
sock.listen()

try:
    conn, radd = sock.accept()
    data = conn.recv(1024)
    print(data)
    ret_http ='HTTP/1.1 200 OK\n Content-Type:text/html\n Content-length:'
    with open(r'D:\magedu_python\img.jpg','rb') as f:
        info = f.read()
        length = len(info)
    ret_http = ret_http.encode()+ str(length).encode()  + b'\n\n'+ info
    send  = conn.sendall(ret_http)
    conn.send(info)
    conn.close()
    sock.close()
except Exception as e:print(e)
finally:
    sock.close()