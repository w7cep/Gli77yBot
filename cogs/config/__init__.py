from nextcord.ext import commands

class Config(commands.Cog, name="Config"):
    """Bot configuration"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['game'])
    @commands.has_role('Bot Manager')
    async def changegame(self, ctx, gameType: str, *, gameName: str):
        '''Changes the game currently playing (BOT OWNER ONLY)'''
        gameType = gameType.lower()
        if gameType == 'playing':
            activityType = nextcord.ActivityType.playing
        elif gameType == 'watching':
            activityType = nextcord.ActivityType.watching
        elif gameType == 'listening':
            activityType = nextcord.ActivityType.listening
        elif gameType == 'streaming':
            activityType = nextcord.ActivityType.streaming
        guildsCount = len(self.bot.guilds)
        memberCount = len(list(self.bot.get_all_members()))
        gameName = gameName.format(guilds = guildsCount, members = memberCount)
        await self.bot.change_presence(activity=nextcord.Activity(type=activityType, name=gameName))
        await ctx.send(f'**:ok:** Change the game to: {gameType} ** {gameName} **')

    @commands.command()
    @commands.has_role('Bot Manager')
    async def changestatus(self, ctx, status: str):
        '''Changes the online status of the bot (BOT OWNER ONLY)'''
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            nextcordStatus = nextcord.Status.invisible
        elif status == 'idle':
            nextcordStatus = nextcord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            nextcordStatus = nextcord.Status.dnd
        else:
            nextcordStatus = nextcord.Status.online
        await self.bot.change_presence(status=nextcordStatus)
        await ctx.send(f'**:ok:** Change status to: **{nextcordStatus}**')

    @commands.command(aliases=['guilds'])
    @commands.has_role('Bot Manager')
    async def servers(self, ctx):
        '''Lists the current connected guilds (BOT OWNER ONLY)'''
        msg = '```py\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)

    @commands.command()
    @commands.is_owner()
    async def leaveserver(self, ctx, guildid: str):
        '''Exits a server (BOT OWNER ONLY)
        Example:
        -----------
        :leaveserver 102817255661772800
        '''
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guild = self.bot.get_guild(guildid)
            if guild:
                await guild.leave()
                msg = f':ok: Successful exit from {guild.name}!'
            else:
                msg = ":x: Couldn't find a suitable guild for this ID!"
        await ctx.send(msg)

    @commands.command()
    @commands.has_role('Bot Manager')
    async def discriminator(self, ctx, disc: str):
        '''Returns users with the respective discriminator'''

        discriminator = disc
        memberList = ''

        for guild in self.bot.guilds:
            for member in guild.members:
                if member.discriminator == discriminator and member.discriminator not in memberList:
                    memberList += f'{member}\n'

        if memberList:
            await ctx.send(memberList)
        else:
            await ctx.send(":x: Couldn't find anyone")

    @commands.command()
    @commands.has_role('Bot Manager')
    async def nickname(self, ctx, *name):
        '''Changes the server nickname of the bot (BOT OWNER ONLY)'''
        nickname = ' '.join(name)
        await ctx.me.edit(nick=nickname)
        if nickname:
            msg = f'Changed my server nickname to: **{nickname}**'
        else:
            msg = f'Reset my server nickname on: **{ctx.me.name}**'
        await ctx.send(msg)

def setup(bot: commands.Bot):
    bot.add_cog(Config(bot))