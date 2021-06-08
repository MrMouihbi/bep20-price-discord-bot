from discord.ext import commands
from asyncio import sleep
from decouple import config
from price_calculation import getPrice

client = commands.Bot("_!_")

@client.event
async def on_ready():
    print('Bot is online.')


async def setPrice():
    await client.wait_until_ready()
    while not client.is_closed():
        guild = client.get_guild(int(config('your_server_id')))
        me = guild.me
        await me.edit(nick='$'+getPrice())
        await sleep(60)  # update every 60 seconds

client.loop.create_task(setPrice())

client.run(config('discord_token'))
