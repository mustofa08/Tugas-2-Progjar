import socket
import logging
import threading

logging.basicConfig(level=logging.INFO)

def kirim_pesan(client_id="default"):
    # Membuat koneksi ke server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = ('localhost', 45000)
    s.connect(server_addr)
    logging.info(f"Klien {client_id} terhubung ke soket {server_addr}")

    try:
        # Mengirim pesan
        pesan = 'TIME\r\n\r\n'
        logging.warning(f"[KLIEN {client_id}] mengirim {pesan.encode()}")
        s.sendall(pesan.encode()) # Mengirim pesan 'TIME' ke server
        data_terkumpul = ''
        while True:
            data = s.recv(16) # Menerima data sebesar 16 byte
            data_terkumpul += data.decode()
            if "\r\n\r\n" in data_terkumpul:
                break
            else:
                break # keluar dari loop jika data kosong
            
        # Menghapus \r\n\r\n
        data_terkumpul = data_terkumpul.strip()
        logging.info(f"WAKTU {data_terkumpul}")
    finally:
        logging.warning("menutup koneksi")
        s.close()
    return

if __name__=='__main__':
    daftar_thread = []
    for i in range(5):
        t = threading.Thread(target=kirim_pesan, args=(i,))
        daftar_thread.append(t) # Menambahkan thread ke dalam daftar

    for t in daftar_thread:
        t.start() # Memulai setiap thread
