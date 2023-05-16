import socket
import threading


HOST = '127.0.0.1'
PORT = 55555

users = {'user1': 'password1', 'user2': 'password2', 'user3': 'password3'}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

# Функция отправки сообщений всем клиентам
def broadcast(message):
    for client in clients:
        client.send(message)

# Функция обработки сообщений от клиента
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} покинул чат!'.encode())
            usernames.remove(username)
            break

# Функция приема клиентов
def receive():
    while True:

        client, address = server.accept()
        print(f'Подключено: {str(address)}')

        client.send('Логин:'.encode())
        login = client.recv(1024).decode()
        client.send('Пароль:'.encode())
        password = client.recv(1024).decode()

        
        if login in users and users[login] == password:
            usernames.append(login)
            clients.append(client)

            print(f'Имя клиента: {login}')
            broadcast(f'{login} присоединился к чату!'.encode())
            client.send('Подключено к чату!'.encode())

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            client.send('Ошибка авторизации!'.encode())
            client.close()

print('Сервер запущен!')
receive()


