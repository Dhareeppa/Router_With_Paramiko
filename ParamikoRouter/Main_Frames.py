import customtkinter as ctk
import tkinter.messagebox as m
import Config_Cmd
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("950x600")
        self.iconbitmap("router.ico")
        self.title("Routing Configuration SSH Manager")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.protocolIP = None
        self.enable_password = None
        self.current_frame = None
        self.show_frame(MainFrame)

    def show_frame(self, FrameClass):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = FrameClass(self)
        self.current_frame.grid(row=0, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")

    def get_enable_password(self):
        dialog = ctk.CTkInputDialog(title="Enable Password", text="Enter the enable password:")
        self.enable_password = dialog.get_input()
        return self.enable_password

    def IP_netmask(self):
        dialogBox1 = ctk.CTkInputDialog(title="IP-Address", text="Enter tha [network-address] /[wildcard-mask] "
                                                                 "/area [area-id] :")
        input1 = dialogBox1.get_input()
        if not input1:
            m.showinfo("Error", "please Enter First IP-address")
            return None
        dialogBox2 = ctk.CTkInputDialog(title="IP-Address", text="Enter tha [network-address] /[wildcard-mask] "
                                                                 "/area [area-id] :")
        input2 = dialogBox2.get_input()
        if not input1:
            m.showinfo("Error", "please Enter First IP-address")
            return None
        self.protocolIP = f"{input1},{input2}"
        return self.protocolIP


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        heading = ctk.CTkLabel(self, text="-:Router-Information:-", font=("Arial", 15))
        heading.place(x=400, y=130)
        self.output_text = tk.Text(self, height=150, width=200, wrap=tk.WORD, bg="#313837", fg="#FFFFFF",
                                   font=("Arial", 12))
        self.output_text.pack(padx=10, pady=200)
        self.output_text.configure(state=tk.DISABLED)

        label1 = ctk.CTkLabel(self, text="Router_Ip = ", font=("Arial", 12))
        label1.place(x=20, y=20)
        label2 = ctk.CTkLabel(self, text="Router_Port = ", font=("Arial", 12))
        label2.place(x=240, y=20)
        label3 = ctk.CTkLabel(self, text="UserName = ", font=("Arial", 12))
        label3.place(x=465, y=20)
        label4 = ctk.CTkLabel(self, text="Password = ", font=("Arial", 12))
        label4.place(x=690, y=20)

        self.ip = ctk.CTkEntry(self)
        self.ip.place(x=90, y=20)
        self.portN = ctk.CTkEntry(self)
        self.portN.place(x=320, y=20)
        self.userN = ctk.CTkEntry(self)
        self.userN.place(x=545, y=20)
        self.passwd = ctk.CTkEntry(self, show="*")
        self.passwd.place(x=760, y=20)

        self.server = ctk.CTkButton(self, text="Connect-to-Server", font=("Arial", 12), fg_color="green",
                                    command=self.Connect_to_Server)
        self.server.place(x=20, y=80)

        self.next_button = ctk.CTkButton(self, text="Executing-Protocol", font=("Arial", 12), fg_color="green",
                                         command=lambda: parent.show_frame(ExecutingCmd), state=tk.DISABLED)
        self.next_button.place(x=180, y=80)

        self.protocol_button = ctk.CTkButton(self, text="show-Protocol", font=("Arial", 12),
                                             command=self.showProtocol, state=tk.DISABLED)
        self.protocol_button.place(x=340, y=80)

        self.config_button = ctk.CTkButton(self, text="show-Config-interface", font=("Arial", 12),
                                           command=self.showConfig, state=tk.DISABLED)
        self.config_button.place(x=500, y=80)

        self.running_button = ctk.CTkButton(self, text="show-Running", font=("Arial", 12),
                                            command=self.showRunning, state=tk.DISABLED)
        self.running_button.place(x=660, y=80)

        self.close_button = ctk.CTkButton(self, text="close", font=("Arial", 15), fg_color="red",
                                          hover_color="dark red", command=self.connClose)
        self.close_button.place(x=20, y=450)

    def update_output(self, text):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state=tk.DISABLED)

    def showProtocol(self):
        enable_password = self.parent.get_enable_password()
        if enable_password:
            protocol_data = Config_Cmd.showProtocol(self.parent.connection, enable_password)
            self.update_output(protocol_data)
        else:
            m.showinfo("Error", "Enable password is required.")

    def showConfig(self):
        enable_password = self.parent.get_enable_password()
        if enable_password:
            config_data = Config_Cmd.showIntConfig(self.parent.connection, enable_password)
            self.update_output(config_data)
        else:
            m.showinfo("Error", "Enable password is required.")

    def showRunning(self):
        enable_password = self.parent.get_enable_password()
        if enable_password:
            ShowConfig_data = Config_Cmd.showRunning(self.parent.connection, enable_password)
            self.update_output(ShowConfig_data)
        else:
            m.showinfo("Error", "Enable password is required.")

    def connClose(self):
        self.parent.quit()

    def Connect_to_Server(self):
        server_ip = self.ip.get()
        server_port = self.portN.get()
        username = self.userN.get()
        password = self.passwd.get()

        if server_ip == "" or server_port == "" or username == "" or password == "":
            m.showinfo("Invalid Input", "Please fill in all fields... ")
        try:
            server_port = int(server_port)
        except ValueError:
            m.showinfo("Input Error", "Port number must be an integer.")
            return
        try:
            Server_connection = Config_Cmd.connect(server_ip, server_port, username, password)
            if Server_connection:
                self.parent.connection = Server_connection
                self.next_button.configure(state=tk.NORMAL)
                self.protocol_button.configure(state=tk.NORMAL)
                self.config_button.configure(state=tk.NORMAL)
                self.running_button.configure(state=tk.NORMAL)
            else:
                m.showinfo("Connection Error", "Failed to connect to the server.")
        except Exception as e:
            m.showinfo("Connection Error", f"An error occurred: {str(e)}")


