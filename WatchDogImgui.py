import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer

import time
import socket
import threading




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
        imgui.text("IP:")
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
        imgui.set_cursor_pos_y(imgui.get_window_height() - 20)
        imgui.text(f"Listening: {self.isListening}")




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
                imgui.text("Log...")
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


    def StopServer(self):
        self.s.close()

        self.isListening = False




    
    def ListeningForClients(self):
        while self.running:
            if self.isListening:
                try:
                    try:
                        conn, addr = self.s.accept()
                        conn.settimeout(self.socket_timeout_clients)  # 2 seconds timeout
                        self.data_clients.append([conn, addr[0], "Alpha", "John-PC", "Windows 10", "2h 15m", "Chrome", "False"])
                        
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

                if (time.time() - ping_time) > 10:
                    ping_time = time.time()
                    # print("ping")

                    for i in range(len(self.data_clients)):
                        if not self.cmd_test_connection(i):
                            self.data_clients.pop(i)

            time.sleep(2)





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
                self.data_clients[index][0].send(bytes("Write-Output 'ping'", "utf-8"))
                self.data_clients[index][0].recv(64).decode("utf-8")
                return 1
            except socket.timeout:
                return 0
        except:
            return 0



    

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























"""




import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer


data_rows = [
    ["192.168.10.141", "Alpha", "John-PC", "Windows 10", "2h 15m", "Chrome", "False"],
    ["192.168.10.112", "Beta", "Alice-Laptop", "Linux", "4h 45m", "Terminal", "False"],
    ["192.168.10.107", "Gamma", "Bob-Work", "Windows 11", "1h 12m", "Visual Studio", "False"],
]

def impl_glfw_init():
    width, height = 900, 450
    window_name = "ImGui TreeView with Context Menu"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

    window = glfw.create_window(width, height, window_name, None, None)
    glfw.make_context_current(window)
    return window

def main():
    global data_rows
    window = impl_glfw_init()
    imgui.create_context()
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        imgui.set_next_window_size(1280, 550)
        imgui.set_next_window_position(0, 0)
        imgui.begin("Main Window")

        if imgui.begin_tab_bar("Tabs"):
            if imgui.begin_tab_item("Tab 1")[0]:
                imgui.columns(7, "tree_columns")
                imgui.set_column_width(0, 120)
                imgui.set_column_width(1, 110)
                imgui.set_column_width(2, 150)
                imgui.set_column_width(3, 120)
                imgui.set_column_width(4, 120)
                imgui.set_column_width(5, 120)
                imgui.set_column_width(6, 200)

                headers = ["IP", "Assigned Name", "Computer User", "OS", "Uptime", "Active Window", "Admin Privileges"]

                # Table headers
                for header in headers:
                    imgui.text(header)
                    imgui.next_column()
                imgui.separator()

                # Render each row
                for i, row in enumerate(data_rows):
                    is_hovered = False
                    for j, cell in enumerate(row):
                        imgui.text(cell)
                        # Check hover state for all cells in the row
                        if imgui.is_item_hovered():
                            is_hovered = True
                        imgui.next_column()

                    # If right-clicked anywhere on the row, open context menu
                    if is_hovered and imgui.is_mouse_clicked(imgui.MOUSE_BUTTON_RIGHT):
                        imgui.open_popup(f"context_menu_row_{i}")

                    # Popup per row
                    if imgui.begin_popup(f"context_menu_row_{i}"):
                        if imgui.menu_item("Remove")[0]:
                            data_rows.pop(i)
                            imgui.end_popup()
                            break  # stop loop since data changed
                        imgui.end_popup()

                imgui.columns(1)
                imgui.end_tab_item()

            if imgui.begin_tab_item("Tab 2")[0]:
                imgui.text("This is Tab 2.")
                imgui.end_tab_item()
            if imgui.begin_tab_item("Tab 3")[0]:
                imgui.text("This is Tab 3.")
                imgui.end_tab_item()
            if imgui.begin_tab_item("Tab 4")[0]:
                imgui.text("This is Tab 4.")
                imgui.end_tab_item()
            imgui.end_tab_bar()

        imgui.end()
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()




"""