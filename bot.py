import discord
import re
from discord.ext import commands
from decouple import config

intents = discord.Intents.all()
client = discord.Bot(command_prefix='$', intents=intents)
mapping = {}

@client.event
async def on_message(message):
    print("Message received: " + message.content)
    for react, regex in mapping.items():
        if re.search(regex, message.content):
            await message.add_reaction(react)

@client.event
async def on_message_edit(_, message):
    for react, regex in mapping.items():
        if re.search(regex, message.content):
            await message.add_reaction(react)

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 255086554622459914
    return commands.check(predicate)

@client.command(name="set_regex")
@is_owner()
async def set_regex(ctx, react, regex):
    """Define a new regex pattern

    Args:
        regex (str): The new regex pattern
    """
    await ctx.respond("New regex pattern defined: ```\n" + regex + "\n```")
    global mapping
    mapping[react] = regex
    save_regex(mapping)

@client.command(name="del_react")
@is_owner()
async def del_regex(ctx, react):
    """Delete a regex pattern

    Args:
        react (str): The reaction to delete
    """
    await ctx.respond("Deleted regex pattern for reaction: " + react)
    global mapping
    mapping.pop(react, None)
    save_regex(mapping)

@client.command(name="get_regex")
async def get_regex(ctx):
    """Get the current regex pattern"""
    global mapping
    await ctx.respond("Current patterns: ```\n" +
                        "\n".join([react + " = " + regex for react, regex in mapping.items()])
                      + "\n```")

@client.command(name="get_id")
async def get_id(ctx):
    """Get your ID"""
    await ctx.respond("Your ID is: " + str(ctx.author.id))

def save_regex(mapping):
    with open("regex.txt", "wb") as f:
        for react, regex in mapping.items():
            f.write(react.encode("utf-8") + b"=" + regex.encode("utf-8") + b"\n")
            print("Saved regex: " + regex + " for reaction: " + react)

def load_regex(mapping: list):
    mapping.clear()
    with open("regex.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line == "" or line == "\n":
                continue
            (react, regex) = line.strip().split("=", 1)
            print("Loaded regex: " + regex + " for reaction: " + react)
            mapping[react] = regex

def main():
    global client
    global mapping
    load_regex(mapping)

    client.run(config("TOKEN"))

if __name__ == "__main__":
    main()