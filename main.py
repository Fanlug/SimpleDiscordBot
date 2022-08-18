import random
import re
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
        self.loses = 0
        self.wins = 0


users: [User] = []


def game_main(user):
    if random.randint(0, 2) >= 1:
        user.loses += 1
        return "Проиграл"
    else:
        user.wins += 1
        return "Выиграл"


def replace(f):
    if int(f.group()) > 100:
        return f'***{int(f.group())}***'
    else:
        return f'*{int(f.group())}*'


@bot.command()
async def game(ctx):
    for user in users:
        if user.id == ctx.author.id:
            await ctx.send(game_main(user))


@bot.command()
async def profile(ctx):
    user_registered = False
    for user in users:
        if user.id == ctx.author.id: user_registered = True
    if not user_registered:
        users.append(User(ctx.author.id))
    await ctx.send(ctx.author)


@bot.command()
async def stats(ctx):
    for user in users:
        if user.id == ctx.author.id:
            await ctx.send(f'Wins: {user.wins} Looses:{user.loses}')


@bot.command()
async def server_stats(ctx):
    await ctx.reply(len(users))


@bot.command()
async def numbers(ctx):
    message = f'{ctx.message.content} + \n'
    sample = r'([\d]+)'
    message += re.sub(sample, replace, message)
    await ctx.send(f'>>> {message}')


@bot.command()
async def time(ctx):
    time_cur = int(times.time())
    time_left_before_next_hour = 3600 - time_cur % 3600
    await ctx.send(
        f'>>> <t:{time_cur}:f>' +
        f'\n {time_left_before_next_hour} \n' +
        f'<t:{time_cur+time_left_before_next_hour}:f>')


bot.run(config.TOKEN)
