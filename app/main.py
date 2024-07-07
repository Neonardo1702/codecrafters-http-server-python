# Uncomment this to pass the first stage
import os
import argparse
import socket

def compression(header,body,com_type) -> tuple:
    # Compression Handling
    supported_encodings = ["gzip"]

    out_header = header.copy()
    out_body = body
    
    if com_type in supported_encodings:
        out_header["Content-Encoding"] = com_type
        # gzip out body

    return out_header, out_body



def respond(input: str) -> tuple:
    decoded = input.split("\r\n")
    target, header, body = decoded[0], decoded[1:-2], decoded[-1]
    headers = {header_item.split(":")[0]:str("".join(header_item.split(":")[1:])).strip() for header_item in header}
    stat = "404 Not Found"
    out_header = {}
    out_body = "bwah"
    
    method = target.split(" ")[0]
    endpoint = target.split(" ")[1].split("/")
    func = endpoint[1]
    if func == "":
        stat = "200 OK"
    if func == "echo":
        stat = "200 OK"
        out_body = endpoint[2]
        out_header["Content-Type"]="text/plain"
    if func == "user-agent" and "User-Agent" in headers:
        stat = "200 OK"
        out_body = headers["User-Agent"].strip()
        out_header["Content-Type"]="text/plain"
    if func == "files":
        filepath = os.path.join(DIR,*endpoint[2:])
        print(filepath)
        if method == "GET" and os.path.exists(filepath):
            stat = "200 OK"
            with open(filepath,"r",encoding="UTF-8") as f:
                out_body = f.read()
            out_header["Content-Type"]="application/octet-stream"

        if method == "POST":
            stat = "201 Created"
            with open(filepath,"w",encoding="UTF-8") as f:
                f.write(body)
            out_body = body
            out_header["Content-Type"]="text/plain"
    
    #handling compression

    if "Accept-Encoding" in headers:
        out_header, out_body = compression(header=out_header,body=out_body,com_type=headers["Accept-Encoding"])

    out_header["Content-Length"]=len(out_body)
    return stat,out_header,out_body
    

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--directory",
            type=str,
            required = False,
            default = ".",
            dest="directory"
    )
    args = parser.parse_args()
    DIR = args.directory
    main()
