# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client, addr = server_socket.accept()
    print(addr)
    data = client.recv(2048).decode()
    decoded = data.split("\r\n")
    target, header, body = decoded[0], decoded[1:-2], decoded[-1] 
    response_status = "200 OK"
    response_body = f"your address is {addr}"
    if target.split(" ")[1] != "/":
        response_status = "404 Not Found"


    response = f"HTTP/1.1 {response_status}\r\n\r\n{response_body}"
    client.send(response.encode())

if __name__ == "__main__":
    main()
