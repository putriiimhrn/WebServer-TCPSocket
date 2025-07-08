from socket import * # import modul socket
import sys           # import modul sys untuk terminasi program

# fungsi untuk mengirim pesan request
def send_request(server_IP, server_port, filename):
    client_socket = socket(AF_INET, SOCK_STREAM)        # set tipe soket menggunakan alamat IPv4 dan soket TCP
    # mencoba jalankan bagian blok ini terlebih dahulu, jika ada error maka masuk ke blok 'except'
    try: 
        client_socket.connect((server_IP, server_port)) # connect to server

    #jika server tidak tersedia, karena sibuk atau salah alamat, masuk ke except
    except:
        print("The server is not available")                                       # print server sedang sibuk
        client_socket.close()                                                      # menutup koneksi socket
        sys.exit()                                                                 # menutup program
    print(f"[CONNECTED] Client connected to server at {server_IP}:{server_port}")  # menampilkan sudah connect dgn server

    # send http request
    request_header = f'GET /{filename} HTTP/1.1\r\nHost: {server_IP}:{server_port}\r\n\r\n' # request file ke server dgn format sbb
    client_socket.send(request_header.encode())                                             # mengirim pesan request ke server setelah diubah jadi byte

    # menampilkan response dan isi file (jika ada) dari server
    print("Server HTTP Response:\r\n")

    # loop diperlukan untuk menerima data sampai seluruh response telah dikirim
    # jika tidak ada response baru, maka timeout
    data = ""                                       # buat variable 'data' untuk meyimpan keseluruhan pesan respons server
    while True:                                     # loop forever
        client_socket.settimeout(5)                 # client socket akan timeout bila tidak ada data baru
        newData = client_socket.recv(1024).decode() # panjang newData akan 0 jika client socket timeout
        data += newData                             # 'newData' ditaruh di 'data'
        if len(newData) == 0:                       # akan keluar loop jika tidak ada data baru
            break                                   # keluar loop
    print(data)                                     # print data

    # matikan socket
    print("\nClosing socket . . .")     # print ke server bahwa socket telah ditutup
    client_socket.close()               # menutup koneksi socket

# define main pd python
if __name__ == '__main__':
    # cek jumlah argument sudah sesuai
    if len(sys.argv) != 4:                                                   # jika argument yang diminta bukan sama dengan 4 masuk if
        print(f"format: {sys.argv[0]} <server_IP> <server_port> <filename>") # jika format masukan salah
    else:                                                                    # jika jumlah argumen ada 4 masuk else
        server_IP, server_port, filename = sys.argv[1:]                      # set server ip, port, dan filename dari argument kedua sampai akhir
        send_request(server_IP, int(server_port), filename)                  # manggil fungsi send_request

