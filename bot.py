from random import *
import random
import time
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.utils import get

import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!', intents= discord.Intents.all())
bot.remove_command('help')

#On Ready
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="the developers"))
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    try:
        sycned = await bot.tree.sync()
        print(f'Sycned {len(sycned)} global commands.')
    except Exception as e:
        print(e)

#Latency
@bot.tree.command(name='latency', description="Shows bot's latency.")
@app_commands.checks.has_permissions(administrator=True)
async def latency(interaction: discord.Interaction):
    await interaction.response.send_message(f"Latency is {round(bot.latency * 1000)}ms", ephemeral=True)

#Description
@bot.tree.command(name='illusa', description="What is Illusa?")
async def malderecesi(interaction: discord.Interaction):
    await interaction.response.send_message(content=f'To be Announced.')

#Avatar
@bot.tree.command(name='avatar', description="You can get people's profile pictures.")
async def avatar(interaction: discord.Interaction, member: Optional[discord.Member]):
    if member == None:
        ProfilePicture = interaction.user.display_avatar.url
        await interaction.response.send_message(ProfilePicture)
    else:
        ProfilePicture = member.avatar.url
        await interaction.response.send_message(ProfilePicture)



#Admin Commands
#Clear
@bot.tree.command(name='clear', description="Clears the given amount of messages.")
@app_commands.checks.has_permissions(administrator=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.send_message(f"Successfully deleted {amount} of messages.", ephemeral=True)
    await interaction.channel.purge(limit=amount)

#Ban
@bot.tree.command(name='ban', description="Bans members.")
@app_commands.checks.has_permissions(administrator=True)
async def ban(interaction: discord.Interaction, member: discord.Member, delete_messages: int ,reason: str = "No reason provided."):
    try:
        await member.ban(reason = reason, delete_message_days = delete_messages)
        await interaction.response.send_message(f"Successfully banned {member.mention} for {reason}")
    except:
        await interaction.response.send_message(f"The {member.mention} could not be banned from the server.", ephemeral=True)
@ban.error
async def ban_error(interaction: discord.Interaction, error):
    if isinstance(error, MissingPermissions):
        await interaction.response.send_message(f"You don't have permission to use this command!", ephemeral=True)

#Kick
@bot.tree.command(name='kick', description="Kicks members.")
@app_commands.checks.has_permissions(administrator=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await member.kick(reason = reason)
        await interaction.response.send_message(f"Successfully kicked {member.mention} for: {reason}")
    except:
        await interaction.response.send_message(f"The {member.mention} could not be kicked from the server.", ephemeral=True)
@kick.error
async def ban_error(interaction: discord.Interaction, error):
    if isinstance(error, MissingPermissions):
        await interaction.response.send_message(f"You don't have permission to use this command!", ephemeral=True)



#Logging
@bot.event
async def on_message(message):
    # Only log messages that are sent in a guild
    if message.guild is not None:
        # Log the message when it is sent
        print(f"{message.author}: {message.content}")

@bot.event
async def on_message_edit(before, after):
    # Only log messages that are edited in a guild
    if after.guild is not None:
        # Log the edited message
        print(f"{after.author} edited their message: {after.content}")

@bot.event
async def on_message_delete(message):
    # Only log messages that are deleted in a guild
    if message.guild is not None:
        # Log the deleted message
        print(f"{message.author} deleted their message: {message.content}")

bot.run(TOKEN)