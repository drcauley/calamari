from calamari.interfaces import CalamariInterface
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl
from threading import Thread

class IRCBot( irc.IRCClient ):
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        self.interface.process( {'message':msg, 'user':user} )

    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'

    def threadSafeMsg(self, channel, msg ):
        reactor.callFromThread( self.msg, channel, msg )

class IRCBotFactory(protocol.ClientFactory):
    """A factory for IRCBots

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, interface):
        self.interface = interface
        self.channel = interface.channel

    def buildProtocol(self, addr):
        p = IRCBot()
        p.nickname = self.interface.nickname
        p.username = self.interface.username
        p.password = self.interface.password
        p.interface = self.interface
        self.interface.bot_instance = p
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

class CalamariIRC( CalamariInterface ):
    def __init__( self, irc_server, irc_port, channel, nickname,
            use_ssl = False, username = None, password = None ):
        """
        Initialize the irc interface
        """
        self.irc_server = irc_server
        self.irc_port = irc_port
        self.channel = channel
        self.nickname = nickname
        self.use_ssl = use_ssl
        self.username = username
        self.password = password

    def write_output( self, msg ):
        """
        writes message to the irc channel
        """
        self.bot_instance.threadSafeMsg("#" + self.channel, str(msg['message']))

    def run( self ):
        """
        start the main server thread
        """
        t = Thread( target = self.server_thread )
        t.daemon = True
        t.start()

    def server_thread( self ):
        f = IRCBotFactory( self )
        if self.use_ssl:
            reactor.connectSSL( self.irc_server, self.irc_port, f,
                    ssl.ClientContextFactory() )
        else:
            reactor.connectTCP( self.irc_server, self.irc_port, f )
        reactor.run(installSignalHandlers=False)
