import os

import aiohttp
import nextcord
from nextcord.ext import commands
import aiosqlite
import config

async def getprefix(client, message):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (message.guild.id,))
            data = await cursor.fetchone()
            if data:
                return data
            else:
                return "!"

def owner(ctx):
    if ctx.author.id == 741118153299591240:
        return True
    return False

def main():
    # allows privledged intents for monitoring members joining, roles editing, and role assignments
    intents = nextcord.Intents.all()
    intents.guilds = True
    intents.members = True

    activity = nextcord.Activity(
        type=nextcord.ActivityType.listening, name=f"{getprefix}help"
    )

    bot = commands.Bot(
        command_prefix=getprefix,
        intents=intents,
        activity=activity,
        owner_id=config.OWNER_ID,
    )

    # boolean that will be set to true when views are added
    bot.persistent_views_added = False
    
    @bot.check()
    def onwer(ctx):
        if ctx.author.id == 741118153299591240:
            return True
        return False

    @bot.event
    async def on_ready():
        print(f"{bot.user.name} has connected to Discord.")
        print("Database connected.")
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS prefixes (prefix TEXT , guild INTEGER)")
                await cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER , guild INTEGER)")
            await db.commit()

    
    @bot.event
    async def on_guild_join(guild):
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("INSERT INTO prefixes (prefix, guild) VALUES (?, ?)", ("!", guild.id,))
            await db.commit()
    @bot.event
    async def on_guild_remove(guild):
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("DELETE FROM prefixes WHERE guild = ?", (guild.id,))
            await db.commit()
    
    @bot.command()
    async def setprefix(ctx, prefix = None):
        if prefix is None:
            ctx.send("You need to specify a prefix")
        else:    
            async with aiosqlite.connect("main.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (ctx.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?", (prefix, ctx.guild.id,))
                        await ctx.send(f"updated prefix to '{prefix}'")
                    else:
                        await cursor.execute("INSERT INTO prefixes (prefix, guild) VALUES (?, ?)", ("!", ctx.guild.id,))
                        await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (ctx.guild.id,))
                        data = await cursor.fetchone()
                        if data:
                            await cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?", (prefix, ctx.guild.id,))
                            await ctx.send(f"updated prefix to '{prefix}'")
                        else:
                            return
                await db.commit()        
                        
    @bot.command()
    async def adduser(ctx, member: nextcord.Member= None):
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM users WHERE guild = ?", (ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("UPDATE users SET id = ? WHERE guild = ?", (member.id, ctx.guild.id,))
                else:
                    await cursor.execute("INSERT INTO users (id, guild) Values (?, ?)", (member.id, ctx.guild.id,))
            await db.commit()            
    
    @bot.command()
    async def removeuser(ctx, member: nextcord.Member = None):
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM users WHERE guild = ?", (ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("DELETE FROM users WHERE id = ? AND guild = ?", (member.id, ctx.guild.id,))
            await db.commit()   
      # load all cogs
    for folder in os.listdir("cogs"):
        bot.load_extension(f"cogs.{folder}")

    async def startup():
        bot.session = aiohttp.ClientSession()

    bot.loop.create_task(startup())

    # run the bot
    bot.run(config.BOT_TOKEN)


if __name__ == "__main__":
    main()
