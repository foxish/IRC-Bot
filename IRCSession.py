import socket

class IRCSession(object):
    def __init__(self, host, port, nick, ident, realname, channel):
        self.host = host
        self.port = port
        self.nick = nick
        self.ident = ident
        self.realname = realname
        self.channel = channel
        self.recv = ""
        self._init_session()
        
    def _init_session(self):        
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))
        self.send_data("NICK %s\r\n" % self.nick)
        self.send_data("USER %s %s bla :%s\r\n" % (self.ident, self.host, self.realname))
        self.send_data(":source JOIN :%s\r\n" % self.channel)
    
    # returns a list of lines
    def get_lines(self):
        self.recv += self.get_data()
        lines = self.recv.split("\n")
        self.recv = lines.pop()
        return lines
    
    def get_data(self):
        return self.sock.recv(1024).decode('UTF-8')
        
    def send_data(self, str_out):
        self.sock.send(bytes(str_out, 'UTF-8'))
        
    def get_channel(self):
        return self.channel
        
    def get_nick(self):
        return self.nick
        
    def get_ident(self):
        return self.ident
