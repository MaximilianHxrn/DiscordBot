import discord
from discord import colour
from discord.ext import commands
from dotenv import load_dotenv
import random
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

options = {"!help", "!botinfo", "!print",
           "!Russisch Roulette", "!CoinFlip", "!clear_message"}

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ASMR"))
    print(f'{client.user} has connected to Discord!')


async def botinfo(message):
    await message.channel.send('Alive and happy :)')


async def print_text(message, temp):
    output = ""
    for x in temp[1:]:
        output += (x + " ")
    await message.channel.purge(limit=1)
    await message.channel.send(output)


async def roulette(message):
    result = random.randint(1, 6)
    if result == 1:
        await message.channel.send('U died...')
    else:
        await message.channel.send('U survived...')


async def clear(message, temp):
    if len(temp) == 1:
        await message.channel.purge(limit=2)
    else:
        await message.channel.purge(limit=(int(temp[1]) + 1))


async def coinflip(message):
    await message.channel.send("Type \"Heads\" or \"Tails\"")

    def check(m):
        return (m.content.lower() == "heads" and m.channel == message.channel) or (m.content.lower() == "tails" and m.channel == message.channel)
    msg = await client.wait_for("message", check=check)
    result = random.randint(1, 2)
    if result == 1:
        if msg.content.lower() == "tails":
            await message.channel.purge(limit=5)
            await message.channel.send("U won")
        else:
            await message.channel.send("U lost")


async def help(message):
    output = ""
    for x in options:
        output += x + "\n"
    await message.channel.send(output)

async def clear_message(message, id):
    msg = await message.channel.fetch_message(id)
    await msg.delete()

async def embed(message, content):
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar.add_field(name="Field1", value=content, inline=False)
    await message.channel.send(embed=embedVar)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    temp = message.content.split()
    option = message.content.lower()
    if option == '!botinfo':
        await botinfo(message)
    elif temp[0] == '!print':
        await print_text(message, temp)
    elif option == '!russisch roulette':
        await roulette(message)
    elif option == '!help':
        await help(message)
    elif temp[0] == '!clear':
        await clear(message, temp)
    elif temp[0] == '!clear_message':
        await clear_message(message, temp[1])
        await message.channel.purge(limit=1)
    elif option == '!coinflip':
        await coinflip(message)
    elif temp[0] == '!embed':
        await embed(message, temp[1])

client.run(TOKEN)
