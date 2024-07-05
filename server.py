import socket
import threading
import logging
import datetime

class ClientHandler(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address

    def run(self):
        received_data = ''  # untuk menyimpan data yang diterima
        while True:
            data = self.connection.recv(32)
            received_data += data.decode()
            if "\r\n\r\n" in received_data:
                break
            elif not data: 
                # Jika data kosong
                break  # keluar dari loop
        if received_data.strip() == "TIME":
            current_time = datetime.datetime.now().strftime('%X')
            current_time += "\r\n\r\n"  # Menambahkan delimiter
            self.connection.sendall(current_time.encode())

        self.connection.close()

class TimeServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # SOCK_STREAM digunakan untuk menentukan transport dengan TCP

    def run(self):
        self.server_socket.bind(('0.0.0.0', 45000))  # Mengikat socket ke semua alamat IP yang tersedia pada port 45000
        self.server_socket.listen(1)
        while True:
            connection, client_address = self.server_socket.accept()
            logging.warning(f"Koneksi dari {client_address}")
            
            client_thread = ClientHandler(connection, client_address)
            client_thread.start()
            self.clients.append(client_thread)

def main():
    server = TimeServer()
    server.start()

if __name__ == "__main__":
    main()
