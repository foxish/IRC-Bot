#!/usr/bin/env python3

"""
    HOST     = "chat.freenode.net"
    PORT     = 6667
    NICK     = "statbot"
    IDENT    = "statbot"
    REALNAME = "DarkCthulhu"
    CHANNEL  = "##programming"
"""
import time
from IRCSession import IRCSession
from PLHandler import PLHandler

def process_line(line, handler):
    print(line.encode('utf-8'))
    handler.process(line)

def main():
    RETRYTIMEOUT = 10
    session = IRCSession("chat.freenode.net", 6667, "noyesnoyesno", "noyesnoyesno", "NoNoNo", "##programming")
    handler = PLHandler(session)
    
    while True:
        try:
            lines = session.get_lines()
            for line in lines:
                line = line.rstrip()
                process_line(line, handler)
        except Exception as e:
            print("Exception: ", e.args)
            print("Retrying in %s seconds" % RETRYTIMEOUT)
            time.sleep(RETRYTIMEOUT)
            
if __name__ == '__main__':
    main()
