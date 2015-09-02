"""
interfaces/xmpp.py

Defines an xmpp interface for the bot
"""
from calamari.interfaces import CalamariInterface
import sys
import sleekxmpp

# The sleekxmpp docs reccomend having this...not very pythonic, might try
# removing it later because YOLO
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

class CalamariXMPP( CalamariInterface ):
    """
    An XMPP interface to the bot
    """
    def __init__(self, jid, password, room, nick):
        """
        Initialize the sleekxmpp object and register all the event handlers and
        plugins we're going to be using
        """
        self.xmpp = sleekxmpp.ClientXMPP(jid, password)
        self.room = room
        self.nick = nick
        self.xmpp.add_event_handler( "session_start", self.start )
        self.xmpp.add_event_handler( "groupchat_message", self.muc_message )
        self.xmpp.register_plugin('xep_0030') # Service Discovery
        self.xmpp.register_plugin('xep_0045') # Multi-User Chat
        self.xmpp.register_plugin('xep_0199') # XMPP Ping

    def start(self, event):
        """
        SleekXMPP event handler.  This gets run once the interface successfully 
        logs in.  Joins the specified chat room.
        """
        self.xmpp.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    def muc_message(self, msg):
        """
        SleekXMPP event handler.  This gets run every time a new message gets
        put in the chat room.  Note: even the bots messages will trigger this
        handler
        """
        # TODO: Actually define what constitutes a message somewhere
        self.process( {'message':msg['body'], 'user':msg['mucnick']} )

    def write_output( self, msg ):
        """
        Implementation of ABC's abstract write_output method.  Simply writes a
        message to the group chat
        """
        self.xmpp.send_message( mto=self.room, mbody=msg['message'],
                mtype="groupchat" )

    def run( self ):
        """
        Implementation of ABC's abstract run method.  Starts the interface.
        """
        self.xmpp.connect()
        self.xmpp.process( )
