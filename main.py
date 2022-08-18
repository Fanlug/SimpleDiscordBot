import random
import time as times

import discord
from discord.ext import commands

import config

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(config.PREFIX, intents=intents)


class User:
    def __init__(self, id):
        self.id = id
        self.l = 0
        self.w = 0


users: [User] = []


def add_user(ctx):
    r = 0
    for user in users:
        if user.id == ctx.author.id: r += 1
    if r == 0:
        users.append(User(ctx.author.id))


def game_main(user):
    if random.randint(0, 2) >= 1:
        user.l += 1
        return "Проиграл"
    else:
        user.w += 1
        return "Выиграл"


@bot.command()
async def game(ctx):
    await add_user(ctx)
    for user in users:
        if user.id == ctx.author.id:
            await ctx.send(game_main(user))


@bot.command()
async def profile(ctx):
    await add_user(ctx)
    await ctx.send(ctx.author)


@bot.command()
async def stats(ctx):
    await add_user(ctx)
    for user in users:
        if user.id == ctx.author.id:
            await ctx.send(f'Wins: {user.w} Looses:{user.l}')


@bot.command()
async def server_stats(ctx):
    await ctx.reply(len(users))


@bot.command()
async def numbers(ctx, *args):
    await ctx.send(f'LOL')


@bot.command()
async def time(ctx):
    await ctx.send(
        '>>> <t:' +
        str(int(times.time())) + ':f>' +
        '\n' +
        str(int(3600 - times.time()) % 3600) +
        '\n' +
        '<t:' + str(int(times.time()) + int(3600 - times.time()) % 3600) + ':f>')


bot.run(config.TOKEN)
