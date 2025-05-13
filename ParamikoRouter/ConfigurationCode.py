import paramiko
import time
import tkinter.messagebox as m


class Connection:
    def __init__(self, server_ip, server_port, username, password, ssh_client=None):
        self.host = server_ip
        self.port = server_port
        self.username = username
        self.password = password
        self.ssh_client = ssh_client

    def Connect(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password,
                                    look_for_keys=False, allow_agent=False)
            m.showinfo("Connection Checking...", "Connection is Successfully.... ")
        except paramiko.AuthenticationException:
            m.showinfo("Authentication Failed", "Please verify your credentials..")
        except paramiko.SSHException as sshException:
            m.showinfo("Connection Error", f"Unable to establish SSH connection: {sshException}")
        except Exception as e:
            m.showinfo("Operation error:", f"{e}")

    def get_shell(self):
        if self.ssh_client is None:
            raise Exception("SSH client is not connected. Call connect() first.")
        self.ssh_client.shell = self.ssh_client.invoke_shell()
        return self.ssh_client.shell

    def send_command(self, command, timeout=1):
        if not hasattr(self.ssh_client, 'shell'):
            raise Exception("Shell is not invoked. Call get_shell() first.")
        self.ssh_client.shell.send(command + "\n")
        time.sleep(timeout)

    def show(self, n=10000):
        if not hasattr(self.ssh_client, 'shell'):
            raise Exception("Shell is not invoked. Call get_shell() first.")
        output = self.ssh_client.shell.recv(n)
        return output.decode()

    def close(self):
        if self.ssh_client and self.ssh_client.get_transport().is_active():
            self.ssh_client.close()
            m.showinfo(f"Connection closed.", f"Connection Closing {self.host}... ")
        else:
            m.showinfo("NO Connection", "No active connection to close.")
