import re
import time

from DB import DBHelper
from BaseHandler import BaseHandler

"""
To fix:
    Doesn't remove nick highlight before counting matches

"""

pl_dict = {
    'cpp'           : 'C++',
    'c++'           : 'C++',
    'c++11'         : 'C++',
    'c++0x'         : 'C++',
    'java'          : 'Java',
    'd'             : 'd',
    'c#'            : 'C#',
    'csharp'        : 'C#',
    'php'           : 'PHP',
    'vb'            : 'Visual Basic',
    'vb6'           : 'Visual Basic',
    'python'        : 'Python',
    'javascript'    : 'JavaScript',
    'ecmascript'    : 'JavaScript',
    'js'            : 'JavaScript',
    'c'             : 'C',
    'ruby'          : 'Ruby',
    'haskell'       : 'Haskell',
    'lisp'          : 'Lisp',
    'scheme'        : 'Scheme',
    'sql'           : 'SQL',
    'perl'          : 'Perl',
    'assembly'      : 'Assembly',
    'asm'           : 'Assembly',
    'apl'           : 'APL',
    'ml'            : 'ML',
    'lua'           : 'Lua',
    'golang'        : 'GoLang',
    'forth'         : 'Forth',
    'golang'        : 'GoLang',
    'erlang'        : 'Erlang',
    'rust'          : 'Rust'
}

DB_RECORD_TYPE = 'lang'
CMD_STAT = '!stats'

"""
Handler for programming language statistics
"""
class PLHandler(BaseHandler):
    def __init__(self, session):
        self.db = DBHelper('stats.db', 'plstats')
        super().__init__(session)
    
    def handle_msg(self, ident_string, recipient, msg):
        sender_nick = self.get_nick(ident_string)
        msg = msg[1:] #remove leading :
        
        if sender_nick == self.session.nick:
            return
        elif(recipient == self.session.nick):
            self._handle_priv_msg(msg, sender_nick)
        elif(recipient == self.session.channel):
            self._handle_channel_msg(msg)
            
    def _handle_priv_msg(self, msg, sender_nick):        
        global CMD_STAT
        if msg.startswith(CMD_STAT):
            self._display_stats(msg[len(CMD_STAT):], sender_nick)
    
    def _handle_channel_msg(self, msg):
        self._record_reference(msg)
        pass
        
    def _record_reference(self, msg):
        global pl_dict, DB_RECORD_TYPE
        
        for key, value in pl_dict.items():
            pattern = r'(^{0}$|.*\s+{0}\s+.*|^{0}\s+.*|.*\s+{0}([.,;!].*|$))'.format(re.escape(key))
            result = re.match(pattern, msg.lower())
            if not result is None:
                self.db.add_entry(DB_RECORD_TYPE, int(time.time()), value)
                #print("Found Entry: {0}".format(value))
                
    def _display_stats(self, command, sender_nick):
        command = command.strip()
        cmd_parts = command.split(" ")
        now_time = int(time.time())
        
        try:
            if command != "" and len(cmd_parts) == 1:
                low_time = (now_time - int(cmd_parts[0])*3600)
                db_out = str(self.db.get_categories_count(low_time, now_time, 5))
                self._send_msg(sender_nick, "Top mentions in the last {0} hour(s) : {1}".format(cmd_parts[0], db_out))
            
            elif len(cmd_parts) == 2:
                low_time = (now_time - int(cmd_parts[0])*3600)
                db_out = str(self.db.get_category_count(low_time, now_time, cmd_parts[1]))
                self._send_msg(sender_nick, "Number of mentions of {0} in the last {1} hour(s) : {2}".format(cmd_parts[1], cmd_parts[0], db_out))
            
            else:
                self._show_stats_help(sender_nick)
        except:
            pass
        
    def _get_time_tuple(self, num_hours):
        curr_time = int(time.time())
        return ((curr_time - int(num_hours)*3600, curr_time))
        
    def _show_stats_help(self, sender_nick):
        self._send_msg(sender_nick, "syntax: !stats <hours> [<language>]")
        
    def _send_msg(self, who, msg):
        self.session.send_data("PRIVMSG %s :%s\r\n" % (who, msg))
    
    def get_nick(self, ident_string):
        temp = ident_string.split("!")[0]
        return temp.lstrip(':')
