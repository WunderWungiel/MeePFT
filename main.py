#!/opt/python.3.9.18/bin/python3.9

import sys
import http.server
import socketserver
import socket
import os
import configparser

import lib.tui as tui

config_dir = os.path.abspath("/opt/MeePFT/config")

config = configparser.ConfigParser()
config.read(config_dir)

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
bold = '\033[1m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[38;5;104m'
cyan_background = '\033[48;5;104m'

port = int(config['meepft']['port'])
dir = config['meepft']['dir']
ip_address = '127.0.0.1'

class quietServer(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def write_config_file():
    with open(config_dir, 'w') as configfile:
        config.write(configfile)

class Options_Actions():
    def __init__(self):
        port = int(config['meepft']['port'])
        dir = config['meepft']['dir']
        self.port = port
        self.dir = dir
        result = self.get_ip()
        if result == "Error":
            self.error = True
        else:
            self.ip_address = result

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
        except OSError:
            print(f" {red}OSError occured.{reset}")
            print(" Network may be unreachable. Check your Wi-Fi connection.")
            input(f" {cyan}Press any key to Exit...{reset}")
            sys.exit(0)
        return s.getsockname()[0]

    def start_server(self):

        os.chdir(self.dir)
        httpd = socketserver.TCPServer(("", self.port), quietServer)
        print(f" HTTP server working on port {cyan}'{self.port}'{reset}")
        print(f" Visit {self.ip_address}:{self.port} in browser.")
        print(f" Press Ctrl + C to stop...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f" Stopping server...")
            httpd.shutdown()
            httpd.server_close()
            tui.press_enter()
        except OSError:
            print(f" {red}OSError occured.{reset}")
            print(f" Network may be unreachable or port in use.")
            input(f" {cyan}Press any key to Exit...{reset}")
            return

    def port_change(self):
        port = self.port
        while True:
            tui.frame(text="Change port")
            print(f" Current port: {cyan}'{port}'{reset}.")
            print(f" Input new port or press Enter to keep current: ", end='')

            answer = input()

            if answer == "":
                answer = self.port
                break
            if not answer.isnumeric() or not len(answer) == 4:
                print(f"{red} Port should be an 4-digits long integer...{reset}")
                continue
            else:
                break

        self.port = int(answer)
        config['meepft']['port'] = str(self.port)
        write_config_file()
        print(f" New port: {cyan}'{self.port}'{reset}.")
        tui.press_enter()
        return "Changed_port"

    def dir_change(self):
        dir = self.dir
        tui.clean()
        while True:
            tui.frame(text="Change directory")
            print(f" Current directory: {cyan}'{dir}'{reset}.")
            print(f" Input new directory or press Enter to keep current: ", end='')

            answer = input()

            if not os.path.isdir(answer):
                print(f"{red} Directory doesn't exist...    {reset}", time=0.03)
                continue
            else:
                break

        self.dir = os.path.abspath(answer)
        config['meepft']['dir'] = self.dir
        write_config_file()
        print(f" New directory: {cyan}'{self.dir}'{reset}.")
        tui.press_enter()

    def about(self):

        tui.frame(
            text = f"""{cyan}MeePFT{reset}© 2023 WunderWungiel
Version: {bold}{bold}0.0.1{reset}

A simple Python HTTP wrapper
written using Python 3.

Join our Telegram group:

https://t.me/linuxmobile_world"""
        )

        tui.press_enter()
        tui.clean()

    def donate(self):

        tui.frame(
            text = f"""{cyan}{bold}Donating{reset}
            
If you want to donate for my
small work, you can do it here:

donationalerts.com/r/WunderWungiel

Thank you for every 
$, €, £, zł, etc., etc. ♥

This really motivates.""",
            second_frame=False
        )

        tui.press_enter()
        tui.clean()

    def exit(self):
        sys.exit(0)

def main():

    while True:

        port = int(config['meepft']['port'])

        options_actions = Options_Actions()

        text = f"""Welcome to MeePFT!
(current port: {cyan}'{port}'{reset})"""

        options = {
            "Start": options_actions.start_server,
            "Change port": options_actions.port_change,
            "Change directory": options_actions.dir_change,
            "Donate": options_actions.donate,
            "About": options_actions.about,
            "Exit": options_actions.exit
        }

        result = tui.menu(text=text, options=options)

if __name__ == "__main__":
    main()
