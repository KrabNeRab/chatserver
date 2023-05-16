import socket
import threading


HOST = '127.0.0.1'
PORT = 55555

username = input('Логин: ')
password = input('Пароль: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))



# Функция приема сообщений от сервера
def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'Логин:':
                client.send(username.encode())
            elif message == 'Пароль:':
                client.send(password.encode())
            else:
                print(message)
        except:
            print('Ошибка подключения к серверу!')
            client.close()
            break

# Функция отправки сообщений серверу
def write():
    while True:
        message = f'{username}: {input()}'
        client.send(message.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()