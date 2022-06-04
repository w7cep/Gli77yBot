import nextcord
from nextcord.ext import commands
import json

class Prefix(commands.Cog, name="Prefix"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

def setup(bot: commands.Bot):
    bot.add_cog(Prefix(bot))