class ExecutingCmd(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        meg = ctk.CTkLabel(self, text="-:Select The Routing Protocol:-", font=("Arial", 12))
        meg.pack(pady=20)

        button1 = ctk.CTkButton(self, text="RIP protocol", command=self.rip_protocol)
        button1.pack(pady=10)

        button2 = ctk.CTkButton(self, text="OSPF protocol", command=self.ospf_protocol)
        button2.pack(pady=10)

        button3 = ctk.CTkButton(self, text="EIGRP protocol", command=self.eigrp_protocol)
        button3.pack(pady=10)

        meg1 = ctk.CTkLabel(self, text="-:You Do NOT Like this Please EXIT Here:-", font=("Arial", 12))
        meg1.pack(pady=20)

        exit_button = ctk.CTkButton(self, text="EXIT", command=self.exitCommand, fg_color="red", hover_color="dark red")
        exit_button.pack(pady=10)
        exit_button = ctk.CTkButton(self, text="BACK", command=self.back_to_main, fg_color="red",
                                    hover_color="dark red")

        exit_button.pack(pady=10)

    def rip_protocol(self):
        enable_password = self.parent.get_enable_password()
        ip_add = self.parent.IP_netmask()
        if enable_password:
            output = Config_Cmd.CMDrip(self.parent.connection, enable_password, ip_add)
            m.showinfo("RIP Configuration", output)
        else:
            m.showinfo("Error", "Enable password is required.")

    def ospf_protocol(self):
        enable_password = self.parent.get_enable_password()
        ip_add = self.parent.IP_netmask()
        if enable_password:
            output = Config_Cmd.OspfCmd(self.parent.connection, enable_password, ip_add)
            m.showinfo("OSPF Configuration ", output)
        else:
            m.showinfo("Error", "Enable password is required.")

    def eigrp_protocol(self):
        enabl_password = self.parent.get_enable_password()
        ip_add = self.parent.IP_netmask()
        if enabl_password:
            output = Config_Cmd.EigrpCmd(self.parent.connection, enabl_password, ip_add)
            m.showinfo("EIGRP Configuration", output)
        else:
            m.showinfo("Error", "Enable password isd required.")

    def exitCommand(self):
        if self.parent.connection:
            self.parent.connection.close()
        self.parent.quit()

    def back_to_main(self):
        self.parent.show_frame(MainFrame)


if __name__ == "__main__":
    app = App()
    app.mainloop()
