Calamari.py - An easy, extensible chat bot

Alright, let me keep this short and sweet.  Just a fore-warning, I drew a lot of
inspiration from flask, even going so far as lifting the configuration class
completely.  This was on purpose, because I am lazy as hell and a pretty big fan
of flask.

The bot has two major components: the interfaces (responsible solely for input
and output) and the engine (responsible solely for parsing and executing
commands, and sending the output of a command (if any) back to the appropriate
interface.

So to begin, you must initialize the engine, like so:

    bot = CalamariEngine( __name__ )

By default, the engine treats everything prefixed with a period as a potential
command.  This can be configured to any character or string by using the
"prefix" argument when intializing the engine.  For example, if we wanted
commands to be prefixed with a hashmark instead, we'd initialize the engine like
so:

    bot = CalamariEngine( __name__, prefix = "#" )

Now that we have the engine initialized, we need to initialize one or more
interfaces.  The only interface available right now is XMPP, so we'll use that
as an example:

    xmpp_interface = CalamariXMPP( "user@chatserver.com/resource", "mypassword",
        "muc_room_name, "bot_nick" )

And then we register the interface with the bot:

    bot.register_interface( xmpp_interface )

So now we're almost ready to start the bot, but we have one more crucial step:
adding commands.  Commands are added to the bot using a convenient decorator
method that should look really familiar to anyone with experience using flask:

    @bot.command( "dude" )
    def dude( msg, user ):
        """
        sweeeet
        """
        return "sweet"

This adds a ".dude" command to the bot, which simply causes it to respond with
the word "sweet".  It is important to note that as long as the message is
prefixed with the appropriate prefix and the first word maps to a command that
you've registered, that command will execute.  For example ".dude blahblah blah"
will still hit the .dude command.  The "msg" argument will contain the entire
message.  This enables you to do argument parsing.  (TODO: Implement some kind
of easy argument parsing).  The user argument will contain the username of the
user who initiated the command.

Finally once you've registered all the commands you want, simply start the bot:

    bot.run()

This will cause all of the currently configured interfaces to "log in", and
begin I/O for the engine.
