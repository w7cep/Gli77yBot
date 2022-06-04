import os

import aiohttp
import nextcord
from nextcord.ext import commands
import aiosqlite
import config


def main():
    # allows privledged intents for monitoring members joining, roles editing, and role assignments
    intents = nextcord.Intents.all()
    intents.guilds = True
    intents.members = True

    activity = nextcord.Activity(
        type=nextcord.ActivityType.listening, name=f"{config.PREFIX}help"
    )

    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or(config.PREFIX),
        intents=intents,
        activity=activity,
        owner_id=config.OWNER_ID,
    )

    # boolean that will be set to true when views are added
    bot.persistent_views_added = False

    @bot.event
    async def on_ready():
        print(f"{bot.user.name} has connected to Discord.")
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTERGER , guild INTERGER) ")
            await db.commit()
    
    @bot.command()
    async def adduser(ctx, member: nextcord.Member):
        member = ctx.author
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM users WHERE guild = ?", (ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("UPDATE users SET id = ? WHERE guild = ?", (member.id, ctx.guild.id,))
                else:
                    await cursor.execute("INSERT INTO users (id, guild) Values (?, ?)", (member.id, ctx.guild.id,))
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
