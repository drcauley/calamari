"""
interfaces/__init__.py

Defines an abstract base class for the bots interfaces to inherit from
"""
import abc
from Queue import Queue
from threading import Thread

class CalamariInterface(object):
    """
    Abstract interface to the bot.  This class should be extended to implement
    additional interfaces
    """
    __metaclass__ = abc.ABCMeta

    def __new__(cls, *args, **kwargs):
        """
        Fanciness!  Allow some initialization to happen without subclass
        implementors having to explicitly call the parent constructor
        """
        # Instantiate the instance and create the input and output queues
        instance = object.__new__( cls )
        instance._inq = Queue()
        instance._outq = Queue()

        # Create the output thread and start it
        instance.__output_thread = Thread(target=instance.output_handler)
        instance.__output_thread.daemon = True
        instance.__output_thread.start()

        return instance

    def get( self ):
        """
        Get a message from the input queue
        """
        return self._inq.get()

    def put( self, msg ):
        """
        Put a message on the output queue
        """
        self._outq.put( msg )

    def process( self, msg ):
        """
        Put a message on the input queue.  Essentially, process a message
        """
        self._inq.put( msg )

    def output_handler( self ):
        """
        This will be spun up in a separate thread.  Simply consumes messages
        from the output queue and writes them to the interface
        """
        while True:
            self.write_output( self._outq.get() )

    @abc.abstractmethod
    def write_output( self, msg ):
        """
        This method should have the bot simply write a message out to the
        appropriate interface
        """
        pass

    @abc.abstractmethod
    def run( self ):
        """
        This should start the interface.  Ie, it should join the room and begin
        listening
        """
        pass

from calamari.interfaces.xmpp import CalamariXMPP
from calamari.interfaces.irc_interface import CalamariIRC
