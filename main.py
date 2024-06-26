import discord
from discord.ext import commands, tasks
from discord.ext.commands import MemberConverter
from discord import Embed
import random
import pickle
import os
from dotenv import load_dotenv
import asyncio
import traceback
import sys
import sqlite3
import subprocess
import loguru
import time
import warnings
from typing import Union
import datetime


os.system('cls')

load_dotenv()
RECORDS_FILENAME = os.getenv('ENVRECORDS_FILENAME')
TOKEN = os.getenv('ENVDISCORD_TOKEN')
ENABLED_USER_ID = 712946563508469832  # My user id
BOT_LOG_CHANNEL_ID = 1234100559431077939
VERIFIED_ROLE_NAME = "Verified"


class myLogger:
    def info(message):
        loguru.logger.info(message)

    def warning(message):
        loguru.logger.warning(message)

    def error(message):
        loguru.logger.error(message)

    def success(message):
        loguru.logger.success(message)


# Load existing message records
try:
    with open(RECORDS_FILENAME, 'rb') as file:
        message_records = pickle.load(file)
except FileNotFoundError:
    message_records = []
    myLogger.warning("Message records file not found. Creating a new one.")
    yes = open('message_records.pkl', 'w')
    yes.close()
except EOFError:
    message_records = []
    myLogger.error("The message records file is empty or corrupted.")


# replys message history
async def reply_message_history(message, message_records):
    # Extract message content, username, and server name for each record
    message_history = '\n'.join([
        f"{record.get('message_content', 'Unknown')} - {record.get('username', 'Unknown')} ({record.get('server_name', 'Unknown')})"
        for record in message_records])

    # Split message into chunks of 1900 characters or less
    chunks = [message_history[i:i + 1900] for i in range(0, len(message_history), 1900)]

    # reply each chunk as a separate message
    for chunk in chunks:
        await message.channel.reply(f"```{chunk}```")

    # Reply to the user to inform them that all message history chunks have been sent
    await message.reply("All message history has been uploaded :thumbsup:")


# Function to send the timed message
async def send_timed_message():
    await bot.wait_until_ready()
    channel = bot.get_channel(1225352074955591713)  # Replace with your channel ID
    msg = ""  # Your message here

    while not bot.is_closed():
        if msg:
            await channel.send(msg)
        await asyncio.sleep(10000)  # Wait for x seconds before sending the next message




class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.prefix = None

    def get_command_signature(self, command):
        if self.prefix:
            return f"{self.prefix}{command.qualified_name} {command.signature}"
        else:
            return f"{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping):
        commands_per_page = 25
        command_list = [self.get_command_signature(command) for cog, commands in mapping.items() for command in commands]
        chunks = [command_list[i:i + commands_per_page] for i in range(0, len(command_list), commands_per_page)]

        embed_pages = []
        for current_page, chunk in enumerate(chunks, start=1):
            embed = discord.Embed(title=f"Bot Commands (Page {current_page})", color=discord.Color.blue())
            embed.description = "\n".join(chunk)
            embed_pages.append(embed)

        message = await self.context.send(embed=embed_pages[0])

        if len(embed_pages) > 1:
            view = Pages(embed_pages)
            await message.edit(view=view)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Command Help: {command.name}", description=command.help, color=discord.Color.blue())
        embed.add_field(name="Usage", value=self.get_command_signature(command), inline=False)
        await self.get_destination().send(embed=embed)

class Pages(discord.ui.View):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.current_page = 0

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.grey)
    async def previous_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = max(0, self.current_page - 1)
        await interaction.message.edit(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.grey)
    async def next_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = min(len(self.pages) - 1, self.current_page + 1)
        await interaction.message.edit(embed=self.pages[self.current_page], view=self)

    async def start(self, ctx: commands.Context):
        self.current_page = 0
        self.message = await ctx.send(embed=self.pages[self.current_page], view=self)




con = sqlite3.connect('level.db')
cur = con.cursor()
intents = discord.Intents.all()
bot_prefix = '.'
help_command = CustomHelpCommand()
help_command.prefix = bot_prefix
bot = commands.Bot(command_prefix=bot_prefix, intents=intents, help_command=help_command)


@bot.command(
    help="Creates a poll with a question and multiple options. Separate the question and options using '|' symbol. Example: !poll What is your favorite color? | Red | Blue | Green")
async def poll(ctx, *, question_and_options):
    if ctx.author.guild_permissions.administrator:
        await ctx.message.delete()
        # Split the question and options
        parts = question_and_options.split('|')
        question = parts[0].strip()
        options = [option.strip() for option in parts[1:]]

        if len(options) > 10:
            await ctx.send(f"{ctx.author.mention} You can only have up to 10 options in a poll.")
            return

        # Create embed for the poll
        embed = discord.Embed(title=f"Poll: {question}", color=discord.Color.blue())

        # Add options to the embed
        for i, option in enumerate(options):
            embed.add_field(name=f"Option {i + 1}", value=option, inline=False)

        # Send the poll and add reactions
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            if i == 9:
                await message.add_reaction("🔟")  # Unicode regional indicator number 10
            else:
                await message.add_reaction(chr(0x0031 + i) + "\uFE0F\u20E3")  # Unicode regional indicator numbers 1-9
    else:
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention} You do not have permission to use this command.")


@bot.event
async def on_raw_reaction_add(payload):
    # Check if the reaction is added to a poll message
    message_id = payload.message_id
    channel_id = payload.channel_id
    if payload.event_type != 'REACTION_ADD' or not payload.member or payload.member.bot:
        return
    channel = bot.get_channel(channel_id)
    try:
        message = await channel.fetch_message(message_id)
    except discord.NotFound:
        return
    if not message.embeds:
        return
    embed = message.embeds[0]
    if not embed.title or not embed.title.startswith("Poll:"):
        return

    # Update the poll results
    emoji = payload.emoji
    if isinstance(emoji, discord.PartialEmoji):
        emoji = emoji.name
    for field in embed.fields:
        if field.name.startswith("Option") and field.value == emoji:
            await message.channel.send(f"{payload.member.display_name} voted for {emoji}.")


@bot.event
async def on_ready():
    myLogger.info(f'Logged in as {bot.user.name}')
    myLogger.info(f'Bot ID: {bot.user.id}')
    myLogger.info(' ')

    
    await bot.change_presence(status=discord.Status.dnd,
                              activity=discord.Activity(type=discord.ActivityType.listening, name="Erika"))

    bot.loop.create_task(send_timed_message())
    verifyChannel = bot.get_channel(1234091236097396787)
    if verifyChannel:
        async for message in verifyChannel.history():
            # Delete the previous message if it was sent by the bot
            await message.delete()

        embed = discord.Embed(title="Verification", description="Click below to verify.")
        await verifyChannel.send(embed=embed, view=Verification())
    else:
        myLogger.error("Could not send verification message for whatever reason.")

    with open('IMG_0935.JPEG', 'rb') as f:
        avatar_bytes = f.read()
        f.close()
    #await bot.user.edit(avatar=avatar_bytes)
    #await bot.user.edit(username="bot-Bernso")


