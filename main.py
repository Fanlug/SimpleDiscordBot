import random
import config
import discord  # Подключаем библиотеку
from discord.ext import commands

intents = discord.Intents.default()  # Подключаем "Разрешения"
intents.message_content = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='#', intents=intents)


class User:
    def __init__(self, id):
        self.id = id
        self.l = 0
        self.w = 0


users: User = []


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
            await ctx.reply(game_main(user))


@bot.command()
async def profile(ctx):
    await add_user(ctx)
    await ctx.reply(ctx.author)


@bot.command()
async def stats(ctx):
    await add_user(ctx)
    for user in users:
        if user.id == ctx.author.id:
            await ctx.reply(f'Wins: {user.w} Looses:{user.l}')


@bot.command()
async def server_stats(ctx):
    await ctx.reply(len(users))


bot.run(config.TOKEN)
