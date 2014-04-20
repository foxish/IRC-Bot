#generic handlers for IRC
import re

class BaseHandler(object):
    def __init__(self, session):
        self.session = session
                
    def process(self, line):
        m_object = re.search(r':?([^:]+)(.*)$', line)
        header = m_object.group(1).rstrip()
        msg = m_object.group(2).rstrip()
        
        if header == "PING":
            self.handle_ping(msg)
        else:
            header_parts = header.split()
            if len(header_parts) == 3:
                ident_string, command, recipient = header_parts
                if command == "PRIVMSG":
                    self.handle_msg(ident_string, recipient, msg)
                elif command == 'PART' or command == 'JOIN':
                    pass
    
    def handle_ping(self, server):
        self.session.send_data("PONG %s\r\n" % server)
    
    def handle_msg(self, ident_string, recipient, msg):
        pass