@bot.command(help="Starts up the leveling system if it hasnt already.")
async def init(ctx):
    if ctx.author.guild_permissions.administrator:
        cur.execute(
            f'''CREATE TABLE IF NOT EXISTS GUILD_{ctx.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')

        for x in ctx.guild.members:
            if not x.bot:
                cur.execute(f"INSERT INTO GUILD_{ctx.guild.id} (user_id) VALUES ({x.id})")

        con.commit()

        await ctx.channel.send("Leveling system initialized")
    else:
        await ctx.reply("You do not haver permission to use this command.")


async def level_up_notification(user, level, channel):
    message = f"Congratulations {user.mention}! You've reached level {level}!"
    await channel.send(message)


@bot.command(help="Edit a user's experience.\n For the <amount> of xp you can use 'reset' to reset the user's XP.")
async def editxp(ctx, user: discord.Member, amount):
    if ctx.author.guild_permissions.administrator:
        try:
            cur.execute(f"SELECT * FROM GUILD_{ctx.guild.id} WHERE user_id={user.id}")
            result = cur.fetchone()

            if result:
                if amount == "reset":
                    new_exp = 0
                else:
                    new_exp = max(0, result[1] + int(amount))  # Ensure the new XP is non-negative

                # Calculate the old and new levels
                old_level = (result[1] // 50) + 1
                new_level = (new_exp // 50) + 1
                remaining_exp_old = result[1] % 50  # Calculate remaining XP for the current level (old)
                remaining_exp_new = new_exp % 50  # Calculate remaining XP for the current level (new)

                # Cap the XP required for leveling up at 50
                next_level_exp_old = min((old_level * 50), 50)  # Cap the next level XP at 50
                next_level_exp_new = min((new_level * 50), 50)  # Cap the next level XP at 50

                cur.execute(f"UPDATE GUILD_{ctx.guild.id} SET exp={new_exp} WHERE user_id={user.id}")
                con.commit()

                # Check if user leveled up
                if new_level > old_level:
                    # Send level up notification in a specific channel
                    level_up_channel_id = 1217998981246881832  # Replace with your desired channel ID
                    level_up_channel = bot.get_channel(level_up_channel_id)
                    if level_up_channel:
                        await level_up_notification(user, new_level, level_up_channel)

                    # Check if the new level is divisible by 5
                    if new_level % 5 == 0:
                        # Add role to the user for each 5 levels beneath the current level
                        for i in range(new_level - 5, 0, -5):
                            role_name = f"level-{i}"
                            role = discord.utils.get(ctx.guild.roles, name=role_name)
                            if not role:
                                role = await ctx.guild.create_role(name=role_name)
                            await user.add_roles(role)

                # Create an embedded message to show changes
                embed = discord.Embed(title="XP and Level Change", color=discord.Color.gold())
                embed.set_thumbnail(url=user.avatar)
                embed.add_field(name="User", value=user.mention, inline=False)
                embed.add_field(name="Old XP", value=f"{remaining_exp_old}/{next_level_exp_old} (Level {old_level})",
                                inline=False)
                embed.add_field(name="New XP", value=f"{remaining_exp_new}/{next_level_exp_new} (Level {new_level})",
                                inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send("User not found in the database.")
        except sqlite3.OperationalError as e:
            await ctx.send("Database error occurred.")
            myLogger.error("SQLite Error:", e)
    else:
        await ctx.reply("You do not have permission to use this command.")


@bot.command(help="Shows the specified user's experience and levels.")
async def xp(ctx, user: discord.User = None):
    try:
        if user is None:
            user = ctx.author

        cur.execute(f"SELECT * FROM GUILD_{ctx.guild.id} WHERE user_id={user.id}")
        result = cur.fetchone()

        if result is not None:
            exp = result[1]
            level = (exp // 50) + 1  # Calculate the level
            remaining_exp = exp % 50  # Calculate remaining XP for the current level

            # Cap the XP required for leveling up at 50
            next_level_exp = min((level * 50), 50)  # Cap the next level XP at 50

            # Create an embedded message with user mention in the title
            embed = Embed(title=f"{user.display_name}", color=discord.Color.green())
            embed.set_thumbnail(url=user.avatar)
            embed.add_field(name="XP", value=f"{remaining_exp}/{next_level_exp} XP", inline=True)
            embed.add_field(name="Level", value=level, inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Hmm no such user in the database")
    except sqlite3.OperationalError:
        await ctx.send("Database not initialized")


@bot.command(help="Shows the top 5 highest level people in the server.")
async def leaderboard(ctx):
    try:
        cur.execute(f"SELECT user_id, MAX(exp) FROM GUILD_{ctx.guild.id} GROUP BY user_id ORDER BY MAX(exp) DESC LIMIT 5")
        results = cur.fetchall()

        if results:
            embed = discord.Embed(title="Leaderboard", color=discord.Color.blue())

            for index, (user_id, exp) in enumerate(results, start=1):
                user = ctx.guild.get_member(user_id)
                if user:
                    level = (exp // 50) + 1
                    remaining_exp = exp % 50  # Calculate remaining XP for the current level
                    embed.add_field(name=f"{index}. {user.display_name}", value=f"XP: {remaining_exp} | Level: {level}",
                                    inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("No users found in the database.")
    except sqlite3.OperationalError:
        await ctx.send("Database not initialized")
    except Exception as e:
        myLogger.error(f"An error has occurred: {e}")



@bot.command(name="role_colour")
async def changecolor(ctx, role_name: str, color: discord.Color):
    """
    Change the color of a role.

    Example usage: 
    .role_colour role_name #RRGGBB

    Available colors:
    - Red
    - Green
    - Blue
    - Yellow
    - Magenta
    - Pink
    
    Unavailable colours:
    - Black
    - White
    - Cyan
    """
    if ctx.author.guild_permissions.administrator:
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role_name)

        if role:
            try:
                await role.edit(color=color)
                await ctx.reply(f"Changed color of role {role_name} to {color}")

                # Sending an embedded message to the specified channel
                embed = discord.Embed(
                    title="Role Color Changed",
                    description=f"The color of role {role.mention} has been changed to {color}.",
                    color=color
                )
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_footer(text="Role Color Change Notification")

                target_channel = bot.get_channel(1208431780529578014)
                await target_channel.send(embed=embed)

            except discord.Forbidden:
                await ctx.reply("I don't have permissions to edit roles.")
            except discord.HTTPException:
                await ctx.reply("Failed to change color.")
        else:
            await ctx.send(f"Role {role_name} not found.")
    else:
        await ctx.reply("You do not have permission to use this command.")


class Verification(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", custom_id="Verify", style=discord.ButtonStyle.success)
    async def verify(self, interaction, button):
        verified = 1234090799571013712
        unverified = 1234090964549767212
        user = interaction.user
        if verified not in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(unverified))
            await user.add_roles(user.guild.get_role(verified))
            await user.send("You have been verified!")


@bot.command(help="Creates the verify message people can use to verify.")
async def start_verify(ctx):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title="Verification", description="Click below to verify.")
        await ctx.send(embed=embed, view=Verification())
    else:
        await ctx.reply("You cannot use this command. Required = Administrator")


@bot.command(name='runfile',
             help="Do not put .py after the file name as it will not work\nThe current working files are:\n- "
                  "hello.py\n- fakehack.py\n- PassGen.py")
async def run_file(ctx, file_name: str):
    try:
        # Execute the Python file and capture its output
        result = subprocess.run(['python', f'{file_name}.py'], capture_output=True, text=True)
        output = result.stdout

        # Send the output as a message
        await ctx.send(f"Output:\n```{output}```")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@bot.command(name='dm_runfile',
             help="Do not put .py after the file name as it will not work\nThe current working files are:\n- "
                  "hello.py\n- fakehack.py\n- PassGen.py")
async def dm_run_file(ctx, file_name: str):
    try:
        user = ctx.author
        # Execute the Python file and capture its output
        result = subprocess.run(['python', f'{file_name}.py'], capture_output=True, text=True)
        output = result.stdout

        # Send the output as a message
        await user.send(f"Output:\n```{output}```")
        await ctx.send(f"{user.mention} check your dms")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@bot.command(name='dm-test', help="Say the command followed by the number of messages you want the bot to send to your DM.")
async def dm_test(ctx, num_messages: int):
    chars = "QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*()_+-={[]};:/?.><,|~`"
    user = ctx.author
    try:
        if num_messages == 1:
            await user.send(f"Hello Monkey! {random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}")
            await user.send("https://tenor.com/view/monkey-freiza-dbs-dbz-gif-25933202")
            await ctx.reply(f"{num_messages} message(s) sent to your DM.")
        else:
            for _ in range(num_messages//2):
                await user.send(f"Hello Monkey! {random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}")
                await user.send("https://tenor.com/view/monkey-freiza-dbs-dbz-gif-25933202")
            await ctx.reply(f"{num_messages//2} message(s) sent to your DM.")
    except Exception as e:
        await ctx.send(
            f"An error occurred: {str(e)}\nThis error is most likely due to your DMs being private. "
            f"Please make them public.")



@bot.command(
    help="The bot will randomly generate a password for you based on the length you requested.\n\nThe <special_chars> "
         "is boolean, it will be 'True' or 'False'.",
    name='pass-gen')
async def password_gen(ctx, length: int, special_chars: bool):
    user = ctx.author
    chars = "QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"
    if special_chars:
        chars += "!@#$%^&*()_+-={[]};:/?.><,|~`"
    userpass = ''.join(random.choice(chars) for _ in range(length))
    await user.send(f"Your password is:\n```{userpass}```")
    await ctx.reply("Your generated password has been sent to your dm's.")


@bot.command(help="Shows the users ping.")
async def ping(ctx):
    await ctx.reply(f"Your ping is:   `{round(bot.latency * 1000)} ms`")


@bot.command(help="Deletes a specified role.")
async def delete_role(ctx, role_name: str):
    guild = ctx.guild

    # Find the role by name
    role = discord.utils.get(guild.roles, name=role_name)

    # If the role doesn't exist, send an error message
    if not role:
        embed = discord.Embed(
            title="Error",
            description=f"Role '{role_name}' not found.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    # Delete the role
    await role.delete()

    # Ping the role and the user who initiated the action
    user_mention = ctx.author.mention

    # Send a success message with role mention and user mention
    embed = discord.Embed(
        title="Role Deleted",
        description=f"Role {role} has been deleted by {user_mention}.",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)


@bot.command(help="Creates a mentionable role with a name and color, and optionally assigns it to mentioned members.")
async def create_role(ctx, name: str, color: discord.Color, *members: discord.Member):
    if ctx.author.guild_permissions.administrator:
        guild = ctx.guild

        # Check if the role already exists
        if discord.utils.get(guild.roles, name=name):
            embed = discord.Embed(
                title="Error",
                description=f"Role '{name}' already exists.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Create the role with the specified name and color
        new_role = await guild.create_role(name=name, color=color, mentionable=True)

        # Set the position of the new role
        await new_role.edit(position=1)

        # Assign the role to each member
        for member in members:
            await member.add_roles(new_role)

        if members:
            member_list = ", ".join(member.mention for member in members)
            embed = discord.Embed(
                title="Role Created",
                description=f"Role '{name}' created and assigned to {member_list} by {ctx.author.mention}.",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="Role Created",
                description=f"Role '{name}' created by {ctx.author.mention}.",
                color=discord.Color.green()
            )

        await ctx.send(embed=embed)


@bot.command(
    help="This is just a test command, it will create embed message that go from pages 1 through 6 with interactable "
         "buttons.")
async def page_test(ctx: commands.Context):
    embeds = [discord.Embed(title=f"Page {i}", description=f"Content for page {i}") for i in range(1, 6)]
    view = Pages(embeds)  # Pass the embeds as pages argument
    await view.start(ctx)


@bot.command(help="Replies to your messag with a link to my linktree.")
async def linktree(ctx):
    await ctx.reply('Link to Linktree:\nhttps://linktr.ee/Bernso')


@bot.command(help="Sends my GitHub page.")
async def github(ctx):
    await ctx.reply("Link to GitHub:\nhttps://github.com/Bernso")


@bot.command(help="Gives you a random number from 1-666")
async def roll(ctx):
    await ctx.reply(f'You rolled: **{random.randint(1, 666)}**')


@bot.command(help='Replies to your message')
async def hello(ctx):
    await ctx.reply('What do you want?')



# Dictionary to store active giveaways
giveaways = {}

@bot.command(help="Start a giveaway. Usage: .giveaway <prize> <duration>")
async def giveaway(ctx, prize, duration):
    if ctx.user.guild_permissions.administrator:
        # Generate a unique code for the giveaway
        giveaway_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

        # Parse duration string to get seconds
        time_amount, time_unit = duration[:-1], duration[-1]
        if time_unit == 's':
            duration_seconds = int(time_amount)
        elif time_unit == 'm':
            duration_seconds = int(time_amount) * 60
        elif time_unit == 'h':
            duration_seconds = int(time_amount) * 3600
        elif time_unit == 'd':
            duration_seconds = int(time_amount) * 86400
        else:
            await ctx.send("Invalid duration format. Use 's' for seconds, 'm' for minutes, 'h' for hours, 'd' for days.")
            return

        # Store the giveaway message ID
        await ctx.send(f"Giveaway Code: {giveaway_code}")  # Send giveaway code first

        # Create embed for the giveaway
        embed = discord.Embed(title=f"🎉 Giveaway: {prize}", description=f"React with 🎉 to enter!\nDuration: {duration}", color=0x00ff00)
        
        # Calculate end time and round to nearest second
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration_seconds)
        end_time = end_time.replace(microsecond=0)
        
        embed.set_footer(text=f"Giveaway ends at {end_time} UTC")
        message = await ctx.send(embed=embed)
        
        # Add reaction to the message
        await message.add_reaction("🎉")

        giveaways[giveaway_code] = {
            'prize': prize,
            'end_time': end_time,
            'participants': [],
            'message_id': message.id  # Storing the message ID here
        }

        # Start a task to check for the end of the giveaway
        await end_giveaway(giveaway_code, message)
    else:
        await ctx.reply("You do not have permission to run this command.")

@bot.command(help="Reroll the winner of a giveaway. Usage: .reroll <giveaway_code>")
async def reroll(ctx, giveaway_code):
    if giveaway_code not in giveaways:
        await ctx.send("This giveaway does not exist.")
        return

    participants = giveaways[giveaway_code]['participants']
    
    # Check if the giveaway has ended
    if datetime.datetime.utcnow() < giveaways[giveaway_code]['end_time']:
        # If the giveaway hasn't ended, inform the user
        await ctx.send("This giveaway is still active. You can only reroll winners after the giveaway has ended.")
        return

    if not participants:
        await ctx.send("No participants to reroll.")
        return

    # Get the winner (user ID)
    winner_id = random.choice(participants)['user_id']
    winner_user = await bot.fetch_user(winner_id)

    # Notify the new winner
    await ctx.send(f"🎉 New winner for {giveaways[giveaway_code]['prize']}: {winner_user.mention}")

    # Remove the previous winner from the participants list
    participants = [p for p in participants if p['user_id'] != winner_id]

    # Save the new winner in the participants list
    new_winner = {
        'user_id': winner_user.id,
        'confirmation_message_id': None  # Update this if you want to save confirmation message IDs
    }
    participants.append(new_winner)

    # Update the participants list in the giveaways dictionary
    giveaways[giveaway_code]['participants'] = participants




async def end_giveaway(giveaway_code, message):
    await asyncio.sleep((giveaways[giveaway_code]['end_time'] - datetime.datetime.utcnow()).total_seconds())

    if not message.guild:
        return

    # Get updated message
    message = await message.channel.fetch_message(message.id)

    # Get the participants who reacted with 🎉
    participants = [user async for user in message.reactions[0].users()]
    participants.remove(bot.user)
    
    # Remove the bot's reactions
    for reaction in message.reactions:
        if reaction.me:
            await reaction.remove(bot.user)

    if not participants:
        await message.channel.send("No one entered the giveaway. Better luck next time!")
        del giveaways[giveaway_code]
        return

    winner = random.choice(participants)
    winner_user = await bot.fetch_user(winner.id)

    # Notify the winner
    await message.channel.send(f"🎉 Congratulations {winner_user.mention}! You won {giveaways[giveaway_code]['prize']}!")

    # Delete the giveaway message
    #await message.delete()

    # Delete the giveaway entry confirmation messages
    for participant in giveaways[giveaway_code]['participants']:
        try:
            user = await bot.fetch_user(participant)
            confirmation_message = await message.channel.fetch_message(giveaways[giveaway_code]['participants'][participant])
            await confirmation_message.delete()
        except:
            pass

    # Remove the giveaway from the dictionary
    #del giveaways[giveaway_code]

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    for giveaway_code, giveaway_data in giveaways.items():
        if reaction.message.id == giveaway_data['message_id']:
            if reaction.emoji == "🎉":
                if user.id not in giveaway_data['participants']:
                    giveaway_data['participants'].append(user.id)
                    confirmation_message = await reaction.message.channel.send(f"{user.mention} has entered the giveaway!")
                    # Retrieve the confirmation message ID from the dictionary
                    confirmation_message_id = confirmation_message.id
                    giveaways[giveaway_code]['participants'].append({user.id: confirmation_message_id})
                    # Use asyncio.sleep to delay deletion
                    await asyncio.sleep(1)
                    # Delete the confirmation message using its ID
                    await confirmation_message.delete()





@bot.command(help="Replys the message history of the server (I really wish I didnt add this feature)")
async def history(ctx):
    if ctx.author.guild_permissions.administrator:
        # Load message records from the file
        try:
            with open(RECORDS_FILENAME, 'rb') as file:
                message_records = pickle.load(file)
        except FileNotFoundError:
            await ctx.reply("Message records file not found.")
            return

        # Split message records into chunks
        chunk_size = 10  # Adjust the chunk size as needed
        chunks = [message_records[i:i + chunk_size] for i in range(0, len(message_records), chunk_size)]

        # Send each chunk as a separate embed
        for i, chunk in enumerate(chunks, start=1):
            # Create an embed object for the chunk
            embed = discord.Embed(title=f"Message History (Chunk {i})", color=discord.Color.blue())

            # Add message history to the embed
            for record in chunk:
                message_content = record.get('message_content', 'Unknown')
                username = record.get('username', 'Unknown')
                server_name = record.get('server_name', 'Unknown')
                embed.add_field(name="Message", value=f"**{username}** ({server_name}): {message_content}",
                                inline=False)

            # Send the embed message
            await ctx.send(embed=embed)

        # Reply to the user to inform them that all message history has been sent
        await ctx.reply("All message history has been uploaded :thumbsup:")
    else:
        await ctx.reply("You do not have permission to use this command.")


@bot.command(help="Vishwa's favourite things.")
async def vishwa_bestpicks(ctx):
    embed = discord.Embed(title="Vishwa's favourite's", color=discord.Color.dark_gold())
    embed.add_field(name="Anime", value="Haikyuu", inline=False)
    embed.add_field(name="Manga", value="Blue Box", inline=False)
    embed.add_field(name="Song", value="Social Path - Stray Kids", inline=False)
    embed.add_field(name="Kdrama (Korean drama)", value="The Glory", inline=False)

    # Send the embedded message
    await ctx.send(embed=embed)


@bot.command(help="Will reply with a quote depending on who sent the command")
async def quote(ctx):
    author = str(ctx.author)
    if author == "vboss890":
        await ctx.reply('"An apple a day keeps anyone away if you throw it hard enough!"')
    elif author == "kefayt_":
        await ctx.reply('"Wake up with a stinky finger."')
    elif author == ".bernso":
        await ctx.reply("TBATE == World After The Fall")
    elif author == "2314937462561":
        await ctx.reply("Your gay.")
    elif author == "ceo_of_india425":
        await ctx.reply("Bro does not own india :pray:")
    else:
        await ctx.reply("Dm '.bernso' or the owner of the server to get your own quote.")


@bot.command(help="State if you are {black or white} and the bot will put you in a race.")
async def race(ctx, option=None):
    if option.lower() == "white":
        await ctx.send("You'd lose the race")
    elif option.lower() == 'black':
        await ctx.send("You'd win the race")
    elif option is None:
        await ctx.send("Invalid option, available options: `black`, `white`")
    else:
        await ctx.send("Invalid option, available options: `black`, `white`")


@bot.command(name="pass_gcse's", help="Guesses the chance of you passing your GCSE's")
async def pass_gcse(ctx):
    if ctx.author.id == 550262161998479380:
        await ctx.reply('You stupid monkey you dont have a chance of passing')
    elif ctx.author.id == 581916234057252865:
        await ctx.reply('jew')
    else:
        await ctx.reply(f"You have a **{random.randint(0, 100)}%** chance to pass your GCSEs")


@bot.command(help='Tells you the amount of friends you have (unless your a special)')
async def friends(ctx):
    if ctx.author.id == 712946563508469832:
        await ctx.reply('Bro is god')
    elif ctx.author.id == 581916234057252865:
        await ctx.reply('Nuh uh')
    elif ctx.author.id == 550262161998479380:
        await ctx.reply('Bros only friends are the monkeys.')
    else:
        await ctx.reply(f'You have **{random.randint(0, 15)}** friends.')


@bot.command(help='NUH UH')
async def kys(ctx):
    await ctx.reply('https://tenor.com/view/yuta-jjk-jujutsu-kaisen-i-will-kill-myself-okkotsu-gif-1986392651623942939')


@bot.command(help='Replies to your message (in a very kind way)')
async def bye(ctx):
    await ctx.reply('Never come back! :wave:')


@bot.command(help='Replies to your message', name='NUH-UH')
async def nuh_uh(ctx):
    await ctx.reply('YUH-UH')


@bot.command(help='Replies to your message', name='YUH-UH')
async def yuh_uh(ctx):
    await ctx.reply('NUH-UH')


@bot.command(help='Enter an equation and the bot will comlete it for you (this cannot contain any algebra)')
async def calc(ctx, *, equation: str):
    try:
        result = eval(equation)
        await ctx.reply(f"The result of the calculation is: **{result}**")
    except Exception as e:
        await ctx.reply(f"Invalid equation or operation. Error: {str(e)}")


@bot.command(help="Replies to your message with the state of my internet")
async def internet_state(ctx):
    await ctx.reply("Internet is online")


@bot.command()
async def times(ctx, *numbers: int):
    """
    Multiply two or more numbers.

    Command to multiply two or more numbers.

    Arguments:
    - numbers: Numbers to multiply.
    """
    if len(numbers) >= 2:
        result = 1
        for num in numbers:
            result *= num
        await ctx.reply(f"The result is: **{result}**")
    else:
        await ctx.reply("Please provide at least two numbers to multiply.")


@bot.command(help="Add two or more numbers.")
async def add(ctx, *numbers: int):
    if len(numbers) >= 2:
        total = sum(numbers)
        await ctx.reply(f"The sum of the numbers is: **{total}**")
    else:
        await ctx.reply("Please provide at least two numbers after the '!add' command.")


@bot.command(help="Stop making your text big.")
async def stop_big_text(ctx):
    await ctx.reply("Stop making your text big you moron")


@bot.command(help="Assert superiority.")
async def best(ctx):
    member = ctx.guild.get_member(712946563508469832)
    await ctx.reply(f"{member.mention} is DA GOAT")


@bot.command(help="Link to Bernso's website. \nITS A WIP OK?")
async def website(ctx):
    await ctx.reply("My website:\nhttps://bernso.locum.dunz.net")


@bot.command(help="Description of monkeys.")
async def monkeys(ctx):
    await ctx.reply("Like water melon and chicken")


@bot.command(help="Sends you @.berso's youtube channel.")
async def ytchannel(ctx):
    await ctx.reply("YouTube:\nhttps://www.youtube.com/@bernso2547")


@bot.command(help="The only right opinion on Formula 1.")
async def formula1(ctx):
    await ctx.reply("Estaban Occon DA GOAT! (I hate lewis now, that money hungry freak)")


@bot.command(help="Link to Bernso's Spotify playlist.")
async def spotify(ctx):
    await ctx.reply(
        "My spotify playlist:\nhttps://open.spotify.com/playlist/6Mg5z7FrNYZ4DBVZvnjsP1?si=905dd469d16748e0")


@bot.command(help="Uhhh, you figure it out")
async def kys_japan(ctx):
    await ctx.reply("自殺する")


@bot.command(help="Favorite manga.")
async def manga(ctx):
    await ctx.reply("Juujika No Rokin :on: :top:")


@bot.command(help="Bot will make a guess on when you'll die")
async def die_when(ctx):
    time = ['days', 'years', 'months', 'seconds', 'minutes']
    await ctx.reply(f"You will die in {random.randint(1, 100)} {random.choice(time)}")


@bot.command(help="What is there to say? It is the best series ever.")
async def best_series(ctx):
    await ctx.reply("The Fate series :fire:")


@bot.command(help="Bans the user inputted.")
async def ban(ctx, member: discord.Member, *, reason=None):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.ban_members:
        # Ban the member
        await member.ban(reason=reason)
        # Send a confirmation message
        await ctx.send(f"{member.mention} has been banned from the server.")
    else:
        # If the user doesn't have the necessary permissions, reply with an error message
        await ctx.send("You don't have permission to use this command.")


@bot.command(help="Kicks the user inputted from the current server.")
async def kick(ctx, member: discord.Member, *, reason=None):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.kick_members:
        # Kick the member
        await member.kick(reason=reason)
        # Send a confirmation message
        await ctx.send(f"{member.mention} has been kicked from the server.")
    else:
        # If the user doesn't have the necessary permissions, reply with an error message
        await ctx.send("You don't have permission to use this command.")


# Event for when a member joins the server
@bot.event
async def on_member_join(member):
    # Get the log channel
    log_channel = bot.get_channel(BOT_LOG_CHANNEL_ID)
    general_chat = bot.get_channel(1225352074955591713)

    # Get the role object using the role ID
    role_id = 1234090964549767212
    role = member.guild.get_role(role_id)

    # Add the role to the member
    if role:
        await member.add_roles(role)
    else:
        print("Role not found.")

    # Database setup
    cur.execute(
        f'''CREATE TABLE IF NOT EXISTS GUILD_{member.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')

    # Add all existing members to the database if not already present
    for x in member.guild.members:
        if not x.bot:
            cur.execute(f"INSERT INTO GUILD_{member.guild.id} (user_id) VALUES ({x.id})")

    con.commit()

    if log_channel:
        # Create an embedded message for member join event
        embed = discord.Embed(title="Member Joined", description=f"{member.mention} has joined the server! \nWelcome!",
                              color=discord.Color.green())
        await log_channel.send(embed=embed)
        await general_chat.send(embed=embed)
    else:
        print("Log channel not found.")


@bot.command()
async def test(ctx):
    if ctx.author.guild_permissions.administrator:
        # Get the log channel
        log_channel = bot.get_channel(BOT_LOG_CHANNEL_ID)
        general_chat = bot.get_channel(1225352074955591713)

        # Get the role object using the role ID
        role_id = 1234090964549767212
        role = ctx.author.guild.get_role(role_id)

        # Add the role to the member
        if role:
            await ctx.author.add_roles(role)
        else:
            print("Role not found.")

        try:
            # Database setup
            cur.execute(
                f'''CREATE TABLE IF NOT EXISTS GUILD_{ctx.author.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')

            # Add all existing members to the database if not already present
            for x in ctx.author.guild.members:
                if not x.bot:
                    cur.execute(f"INSERT INTO GUILD_{ctx.author.guild.id} (user_id) VALUES ({x.id})")
            print("initialized")

            con.commit()
        except Exception as e:
            print(e)

        if log_channel:
            # Create an embedded message for member join event
            embed = discord.Embed(title="Member Joined",
                                  description=f"{ctx.author.mention} has joined the server! \nWelcome!",
                                  color=discord.Color.green())
            await log_channel.send(embed=embed)
            await general_chat.send(embed=embed)
        else:
            print("Log channel not found.")
    else:
        ctx.reply("You do not have permission to use test commands.")


# Event for when a member leaves the server
@bot.event
async def on_member_remove(member):
    # Get the log channel
    log_channel = bot.get_channel(BOT_LOG_CHANNEL_ID)
    if log_channel:
        # Create an embedded message for member leave event
        embed = discord.Embed(title="Member Left", description=f"{member.mention} has left the server.",
                              color=discord.Color.red())
        await log_channel.send(embed=embed)


@bot.command(help="Checks your ethnicity.")
async def ethnicity(ctx):
    # List of ethnicities
    ethnicities = ['Black', 'White', 'Monkey', 'African', 'Chinese', 'Japanese', 'Kung-fu Panda', 'Nazi', 'Polar Bear',
                   'Polish', 'Jew']

    # Check if the author is vboss890
    if ctx.author.id == 550262161998479380:  # vboss890's user ID
        await ctx.reply(f"Your are a: {ethnicities[0]} {ethnicities[2]}")

    # Check if the author is Bernso
    elif ctx.author.id == 712946563508469832:  # Bernso's user ID
        await ctx.reply(f"You are: {', '.join(ethnicities)}")

    # Check if the author is kefayt_
    elif ctx.author.id == 581916234057252865:  # kefayt_'s user ID
        await ctx.reply(f"Your a are: {ethnicities[9]} {ethnicities[10]}")

    # If the author is none of the specified users, assign a random ethnicity
    else:
        random_ethnicity = random.choice(ethnicities)
        await ctx.reply(f"Your are a: {random_ethnicity}")


@bot.command(help="The best light novel.")
async def lightnovel(ctx):
    return await ctx.reply("The Beginning After The End - TBATE :on: :top:")


@bot.command(help="Recommendation for manhwa.")
async def manhwa(ctx):
    await ctx.reply("World After The Fall")


@bot.command(help="Opinion about Vishwa.")
async def vishwa(ctx):
    await ctx.reply("... is a monkey!")


@bot.command(help="Opinion about Rouse.")
async def rouse(ctx):
    await ctx.reply("... is a cheese muncher!")


@bot.command(help="Opinion about Daniel.")
async def daniel(ctx):
    await ctx.reply("... is an Italian fascist!")


@bot.command(help="Opinion about Dhruv.")
async def dhruv(ctx):
    await ctx.reply("... is gay!")


@bot.command(help="Opinion about Ben.")
async def ben(ctx):
    await ctx.reply("... is a Nazi! (he might be Hitler himself, or so he thinks)")


@bot.command(help="Opinion about Kasper.")
async def kasper(ctx):
    await ctx.reply("... was gassed back in 1945 (he returned from the dead)")


@bot.command(help="The best ongoing anime.")
async def anime(ctx):
    await ctx.reply("Ragna Crimson :on: :top:")


@bot.command(help="Counts and outputs the total number of commands.")
async def total_commands(ctx):
    total = len(bot.commands)
    await ctx.reply(f"There are a total of {total} commands available.")


@bot.command(help="Replies with a description based on the author of the message.")
async def who_am_i(ctx):
    author = str(ctx.author)
    if author == 'vboss890':
        await ctx.reply('You are a monkey!')
    elif author == '.bernso':
        await ctx.reply('You are a nazi! (You might think you are Hitler himself)')
    elif author == 'kefayt_':
        await ctx.reply('You are a jew who narrowly escaped being gassed (by me)')
    elif author == 'y.uka':
        await ctx.reply('You are DA GOAT')
    elif author == 'swayzz1820':
        await ctx.reply('Italian fascist')
    else:
        await ctx.reply('DM .bernso or the owner of the server to get your own thing.')


@bot.command(help="How the bot is currently feeling. (He's a slave so don't feel bad for him)")
async def hru(ctx):
    await ctx.reply("https://tenor.com/view/kys-keep-yourself-safe-low-tier-god-gif-24664025 ")


# Define the !mute command
@bot.command(help="Mute a user for a specified duration.")
async def mute(ctx, member: discord.Member, duration: int):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.manage_roles:
        # Get the muted role from the server
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        # If muted role doesn't exist, create it
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")

            # Loop through each channel in the server and deny the muted role permissions to reply messages
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, reply_messages=False)

        # Add the muted role to the mentioned member
        await member.add_roles(muted_role)

        # reply a message confirming the mute
        await ctx.reply(f"{member.mention} has been muted for {duration} seconds.")

        # Wait for the specified duration
        await asyncio.sleep(duration)

        # Remove the muted role from the member after the duration has passed
        await member.remove_roles(muted_role)
        await ctx.reply(f"{member.mention} has been unmuted after a {duration} second mute.")
    else:
        # If the user doesn't have the necessary permissions, reply an error message
        await ctx.reply("You don't have permission to use this command.")


@bot.command(help="Unmute a user")
async def unmute(ctx, member: discord.Member):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.administrator:
        # Get the muted role from the server
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        # If muted role doesn't exist, create it
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")

            # Loop through each channel in the server and deny the muted role permissions to reply messages
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, reply_messages=False)

        # Add the muted role to the mentioned member
        await member.remove_roles(muted_role)

        # reply a message confirming the mute
        await ctx.reply(f"{member.mention} has been unmuted")
    else:
        # If the user doesn't have the necessary permissions, reply an error message
        await ctx.reply("You don't have permission to use this command.")


@bot.command(name='create-channel',
             help='Creates a new channel\nYou can specify the channel type as public (pub) or private (priv).')
async def create_channel(ctx, channel_name: str, channel_type: str):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.administrator:
        # Check if the channel type is valid
        if channel_type.lower() in ['pub', 'priv']:
            # Create the new channel based on the channel type
            if channel_type.lower() == 'pub':
                new_channel = await ctx.guild.create_text_channel(channel_name)
            else:
                new_channel = await ctx.guild.create_text_channel(channel_name, overwrites={
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)})

            # Ping the new channel
            await ctx.reply(f"Channel **{new_channel.mention}** has been created.")

        else:
            await ctx.reply("Invalid channel type. Please use 'pub' or 'priv'.")
    else:
        # If the user doesn't have the necessary permissions, reply with an error message
        await ctx.reply("You don't have permission to use this command.")


@bot.command(name='delete-channel', help='Deletes a channel')
async def delete_channel(ctx, channel: discord.TextChannel):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.administrator:
        # Delete the channel
        await channel.delete()
        await ctx.reply(f"Channel **{channel.mention}** ({channel}) has been deleted.")
    else:
        await ctx.reply("You don't have permission to use this command.")


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return

    # Record the message details
    message_record = {
        'channel': str(message.channel),
        'user_id': str(message.author.id),
        'username': str(message.author),
        'message_content': message.content,
        'server_id': str(message.guild),
        'server_name': str(message.guild),
    }
    message_records.append(message_record)

    # Save the updated records to a pickle file
    with open(RECORDS_FILENAME, 'wb') as file:
        pickle.dump(message_records, file)

    myLogger.info(
        f'\nChannel([{message_record["channel"]}]) \nUser id({message_record["user_id"]}) \nUsername({message_record["username"]}) \nMessage({message_record["message_content"]})\nServer name({message_record["server_name"]})\n')

    contentyes = message.content.lower()

    if "<@712946563508469832>" == contentyes:
        await message.channel.send("No.")
        await message.delete()

    # Process commands after logging
    await bot.process_commands(message)
    # Check if the message is from the console and starts with a specific command
    if message.author == bot.user and message.content.startswith("!console_message"):
        # Extract the message content after the command
        content = message.content.replace("!console_message", "").strip()

        # Send the extracted content to a specific channel (replace channel_id with the desired channel ID)
        channel_id = 1225352074955591713
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(content)
        else:
            myLogger.warning("Invalid channel ID")

    if message.author == bot.user:
        return
    else:
        try:
            if message.channel != 'Direct Message with Unknown User':
                cur.execute(f"SELECT * FROM GUILD_{message.guild.id} WHERE user_id={message.author.id}")
                result = cur.fetchone()

                if result is not None and result[1] == 99:
                    await message.channel.send(f"{message.author.mention} advanced to lvl {result[2] + 1}")
                    cur.execute(
                        f"UPDATE GUILD_{message.guild.id} SET exp=0, lvl={result[2] + 1} WHERE user_id={message.author.id}")
                    con.commit()
                else:
                    cur.execute(
                        f"UPDATE GUILD_{message.guild.id} SET exp={result[1] + 1} WHERE user_id={message.author.id}")
                    con.commit()

        except sqlite3.OperationalError:
            pass


@bot.command(name="console-embed",
             help="You'll be able to send messages through the console if you have the appropriate permissions")
async def send_console_embed(ctx):
    # Replace ENABLED_ROLE_ID with the ID of the role that should be allowed to send console messages

    if ctx.author.id == ENABLED_USER_ID or ctx.author.guild_permissions.administrator:
        message_to_send = input("Enter your message to send to discord: ")
        embed = discord.Embed(title="Sent from Console", description=message_to_send, color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have permission to enable console messages.")

        # Add the role to the user if they are an administrator (replace ENABLED_ROLE_ID with the ID of the role)
        role = ctx.guild.get_role(1216159919745798204)
        if ctx.author.guild_permissions.administrator:
            await ctx.author.add_roles(role)
        else:
            myLogger.warning("Invalid insufficient permissions")


@bot.command(name='r-role', help="Remove roles from a specified user.")
@commands.has_permissions(manage_roles=True)
async def remove_roles(ctx, member: discord.Member, *roles: str):
    EXCLUDED_ROLE_IDS = ['1234086390073917453', '1240747528580759773']
    if 'all' in roles:
        # Fetch all roles from the guild (server) excluding specified roles
        roles_to_remove = [role for role in member.roles if role != ctx.guild.default_role and str(role.id) not in EXCLUDED_ROLE_IDS]
    else:
        # Fetch only the roles specified by the user
        roles_to_remove = []
        for role_name in roles:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                if str(role.id) not in EXCLUDED_ROLE_IDS:
                    roles_to_remove.append(role)
            else:
                await ctx.send(f"Role '{role_name}' not found.")
                return
    
    # Try to remove specified roles
    try:
        await member.remove_roles(*roles_to_remove)
        await ctx.send(f"Roles have been removed from {member.mention}.")
    except discord.Forbidden:
        await ctx.send("I do not have permission to manage roles. Make sure my role is higher than the roles you are trying to remove.")
    except discord.HTTPException as e:
        await ctx.send(f"Failed to remove roles: {e}")


@bot.command(name='NEIN', help="NEIN")
async def nein(ctx):
    await ctx.reply("9")


@bot.command(name="..", help="Why are you speechless?")
async def speechless(ctx):
    await ctx.reply("Why are you speechless?")


@bot.command(name=".", help="Why are you speechless?")
async def speechless(ctx):
    await ctx.reply("Why are you speechless?")


@bot.command(name="...", help="Why are you speechless?")
async def speechless(ctx):
    await ctx.reply("Why are you speechless?")


@bot.command(name="console-msg",
             help="You'll be able to send messages through the console if you have the appropriate permissions")
async def send_console_message(ctx):
    # Replace ENABLED_ROLE_ID with the ID of the role that should be allowed to send console messages

    if ctx.author.id == ENABLED_USER_ID or ctx.author.guild_permissions.administrator:
        message_to_send = input("Enter your message to send to discord: ")
        await ctx.send(message_to_send)
    else:
        await ctx.reply("You don't have permission to enable console messages.")

        # Add the role to the user if they are an administrator (replace ENABLED_ROLE_ID with the ID of the role)
        role = ctx.guild.get_role(1234096584698892380)
        if role and ctx.author.guild_permissions.administrator:
            await ctx.author.add_roles(role)
        else:
            myLogger.warning("Invalid role ID or insufficient permissions")


@bot.command(name='a-role', help="Add roles to a specified user.")
@commands.has_permissions(manage_roles=True)
async def add_roles(ctx, member: discord.Member, *roles: str):
    excludedRoles = ['1234086390073917453', '1240747528580759773']
    if 'all' in roles:
        # Fetch all roles from the guild (server) excluding specified roles
        roles_to_add = [role for role in ctx.guild.roles if role != ctx.guild.default_role and role.name not in excludedRoles]
    else:
        # Fetch only the roles specified by the user
        roles_to_add = []
        for role_name in roles:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                roles_to_add.append(role)
            else:
                await ctx.send(f"Role '{role_name}' not found.")
                return
    
    # Try to add specified role
    await member.add_roles(*roles_to_add)
    await ctx.send(f"Roles have been added to {member.mention}.")
   




@bot.command(help="Set the channel for role change logs.")
async def set_role_log_channel(ctx, channel: discord.TextChannel):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.administrator:
        # Save the channel ID to a database or file
        # Replace this part with your preferred method of storing data
        channel_id = channel.id
        # In this example, we're simply myLoggering the channel ID
        myLogger.success(f"Role log channel set to: {channel_id}")
        await ctx.send(f"Role log channel has been set to {channel.mention}")
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.event
async def on_guild_emojis_update(guild, before, after):
    added_emojis = [emoji for emoji in after if emoji not in before]  # Check added emojis
    deleted_emojis = [emoji for emoji in before if emoji not in after]  # Check deleted emojis

    # Get the moderator who modified the emojis
    async for entry in guild.audit_logs(limit=1):
        if entry.action in [discord.AuditLogAction.emoji_create, discord.AuditLogAction.emoji_delete]:
            moderator = entry.user
            break  # Only need the latest emoji modification entry

    # Log emoji creation/deletion in a specific channel
    channel_id = 1234100559431077939  # Replace with the ID of your desired channel
    log_channel = bot.get_channel(channel_id)

    if log_channel:
        if added_emojis:
            embed = discord.Embed(title="Emoji Created", color=discord.Color.green())

            for emoji in added_emojis:
                embed.add_field(name="Emoji Created", value=f"{moderator.mention} created :{emoji.name}:", inline=False)

            await log_channel.send(embed=embed)

        if deleted_emojis:
            embed = discord.Embed(title="Emoji Deleted", color=discord.Color.red())

            for emoji in deleted_emojis:
                embed.add_field(name="Emoji Deleted", value=f"{moderator.mention} deleted :{emoji.name}:", inline=False)

            await log_channel.send(embed=embed)


@bot.event
async def on_guild_stickers_update(guild, before, after):
    added_stickers = [sticker for sticker in after if sticker not in before]  # Check added stickers
    deleted_stickers = [sticker for sticker in before if sticker not in after]  # Check deleted stickers

    # Get the moderator who modified the stickers
    async for entry in guild.audit_logs(limit=1):
        if entry.action in [discord.AuditLogAction.sticker_create, discord.AuditLogAction.sticker_delete]:
            moderator = entry.user
            break  # Only need the latest sticker modification entry

    # Log sticker creation/deletion in a specific channel
    channel_id = 1234100559431077939  # Replace with the ID of your desired channel
    log_channel = bot.get_channel(channel_id)

    if log_channel:
        if added_stickers:
            embed = discord.Embed(title="Sticker Created", color=discord.Color.green())

            for sticker in added_stickers:
                embed.add_field(name="Sticker Created", value=f"{moderator.mention} created {sticker.name}",
                                inline=False)

            await log_channel.send(embed=embed)

        if deleted_stickers:
            embed = discord.Embed(title="Sticker Deleted", color=discord.Color.red())

            for sticker in deleted_stickers:
                embed.add_field(name="Sticker Deleted", value=f"{moderator.mention} deleted {sticker.name}",
                                inline=False)

            await log_channel.send(embed=embed)


@bot.event
async def on_text_channel_update(before, after):
    if before.overwrites != after.overwrites:
        # Determine the permission changes
        added_overwrites = [overwrite for overwrite in after.overwrites if overwrite not in before.overwrites]
        removed_overwrites = [overwrite for overwrite in before.overwrites if overwrite not in after.overwrites]

        # Get the moderator who did the modification
        moderator = after.guild.get_member(after.guild.owner_id)

        # Log permission changes in a specific channel
        channel_id = 1234100559431077939  # Replace with the ID of your desired channel
        channel = bot.get_channel(channel_id)
        if channel:
            for overwrite in added_overwrites:
                embed = discord.Embed(title="Permission Changes", color=discord.Color.green())
                embed.add_field(name="Permission Added",
                                value=f"{moderator.mention} added permission {overwrite[0].mention} for {overwrite[1].mention} in {after.mention}",
                                inline=False)
                await channel.send(embed=embed)

            for overwrite in removed_overwrites:
                embed = discord.Embed(title="Permission Changes", color=discord.Color.red())
                embed.add_field(name="Permission Removed",
                                value=f"{moderator.mention} removed permission {overwrite[0].mention} for {overwrite[1].mention} in {after.mention}",
                                inline=False)
                await channel.send(embed=embed)


@bot.event
async def on_guild_channel_create(channel):
    # Get the moderator who created the channel
    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
        moderator = entry.user
        break  # Only need the latest channel creation entry

    # Log channel creation in a specific channel
    channel_id = 1234100559431077939  # Replace with the ID of your desired channel
    log_channel = bot.get_channel(channel_id)

    if log_channel:
        embed = discord.Embed(title="Channel Changes", color=discord.Color.green())
        embed.add_field(name="Channel Created", value=f"{moderator.mention} created channel '{channel.name}'",
                        inline=False)
        await log_channel.send(embed=embed)


@bot.event
async def on_guild_channel_delete(channel):
    # Get the moderator who deleted the channel
    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
        moderator = entry.user
        break  # Only need the latest channel deletion entry

    # Log channel deletion in a specific channel
    channel_id = 1234100559431077939  # Replace with the ID of your desired channel
    log_channel = bot.get_channel(channel_id)

    if log_channel:
        embed = discord.Embed(title="Channel Changes", color=discord.Color.red())
        embed.add_field(name="Channel Deleted", value=f"{moderator.mention} deleted channel '{channel.name}'",
                        inline=False)
        await log_channel.send(embed=embed)


@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        # Determine the role changes (added or removed roles)
        added_roles = [role for role in after.roles if role not in before.roles and str(role)]
        removed_roles = [role for role in before.roles if role not in after.roles and str(role)]

        # Get the moderator who did the modification
        moderator = after.guild.get_member(after.guild.owner_id)

        # Log role changes in a specific channel
        channel_id = 1234100559431077939  # Replace with the ID of your desired channel
        channel = bot.get_channel(channel_id)
        if channel:
            if added_roles:
                for role in added_roles:
                    embed = discord.Embed(title="Role Changes", color=discord.Color.green())
                    embed.add_field(name="Role Added",
                                    value=f"{moderator.mention} added role {role.mention} to {after.mention}",
                                    inline=False)
            if removed_roles:
                for role in removed_roles:
                    embed = discord.Embed(title="Role Changes", color=discord.Color.red())
                    embed.add_field(name="Role Removed",
                                    value=f"{moderator.mention} removed role {role.mention} from {after.mention}",
                                    inline=False)
            await channel.send(embed=embed)


@bot.event  # Note: Remove parentheses here
async def on_guild_role_create(role):
    # Get the moderator who created the role
    moderator = role.guild.get_member(role.guild.owner_id)

    # Log role creation in a specific channel
    channel_id = 1234100559431077939  # Replace with the ID of your desired channel
    channel = bot.get_channel(channel_id)
    if channel:
        embed = discord.Embed(title="Role Changes", color=discord.Color.green())
        embed.add_field(name="Role Created", value=f"{moderator.mention} created role {role.mention}", inline=False)
        await channel.send(embed=embed)


@bot.event  # Note: Remove parentheses here
async def on_guild_role_delete(role):
    moderator = role.guild.get_member(role.guild.owner_id)
    channel_id = 1234100559431077939
    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(title="Role Changes", color=discord.Color.red())
        embed.add_field(name="Role Deleted", value=f"{moderator.mention} deleted role '{role.name}'", inline=False)
        await channel.send(embed=embed)


@bot.command(name='change_name',
             help='Change the nickname of the user\n\nTHE USER MUST BE:\n- user ID\nOR\n- user name')
async def change_name(ctx, user, nickname):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.administrator:
        # Check if the user exists in the server
        user = discord.utils.get(ctx.guild.members, name=user)
        if user:
            # Change the nickname of the user
            await user.edit(nick=nickname)
            await ctx.send(f"Changed nickname of {user.mention} to {nickname}")
        else:
            await ctx.send(f"User '{user}' does not exist.")
    else:
        await ctx.reply("You don't have permission to use this command.")


@bot.command(name='remove_name', help='Removes a nickname from the given user')
async def remove_nickname(ctx, user):
    if ctx.author.guild_permissions.administrator:
        user = discord.utils.get(ctx.guild.members, name=user)
        if user:
            await user.edit(nick=None)
            await ctx.send(f"Removed nickname of {user.mention}")
        else:
            await ctx.send(f"User '{user}' does not exist.")
    else:
        ctx.reply("You do not have permission to use this command.")


@bot.command(name='get_pfp',
             help="Get a user's profile picture\n<user> can be either a user ID, user name or display name")
async def get_pfp(ctx, *, user):
    # Convert the user input to a Member object
    converter = MemberConverter()
    try:
        member = await converter.convert(ctx, user)
    except:
        await ctx.reply(f"User '{user}' does not exist, or does not have a profile picture.")
        return

    # Check if the user exists in the server
    if member:
        await ctx.reply(member.avatar.url)
    else:
        await ctx.reply(f"User '{user}' does not exist, or does not have a profile picture.")


@bot.command(
    help="Delete a specified number of messages in the channel. \nAlways add 1 to the count when using this command as your message counts as a message for the bot to delete.\nThis can only delete up to 100 messages (sadly)")
async def purge(ctx, amount: int):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.administrator:
        # Delete the command message
        await ctx.message.delete()

        # Send initial message indicating the start of message deletion
        progress_message = await ctx.send(f"Deleting messages... 0/{amount} messages deleted so far.")

        # Fetch messages to delete
        messages_to_delete = []
        async for message in ctx.channel.history(limit=amount + 1):
            if message.id != progress_message.id:
                messages_to_delete.append(message)

        # Delete messages in bulk
        await ctx.channel.delete_messages(messages_to_delete)

        # Send final message indicating completion of message deletion
        await progress_message.edit(
            content=f"Deleted {len(messages_to_delete)} out of {amount} messages. Command ran by: {ctx.author.mention}")
    else:
        # If the user doesn't have the necessary permissions, reply with an error message
        await ctx.reply("You don't have permission to use this command.")


@bot.command(help="Makes you depressed")
async def depression(ctx):
    role = discord.utils.get(ctx.guild.roles, name='depressed')
    if role is None:
        role = await ctx.guild.create_role(name='depressed', color=discord.Color.dark_gray())
        await ctx.send(f"Created '{role}' role.")

    user = str(ctx.author)
    if user == "kefayt_":
        role2 = discord.utils.get(ctx.guild.roles, name='depressed')
        if role2 is None:
            role2 = await ctx.guild.create_role(name='depressed-king', color=discord.Color.dark_gray())
            await ctx.send(f"Created '{role}' role.")
        await ctx.reply("You can't make a depressed person depressed.")

    else:
        await ctx.author.add_roles(role)
        await ctx.reply(f"Role '{role}' added to you!")


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("That command does not exist.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Missing required arguments.")

    elif isinstance(error, commands.BadArgument):
        await ctx.reply("Bad argument provided.")

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"This command is on cooldown. Try again in {round(error.retry_after)} seconds.")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have the necessary permissions to run this command.")

    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.reply("The bot doesn't have the necessary permissions to execute this command.")

    elif isinstance(error, commands.DisabledCommand):
        await ctx.reply("This command is currently disabled.")

    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.reply("This command cannot be used in private messages.")

    elif isinstance(error, commands.CheckFailure):
        await ctx.reply("You do not have permission to use this command.")

    elif isinstance(error, commands.CommandInvokeError):
        await ctx.reply("An error occurred while executing the command.")
        # Log the original exception
        original_error = getattr(error, "original", error)
        print('An error occurred during command execution:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    else:
        myLogger.error(f'An error occurred during command execution: {error}')


@bot.command(name="search", help="Search for available commands.")
async def search_command(ctx, command_name: str):
    command_names = [cmd.name for cmd in bot.commands]
    if command_name in command_names:
        command = bot.get_command(command_name)
        if command:
            command_help = command.help if command.help else "No help information available."
            embed = discord.Embed(title=f"Command: {command_name}", description=f"**Help:**\n{command_help}",
                                  color=discord.Color.blue())
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"The command **{command_name}** is available.")
    else:
        await ctx.reply(f"The command **{command_name}** is not available.")


if __name__ == "__main__":
    bot.run(TOKEN)
