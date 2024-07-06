# Uncomment this to pass the first stage
import socket

def respond(input: str) -> tuple:
    decoded = input.split("\r\n")
    target, header, body = decoded[0], decoded[1:-2], decoded[-1]
    headers = {header_item.split(":")[0]:"".join(header_item.split(":")[1:]) for header_item in header}
    stat = "404 Not Found"
    out_header = {}
    body = "bwah"
    
    endpoint = target.split(" ")[1].split("/")
    func = endpoint[1]
    if func == "":
        stat = "200 OK"
    if func == "echo":
        stat = "200 OK"
        body = endpoint[2]
        out_header["Content-Type"]="text/plain"
        out_header["Content-Length"]=len(body)
    if func == "user-agent" and "User-Agent" in headers:
        stat = "200 OK"
        body = headers["User-Agent"].strip()
        out_header["Content-Type"]="text/plain"
        out_header["Content-Length"]=len(body)
        
    return stat,out_header,body
    

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client, addr = server_socket.accept()
        print(addr)
        data = client.recv(2048).decode()
        response_status,response_header, response_body = respond(input = data)
        out_headers = [f"{key}: {value}" for key, value in response_header.items()]
        out_header = "\r\n".join(out_headers)
        
        response = f"HTTP/1.1 {response_status}\r\n{out_header}\r\n\r\n{response_body}"
        client.send(response.encode())
        if response_status == "TERMINATE":
            break

if __name__ == "__main__":
    main()
