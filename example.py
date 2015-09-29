"""
This bot is simple: it sits in the room and responds to two commands:
    .dude and .sweet

Example output:
    d00kiesh0es: .sweet
    bot: dude
    d00kiesh0es: .dude
    bot: sweet
"""
from calamari.engine import CalamariEngine
from calamari.interfaces import CalamariXMPP, CalamariIRC

# Instantiate and configure the bot engine
bot = CalamariEngine(__name__)

# Instantiate all the interfaces
xmpp_interface = CalamariXMPP( "user@chat.server.com/jid"
        "password", "room_name",  'bot_nick' )
# Last 3 arguments are optional
irc_interface = CalamariIRC( 'irc_server.example.com',
        6697, 'IRC_CHANNEL', 'bot_nick', use_ssl=True, # Use SSL
        username='IRC_USERNAME', password='IRC_PASSWORD' )

# Register all the interfaces
bot.register_interface( xmpp_interface )
bot.register_interface( irc_interface )

@bot.command( "dude" )
def dude( msg, user ):
    """
    sweeeet
    """
    return "sweet"

@bot.command( "sweet" )
def sweet( msg, user ):
    """
    duuuuuude
    """
    return "dude"

bot.run()
