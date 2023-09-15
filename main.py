#!/opt/bin/python3.9

import sys
import http.server
import socketserver
import socket
import lib.tui as tui

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
bold = '\033[1m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[38;5;104m'
cyan_background = '\033[48;5;104m'

port = 8000
ip_address = '127.0.0.1'

class quietServer(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

class Options_Actions():
    def __init__(self):
        global port
        self.port = port
        self.ip_address = self.get_ip()

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def start_server(self):
        httpd = socketserver.TCPServer(("", self.port), quietServer)
        tui.rprint(f" HTTP server working on port {cyan}'{self.port}'{reset}")
        tui.rprint(f" Visit {self.ip_address}:{self.port} in browser.")
        tui.rprint(f" Press Ctrl + C to stop...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            tui.rprint(f" Stopping server...")
            httpd.shutdown()
            httpd.server_close()
            tui.press_enter() 

    def port_change(self):
        port = self.port
        while True:
            tui.frame(text="Change port")
            tui.rprint(f" Current port: {cyan}'{port}'{reset}.")
            tui.rprint(f" Input new port or press Enter to keep current: ", _end='')

            answer = input()

            if answer == "":
                answer = self.port
                break
            if not answer.isnumeric() or not len(answer) == 4:
                tui.rprint(f"{red} Port should be an 4-digits long integer...{reset}")
                continue
            else:
                break

        self.port = int(answer)
        print(f" New port: {cyan}'{self.port}'{reset}.")
        tui.press_enter()

    def about(self):

        tui.frame(
            f"""{cyan}MeePFT{reset}© 2023 WunderWungiel
Version: {bold}0.0.1{reset}

A simple Python HTTP wrapper
written using Python 3.

Join our Telegram group:

https://t.me/linuxmobile_world""",
            second_frame=True
        )

        tui.press_enter()
        tui.clean()

    def exit(self):
        sys.exit(0)

def main():
    options_actions = Options_Actions()

    text = f"""Welcome to MeePFT!
(current port: {cyan}'{port}'{reset})"""

    options = {
        "Start": options_actions.start_server,
        "Change port": options_actions.port_change,
        "About": options_actions.about,
        'Exit': options_actions.exit
    }

    while True:
        result = tui.menu(text=text, options=options)
        if result:
            return result

if __name__ == "__main__":
    main()