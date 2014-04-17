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
import re
from IRCSession import IRCSession

def process_line(line, session):
    print(line)
    
    m_object = re.search(r':?([^:]+)(.*)$', line)
    header = m_object.group(1).rstrip()
    msg = m_object.group(2).rstrip()
    
    if header == "PING":
        handlePing(session, msg)
    else:
        header_parts = header.split()
        if len(header_parts) == 3:
            ident_string, command, recipient = header_parts
            if command == "PRIVMSG":
                handlePrivMsg(session, ident_string, recipient, msg)
            elif command == 'PART' or command == 'JOIN':
                pass

def handlePing(session, recipient):
    session.send_data("PONG %s\r\n" % recipient)

def handlePrivMsg(session, ident_string, recipient, msg):
    if get_nick(ident_string) == session.nick:
        return
    elif(recipient == session.nick):
        session.send_data("PRIVMSG %s :%s\r\n" % (get_nick(ident_string), "Did I screw up? :( Tell DarkCthulhu to deactivate me!"))
    elif(recipient == session.channel and msg.strip() == ":!stats"):
        session.send_data("PRIVMSG %s :%s\r\n" % (session.channel, "[Stats]"))
    
def get_nick(ident_string):
    temp = ident_string.split("!")[0]
    return temp.lstrip(':')
    
def main():
    RETRYTIMEOUT = 10    
    session = IRCSession("chat.freenode.net", 6667, "Xstatbot", "Xstatbot", "DarkCthulhu", "##whatthefuck")
    while True:
        try:
            lines = session.get_lines()
            for line in lines:
                line = line.rstrip()
                process_line(line, session)
        except Exception as e:
            print("Exception: ", e.args)
            print("Retrying in %s seconds" % RETRYTIMEOUT)
            time.sleep(RETRYTIMEOUT)
            
if __name__ == '__main__':
    main()
