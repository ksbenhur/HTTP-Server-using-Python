# Overview:
This program implements a simple HTTP server using the python programming language. The server listens on a specified port and serves files from a specified directory. There are additional functionalities, like handling requests for specific routes or files, logging requests, and handling errors.

## Features and Functionalities:
### Request Handling:
- If the request doesn't follow the basic structure of an HTTP request, a 400 (Bad Request) response is sent.
- Requests to the root ("/") are automatically redirected to "/index.html".
- Any request starting with "/restricted" is treated as a forbidden resource, and a 403
  (Forbidden) response is sent.
- If the requested file exists in the specified directory, it is served to the client. Otherwise, a
  404 (Not Found) response is sent.

### Dispatcher Mechanism:
The web server is designed to handle incoming connections from clients over the 
network. It operates on a specified port, allowing clients to establish connections and 
retrieve files using the HTTP/1.0 and HTTP/1.1 protocols. When a client sends a 
request, the server parses the request to extract the requested filename and 
determines the appropriate file path within the server's document root directory. 

### Content Type Handling: 
The server can serve various file types, such as .html, .txt, .jpg, and .gif.

### Custom Port and Document Root: 
Through the use of command-line flags, the server can be started on a custom port (-port) and can serve files from a specified directory (-root).

### Client Request Handling:
When a client connects to the server and sends an HTTP request, the processClientRequest function reads the request, extracts the necessary headers, and delegates further handling to the handleRequest function.

### Timezone Handling: 
The program is set to recognize the Pacific timezone (America/Los Angeles) for logging purposes.

### Logging:
Every response from the server is logged to the console with a timestamp in the Pacific time zone, the HTTP status code, and the request URI.

# Usage:
```
- The command ‘python3 server.py -root './server_files' -port 9768' is used to 
run the file. - Open any web browser and try the following searches in the address bar: 
o localhost:9768 
o localhost:9768/index.html 
o localhost:9768/scu.jpg 
o localhost:9768/scu.gif 
o localhost:9768/restricted 
o as well as any other types to see error detection. 
o the port number can be changed accordingly in the command line. 
o appropriate logs are also available in the console 
```

### Screenshots attached in folder
- Url: http://localhost:9768/ SCU Home Page; Status Code: 200
- Url: http://localhost:9768/restricted; Private Url for which access is denied; Status Code: 403
- Supporting txt; Aboutproject.txt http://localhost:9768/Aboutproject.txt; Status Code: 200
- SCU GIF; url: http://localhost:9768/scu.gif; Status Code: 200
- SCU JPG: http://localhost:9768/scu.jpg; Status Code: 200
- Status Code: 400 Using Terminal: echo -ne "GET" | nc localhost 9768
