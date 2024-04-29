import socket 

s = socket.socket()
host = input("Please enter the server address: ")
port = 8080 
s.connect((host, port))
print("Connected to server.")

while True:
    command = input("Enter command: ").encode()
    s.send(command)
    if command.decode().split()[0] == "EXIT":
        print("Connection closed by client.")
        break
    response = s.recv(1024).decode()
    print(response)

s.close()
