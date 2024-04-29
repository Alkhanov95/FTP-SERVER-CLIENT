import socket 
import os

def list_files():
    files = os.listdir()
    return '\n'.join(files)

def mkdir(directory_name):
    os.mkdir(directory_name)
    return f"Directory '{directory_name}' created."

def rmdir(directory_name):
    os.rmdir(directory_name)
    return f"Directory '{directory_name}' deleted."

def delete(file_name):
    os.remove(file_name)
    return f"File '{file_name}' deleted."

def rename(old_name, new_name):
    os.rename(old_name, new_name)
    return f"File '{old_name}' renamed to '{new_name}'."

def upload(file_name, file_data):
    with open(file_name, 'wb') as file:
        file.write(file_data)
    return f"File '{file_name}' uploaded."

def download(file_name):
    with open(file_name, 'rb') as file:
        file_data = file.read()
    return file_data

s = socket.socket()
host = socket.gethostname()
port = 8080
s.bind((host, port))
s.listen(1)
print("ваш хост", host)
print("Server is listening...")

conn, addr = s.accept()
print("Connection established with:", addr)

while True:
    command = conn.recv(1024).decode()
    if not command:
        break
    command_parts = command.split()
    action = command_parts[0]
    response = ""

    if action == "LIST":
        response = list_files()
    elif action == "MKDIR":
        response = mkdir(command_parts[1])
    elif action == "RMDIR":
        response = rmdir(command_parts[1])
    elif action == "DELETE":
        response = delete(command_parts[1])
    elif action == "RENAME":
        response = rename(command_parts[1], command_parts[2])
    elif action == "UPLOAD":
        file_name = command_parts[1]
        file_data = conn.recv(1024)
        response = upload(file_name, file_data)
    elif action == "DOWNLOAD":
        file_name = command_parts[1]
        file_data = download(file_name)
        conn.send(file_data)
        continue  # Skip sending response for download command
    elif action == "EXIT":
        print("Client disconnected.")
        break
    else:
        response = "Invalid command."

    conn.send(response.encode())

conn.close()
