"""
engine/engine.py

Defines the main logic of the bot, while IO is handled by the interfaces.
"""
from threading import Thread
from config import Config, get_root_path

class CalamariEngine():
    """
    The brains of the operation.  Register interfaces with the engine and it
    will do all of the heavy lifting
    """
    def __init__( self, import_name, prefix = "." ):
        """
        Initialize the list of commands / interfaces, the config dictionary, and
        set the command prefix
        """
        self.import_name = import_name
        self.root_path = get_root_path( import_name )
        self.config = Config( self.root_path )
        self.prefix = prefix
        self.commands = {}
        self.null_cmd = None
        self.interfaces = []

    def register_interface( self, interface, threads = 5 ):
        """
        Registers an interface to the engine and spins up the specified number
        of threads to handle that interface.  
        """
        self.interfaces.append( interface )
        for i in range( threads ):
            t = Thread( target = self.interface_handler, args = (interface,) )
            t.start()

    def interface_handler( self, interface ):
        """
        This is the method run by the interface handler threads.  Gets a
        message from an interface, processes it, and puts the output back into
        the interface, if there was any
        """
        while True:
            output = self.process( interface.get() )
            if output:
                interface.put( {'message':output} )

    def process( self, msg ):
        """
        Determine which command is supposed to be run and do it
        """
        if not msg['message'].startswith( self.prefix ):
            if self.null_cmd:
                return self.null_cmd( msg['message'], msg['user'] )
            return

        command = msg['message'].split()[0][1:]
        if not command:
            return "Usage: .(command) [args]"

        if command in self.commands:
            return self.commands[command]['func']( msg['message'], msg['user'] )

    def null_command( self ):
        """
        A decorator to specify a "default" command for the bot, that gets run
        when the configured prefix is not present
        """
        def wrap( func ):
            self.null_cmd = func
            return func
        return wrap

    def command( self, command_alias, hidden = False ):
        """
        A decorator which maps a prefix command to a method.
        """
        def wrap( func ):
            self.commands[ command_alias ] = {'func':func,'help':func.__doc__,
                    'hidden':hidden}
            return func
        return wrap

    def run( self ):
        """
        Start listening on all the interfaces
        """
        for i in self.interfaces:
            i.run()
