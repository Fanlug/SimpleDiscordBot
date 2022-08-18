import random
import time

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


async def add_user(ctx):
    r = 0
    for user in users:
        if user.id == ctx.author.id: r = r + 1
    if r == 0:
        users.append(User(ctx.author.id))


def game_main(user):
    if random.randint(0, 2) >= 1:
        user.l = user.l + 1
        return "Проиграл"
    else:
        user.w = user.w + 1
        return "Выиграл"


@bot.command()
async def ping(ctx):
    await add_user(ctx)
    await ctx.send('pong')


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
    r = 1
    message = args.__str__()[2:-3]
    form_message = ''
    for i in range(0, len(message)):
        if ('0' > message[i] or message[i] > '9') and (r == 1 or r == 4):
            r = 1
            form_message = form_message + message[i]
        elif '0' <= message[i] <= '9' and (r == 1 or r == 4):
            r = 2
            form_message = form_message + '*' + message[i]
        elif (r == 3 or r == 2) and '0' <= message[i] <= '9':
            r = 3
            form_message = form_message + message[i]
        elif (r == 3 or r == 2) and ('0' > message[i] or message[i] > '9'):
            r = 4
            form_message = form_message + '*' + message[i]
    if r == 2 or r == 3:
        form_message = form_message + '*'
    print(form_message)
    state2 = 1
    begin = []
    end = []
    l = 0
    pos = 0
    for i in range(0, len(form_message)):
        if form_message[i] == '*' and state2 == 1:
            if '9' >= form_message[i + 1] >= '1':
                state2 = 2
                l = l + 1
                pos = i
        elif form_message[i] == '*' and state2 == 2:
            if l > 2:
                print(str(pos) + ' ' + str(i))
                begin.append(pos)
                end.append(i)
            l = 0
            pos = 0
            state2 = 1
        elif state2 == 2 and l > 0:
            l = l + 1
    for i in range(len(begin) - 1, -1, -1):
        form_message = form_message[:end[i]] + '**' + form_message[end[i]:]
        form_message = form_message[:begin[i]] + '**' + form_message[begin[i]:]
    await ctx.send('>>> ' + message + '\n' + form_message)


@bot.command()
async def times(ctx):
    await ctx.send(
        '>>> <t:' + str(int(time.time())) + ':f>' + '\n' + str(int(3600 - time.time()) % 3600) + '\n' + '<t:' + str(
            int(time.time()) + int(3600 - time.time()) % 3600) + ':f>')


bot.run(config.TOKEN)
