from socket import *    # import modul socket
import sys              # import modul sys untuk terminasi program

# fungsi untuk menangani request dari server
def handle_request(connectionSocket, client_address): 
    # mencoba jalankan bagian blok ini terlebih dahulu, jika ada error maka masuk ke blok 'except'
    try:
        # decode file
        message = connectionSocket.recv(1024).decode() # menerima pesan request dari klien dgn max data 1024 byte dan diubah ke string
        filename = message.split()[1]                  # membagi pesan request klien dan diambil path file yang diminta klien
        f = open(filename[1:], "rb")                   # file dibuka dari indeks kedua sampai akhir dengan format rawbyte
        outputdata = f.read()                          # membaca isi file yang telah dibuka dan disimpan di 'outputdata'
        f.close()                                      # menutup file yang telah dibuka
 
        # send http response OK
        header = "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\r\n\r\n"  # header HTTP yang akan dikirim sebagai respons ke klien dengan status "200 OK",tipe konten html, dan charset=utf-8 untuk menerima ASCII text
        connectionSocket.send(header.encode())                                      # mengirim header yang telah diubah menjadi byte
        print(f'Connection from {client_address}')                                  # menampilkan alamat client yg terconnect
        print("Response: HTTP/1.1 200 OK")                                          # print respons "200 OK" pada server
        connectionSocket.send(outputdata)                                           # krn pakai rawbyte, data dijadikan 1 byte, maka bisa send output data tanpa harus di-iterate
        connectionSocket.close()                                                    # menutup koneksi socket

    # bila error masuk ke blok 'except'
    except IOError:
        # send http response Not Found
        header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" # header HTTP yang akan dikirim sebagai respons ke klien dengan status "404 Not Found", tipe konten html, dan charset=utf-8 untuk menerima ASCII text
        connectionSocket.send(header.encode())                                              # mengirim header yg telah diubah ke byte
        print(f'Connection from {client_address}')                                          # menampilkan alamat client yg terconnect
        print("Response: HTTP/1.1 404 Not Found")                                           # print respons "404 Not Found" pd server
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())  # kirim 404 Not Found ke klien di browser
        connectionSocket.close()                                                            # menutup koneksi socket
    print("\n===============================================\n")                            # print pemisah untuk setiap koneksi

# fungsi untuk menjalankan server
def start_server():
    # set socket
    server_socket = socket(AF_INET, SOCK_STREAM)  # set tipe soket menggunakan alamat IPv4 dan soket TCP
    server_IP = "localhost"                       # server ip di set "localhost"
    server_port = 80                              # server port di set 80
    server_socket.bind((server_IP, server_port))  # mengikat server soket dan server ip yang sudah ditentukan sebelumnya
    server_socket.listen(1)                       # membuat server mendengarkan koneksi dari klien dengan jumlah maksimum 1 koneksi yang di handle sekaligus

    print(f"[LISTENING] Server is listening on {server_IP}:{server_port}") # print pesan bahwa server sedang mendengar koneksi pada alamat ip dan port yang telah ditentukan
    print("===============================================\n")             # print pemisah untuk setiap koneksi
    
    # loop forever
    while True: 
        connection_socket, client_address = server_socket.accept()  # meng-accept koneksi dan address klien ditaruh di 'client_address'
        handle_request(connection_socket, client_address)           # memanggil procedure handle_request()
    connectionSocket.close()                                        # menutup koneksi socket
    sys.exit()                                                      # menutup program

if __name__ == '__main__':  # define main pd python
    start_server()          # memanggil procedure start_server()