import random

import discord
from discord.ext import commands

bot_token: str = ''

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print("Among Ghost is ready to start a game !")
    await bot.change_presence(activity=discord.Game(name='Among Ghost !'))


@bot.command(name='play')
async def play(ctx: commands.Context, user1: discord.User, user2: discord.User, user3: discord.User,
               user4: discord.User):
    print(f"Play command received.")
    users = [user1, user2, user3, user4]
    if not await checkUsers(ctx, users):
        return
    selected = getGhostUser(users)
    sendMessages(users, selected)


@play.error
async def play_error(ctx: commands.Context, error):
    print(f"Play command received with error \"{error}.\"")
    await ctx.send(error)


def getGhostUser(users: list[discord.User]) -> discord.User:
    return random.choice(users)


def sendMessages(users: list[discord.User], selected: discord.User):
    for user in users:
        sendMessage(user, selected)


async def sendMessage(user: discord.User, selected: discord.User):
    if user.id == selected.id:
        await bot.get_user(user.id).send('Tu es le charmeur de fantôme ! Tue ton équipe !')
    else:
        await bot.get_user(user.id).send('Tu es un enquêteur ! Trouve le fantôme et accomplis les quêtes !')


async def checkUsers(ctx: commands.Context, users: list[discord.User]) -> bool:
    for user in users:
        if not checkUserExistsAndIsInGuild(ctx, user):
            return await sendInvalidUserMessage(ctx, user)


def checkUserExistsAndIsInGuild(ctx: commands.Context, user: discord.User) -> bool:
    return ctx.guild.get_member(user.id) is not None


async def sendInvalidUserMessage(ctx, user):
    await ctx.send(f"L'utilisateur {user} n'est pas valide ou pas présent sur le serveur."
                   f"Assurez-vous que les utilisateurs sont valides en les mentionnant,"
                   f"et qu'ils soient présents sur le serveur.")
    return False


if __name__ == '__main__':
    bot.run(bot_token)
