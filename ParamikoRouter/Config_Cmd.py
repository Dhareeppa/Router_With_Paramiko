import ConfigurationCode
import tkinter.messagebox as m


def connect(server_ip, server_port, username, password):
    Conn = ConfigurationCode.Connection(server_ip, server_port, username, password)
    Conn.Connect()
    return Conn


def EnablePassword(Conn, enable_password):
    try:
        Conn.send_command("enable")
        Conn.send_command(enable_password)
    except Exception as e:
        m.showinfo("Password Error", f"Incorrect Password: {str(e)} ")


def netmask(Conn, IP_Address):
    try:
        Conn.send_command(IP_Address)
    except Exception as e:
        m.showinfo("Error Network", f"Incorrect[network-address] [wildcard-mask]:{str(e)} ")


def showProtocol(Conn, enable_password):
    try:
        Conn.get_shell()
        Conn.send_command("enable")
        Conn.send_command(enable_password)
        Conn.send_command("terminal length 0")
        Conn.send_command("show ip route")
        output = ConfigurationCode.Connection.show(Conn)
        return output
    except Exception as e:
        m.showerror("Command Error", f"An error occurred while executing the command: {str(e)}")
        return None
    finally:
        Conn.close()


def showIntConfig(Conn, enable_password):
    try:
        Conn.get_shell()
        Conn.send_command("enable")
        Conn.send_command(enable_password)
        Conn.send_command("terminal length 0")
        Conn.send_command("show ip interface brief")
        output = ConfigurationCode.Connection.show(Conn)
        return output
        # m.showinfo("Showing Config...", output)
    except Exception as e:
        m.showerror("Command Error", f"An error occurred while executing the command: {str(e)}")
        return None
    finally:
        Conn.close()


def showRunning(Conn, enable_password):
    try:
        Conn.get_shell()
        Conn.send_command("enable")
        Conn.send_command(enable_password)
        Conn.send_command("terminal length 0")
        Conn.send_command("show running-config")
        output = ConfigurationCode.Connection.show(Conn)
        return output
    except Exception as e:
        m.showerror("Command Error", f"An error occurred while executing the command: {str(e)}")
        return None
    finally:
        Conn.close()


def CMDrip(Conn, enable_password, IP_Address):
    try:
        Conn.get_shell()
        Conn.send_command("enable")
        Conn.send_command(enable_password)
        Conn.send_command("terminal length 0")
        Conn.send_command("router rip ")
        Conn.send_command("version 2")
        Conn.send_command("network" + str(IP_Address))
        Conn.send_command("network" + str(IP_Address))
        Conn.send_command("Exit")
        Conn.send_command("show ip route")

        output = ConfigurationCode.Connection.show(Conn)
        m.showinfo("Output", output)
    except Exception as e:
        m.showerror("Command Error", f"An error occurred while executing the command: {str(e)}")
        return None
    finally:
        Conn.close()


def OspfCmd(Conn, enable_password, IP_Address):
    try:
        Conn.get_shell()
        Conn.send_command("enable")
        Conn.send_command(enable_password)
        Conn.send_command("terminal length 0")
        Conn.send_command("router ospf 1 ")
        Conn.send_command("network" + str(IP_Address) + "area 0")
        Conn.send_command("network" + str(IP_Address) + "area 0")
        Conn.send_command("Exit")
        Conn.send_command("show ip route")

        output = ConfigurationCode.Connection.show(Conn)
        m.showinfo("Output", output)
    except Exception as e:
        m.showerror("Command Error", f"An error occurred while executing the command: {str(e)}")
        return None
    finally:
        Conn.close()


def EigrpCmd(Conn, enable_password, IP_Address):
    try:
        Conn.get_shell()
        Conn.send_command("enable")
        Conn.send_command(enable_password)
        Conn.send_command("terminal length 0")
        Conn.send_command("router eigrp 100 ")
        Conn.send_command("network" + str(IP_Address))
        Conn.send_command("network" + str(IP_Address))
        Conn.send_command("Exit")
        Conn.send_command("show ip route")

        output = ConfigurationCode.Connection.show(Conn)
        m.showinfo("Output", output)
    except Exception as e:
        m.showerror("Command Error", f"An error occurred while executing the command: {str(e)}")
        return None
    finally:
        Conn.close()
