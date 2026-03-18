import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import receive_email
load_dotenv()
import random
import send_email
from discord.ext import tasks
import asyncio


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "!", intents = intents)

bot.emailFlag = False
bot.user_email = None
guild = discord.Object(id = 1463260302325055530)

@tasks.loop(seconds=10)
async def check_email():
        if bot.user_email == None:
            return
        message = await receive_email.check_email(bot.user_email)
        if message is not None:
            mail_from = message['from']
            mail_subject = message['subject']
            mail_content = ''
            for part in message.get_payload():
                if part.get_content_type() == 'text/plain':
                    mail_content += part.get_payload()
                    channel_id = receive_email.getChannelId(mail_content)
            mail_content = await receive_email.extract_original(mail_content)
            channel = bot.get_channel(channel_id)
            await channel.send(f'{bot.user_email}:\n{mail_content}')


@bot.event
async def on_ready():
   print(f'Logged in as {bot.user}!')
   await bot.tree.sync(guild=guild)
   check_email.start()


##all messages
@bot.event
async def on_message(message):
   await bot.process_commands(message)
   author = message.author
   channel = message.channel.id
   if author == bot.user:
       return
   print(f'{author.display_name} ({author.name}): {message.content}')
   if bot.emailFlag:
       await send_email.send(message.content, author.name, bot.user_email, channel)

@bot.tree.command(name="email", description="Turn email messages on. Usage: /email example@gmail.com", guild=guild)
async def email(interaction : discord.Interaction, message : str):
    if not message.endswith("@gmail.com"):
        await interaction.response.send_message(content = "Not a valid gmail address.")
        return
    await interaction.response.send_message(content = f"Messages will be emailed to {message}!")
    bot.emailFlag = True
    bot.user_email = message

@bot.tree.command(name="emailoff", description="Turn email messages off", guild=guild)
async def emailoff(interaction : discord.Interaction):
    bot.emailFlag = False
    await interaction.response.send_message(content = "Email messages turned off.")

bot.run(os.getenv('TOKEN'))

