# Uncomment this to pass the first stage
import socket

def respond(input: str) -> tuple:
    decoded = input.split("\r\n")
    target, header, body = decoded[0], decoded[1:-2], decoded[-1]
    
    stat = "404 Not Found"
    header = {}
    body = "bwah"
    
    endpoint = input.split(" ")[1].split("/")
    func = endpoint[1]
    if func == "":
        stat = "200 OK"
    if func == "echo":
        stat = "200 OK"
        body = endpoint[2]
        header["Content-Type"]="text/plain"
        header["Content-Length"]=len(body)
    
    return stat,header,body
    

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client, addr = server_socket.accept()
    print(addr)
    data = client.recv(2048).decode()
    response_status,response_header, response_body = respond(input = data)

    out_headers = [f"{key}: {value}" for key, value in response_header.items()]
    out_header = "\r\n".join(out_headers)

    response = f"HTTP/1.1 {response_status}\r\n{out_header}\r\n\r\n{response_body}"
    client.send(response.encode())

if __name__ == "__main__":
    main()
