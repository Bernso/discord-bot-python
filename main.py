from logging import warn
import discord
from discord.ext import commands, tasks
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




os.system('cls')


load_dotenv()
RECORDS_FILENAME = os.getenv('ENVRECORDS_FILENAME')
TOKEN = os.getenv('ENVDISCORD_TOKEN')
ENABLED_USER_ID = 712946563508469832 # My user id
BOT_LOG_CHANNEL_ID = 1234100559431077939
VERIFIED_ROLE_NAME = "Verified"


class print:
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
    print.warning("Message records file not found. Creating a new one.")
    yes = open('message_records.pkl', 'w')
    yes.close()
except EOFError:
    message_records = []
    print.error("The message records file is empty or corrupted.")





# replys message history
async def reply_message_history(message, message_records):
    
    # Extract message content, username, and server name for each record
    message_history = '\n'.join([f"{record.get('message_content', 'Unknown')} - {record.get('username', 'Unknown')} ({record.get('server_name', 'Unknown')})" for record in message_records])
    
    # Split message into chunks of 1900 characters or less
    chunks = [message_history[i:i+1900] for i in range(0, len(message_history), 1900)]
    
    # reply each chunk as a separate message
    for chunk in chunks:
        await message.channel.reply(f"```{chunk}```")
    
    # Reply to the user to inform them that all message history chunks have been sent
    await message.reply("All message history has been uploaded :thumbsup:")


# Function to send the timed message
async def send_timed_message():
    await bot.wait_until_ready()
    channel = bot.get_channel(1225352074955591713)
    while not bot.is_closed():
        # Send your message here
        await asyncio.sleep(800)
        await channel.send("Hi")
        # Wait for 1 hour (3600 seconds) 3 hours (10800)
        await asyncio.sleep(10000)





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
        embed_pages = []
        current_page = 1
        commands_per_page = 15  # Number of commands to display per page

        # Create a list of commands and their signatures
        command_list = [self.get_command_signature(command) for cog, commands in mapping.items() for command in commands]

        # Split the command list into chunks for each page
        chunks = [command_list[i:i+commands_per_page] for i in range(0, len(command_list), commands_per_page)]

        # Create embed pages
        for chunk in chunks:
            embed = discord.Embed(title=f"Bot Commands (Page {current_page})", color=discord.Color.blue())
            embed.description = "\n".join(chunk)
            embed_pages.append(embed)
            current_page += 1

        # Send the first page
        message = await self.context.send(embed=embed_pages[0])

        # Add buttons for pagination if there are multiple pages
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




@bot.command(help="Creates a poll with a question and multiple options. Separate the question and options using '|' symbol. Example: !poll What is your favorite color? | Red | Blue | Green")
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
            embed.add_field(name=f"Option {i+1}", value=option, inline=False)

        # Send the poll and add reactions
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await message.add_reaction(chr(0x1f1e6 + i))  # Unicode regional indicator symbols A-Z
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
    print.info(f'{bot.user} is now running!')
    
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="Erika"))
    
    
    bot.loop.create_task(send_timed_message())
    verifyChannel = bot.get_channel(1234091236097396787)
    if verifyChannel:
        async for message in verifyChannel.history():
            # Delete the previous message if it was sent by the bot
            await message.delete()
                
        embed = discord.Embed(title = "Verification", description = "Click below to verify.")
        await verifyChannel.send(embed = embed, view = Verification())
    else:
        print.error("Could not send verification message for whatever reason.")
    
    with open('IMG_0935.JPEG', 'rb') as f:
        avatar_bytes = f.read()
        f.close()
    #await bot.user.edit(avatar=avatar_bytes)
    #await bot.user.edit(username="bot-Bernso")

    



@bot.command(help = "Starts up the leveling system if it hasnt already.")
async def init(ctx):
    if ctx.author.guild_permissions.administrator:
        cur.execute(f'''CREATE TABLE IF NOT EXISTS GUILD_{ctx.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')

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
                embed.add_field(name="Old XP", value=f"{remaining_exp_old}/{next_level_exp_old} (Level {old_level})", inline=False)
                embed.add_field(name="New XP", value=f"{remaining_exp_new}/{next_level_exp_new} (Level {new_level})", inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send("User not found in the database.")
        except sqlite3.OperationalError as e:
            await ctx.send("Database error occurred.")
            print.error("SQLite Error:", e)
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





@bot.command(help="Shows all the highest level people in the server.")
async def leaderboard(ctx):
    try:
        cur.execute(f"SELECT user_id, MAX(exp) FROM GUILD_{ctx.guild.id} GROUP BY user_id ORDER BY MAX(exp) DESC")
        results = cur.fetchall()

        if results:
            embed = discord.Embed(title="Leaderboard", color=discord.Color.blue())

            for index, (user_id, exp) in enumerate(results, start=1):
                user = ctx.guild.get_member(user_id)
                if user:
                    level = (exp // 50) + 1
                    remaining_exp = exp % 50  # Calculate remaining XP for the current level
                    embed.add_field(name=f"{index}. {user.display_name}", value=f"XP: {remaining_exp} | Level: {level}", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("No users found in the database.")
    except sqlite3.OperationalError:
        await ctx.send("Database not initialized")






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
        super().__init__(timeout = None)
    @discord.ui.button(label="Verify",custom_id = "Verify",style = discord.ButtonStyle.success)
    async def verify(self, interaction, button):
        verified = 1234090799571013712
        unverified = 1234090964549767212
        user = interaction.user
        if verified not in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(unverified))
            await user.add_roles(user.guild.get_role(verified))
            await user.send("You have been verified!")

@bot.command(help = "Creates the verify message people can use to verify.")
async def start_verify(ctx):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title = "Verification", description = "Click below to verify.")
        await ctx.send(embed = embed, view = Verification())
    else:
        await ctx.reply("You cannot use this command. Required = Administrator")

@bot.command(name='runfile', help = "Do not put .py after the file name as it will not work\nThe current working files are:\n- hello.py\n- fakehack.py\n- PassGen.py")
async def run_file(ctx, file_name: str):
    try:
        # Execute the Python file and capture its output
        result = subprocess.run(['python', f'{file_name}.py'], capture_output=True, text=True)
        output = result.stdout

        # Send the output as a message
        await ctx.send(f"Output:\n```{output}```")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='dm_runfile', help = "Do not put .py after the file name as it will not work\nThe current working files are:\n- hello.py\n- fakehack.py\n- PassGen.py")
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

@bot.command(help = "Say the command and the bot will dm you a message, no parameters are needed.")
async def dm_test(ctx):
    chars = "QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*()_+-={[]};:/?.><,|~`"
    user = ctx.author
    try:
        await user.send("Hello Monkey!")
        await user.send("https://tenor.com/view/monkey-freiza-dbs-dbz-gif-25933202")
        await ctx.reply("Messages sent to your dm's.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}\nThis error is most likely due to your dm's being private, please make them public.")
    
@bot.command(help = "The bot will randomly generate a password for you based on the length you requested.\n\nThe <special_chars> is boolean, it will be 'True' or 'False'.")
async def password_gen(ctx, length: int, special_chars: bool):
    user = ctx.author
    chars = "QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"
    if special_chars:
        chars += "!@#$%^&*()_+-={[]};:/?.><,|~`"
    userpass = ''.join(random.choice(chars) for _ in range(length))
    await user.send(f"Your password is:\n```{userpass}```")
    await ctx.reply("Your generated password has been sent to your dm's.")

@bot.command(help = "Shows the users ping.")
async def ping(ctx):

    await ctx.reply(f"Your ping is:   `{round(bot.latency*1000)} ms`")

@bot.command(help = "Deletes a specified role.")
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


@bot.command(help = "This is just a test command, it will create embed message that go from pages 1 through 6 with interactable buttons.")
async def page_test(ctx: commands.Context):
    embeds = [discord.Embed(title=f"Page {i}", description=f"Content for page {i}") for i in range(1, 6)]
    view = PaginationView(embeds)  # Pass the embeds as pages argument
    await view.start(ctx)



@bot.command(help = "Replies to your messag with a link to my linktree.")
async def linktree(ctx):
    await ctx.reply('Link to Linktree:\nhttps://linktr.ee/Bernso')

@bot.command(help = "Sends my GitHub page.")
async def github(ctx):
    await ctx.reply("Link to GitHub:\nhttps://github.com/Bernso")

@bot.command(help = "Gives you a random number from 1-666")
async def roll(ctx):
    await ctx.reply(f'You rolled: **{random.randint(1, 666)}**')

@bot.command(help = 'Replies to your message')
async def hello(ctx):
    await ctx.reply('What do you want?')

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
        chunks = [message_records[i:i+chunk_size] for i in range(0, len(message_records), chunk_size)]

        # Send each chunk as a separate embed
        for i, chunk in enumerate(chunks, start=1):
            # Create an embed object for the chunk
            embed = discord.Embed(title=f"Message History (Chunk {i})", color=discord.Color.blue())

            # Add message history to the embed
            for record in chunk:
                message_content = record.get('message_content', 'Unknown')
                username = record.get('username', 'Unknown')
                server_name = record.get('server_name', 'Unknown')
                embed.add_field(name="Message", value=f"**{username}** ({server_name}): {message_content}", inline=False)

            # Send the embed message
            await ctx.send(embed=embed)

        # Reply to the user to inform them that all message history has been sent
        await ctx.reply("All message history has been uploaded :thumbsup:")

@bot.command(help = "Vishwa's favourite things.")
async def vishwa_bestpicks(ctx):
    embed = discord.Embed(title="Vishwa's favourite's", color=discord.Color.dark_gold())
    embed.add_field(name = "Anime", value = "Haikyuu", inline=False)
    embed.add_field(name = "Manga", value = "Blue Box", inline=False)
    embed.add_field(name = "Song", value = "Social Path - Stray Kids", inline=False)
    embed.add_field(name = "Kdrama (Korean drama)", value = "The Glory", inline=False)

    # Send the embedded message
    await ctx.send(embed=embed)

@bot.command(help = "Will reply with a quote depending on how sent the command")
async def quote(ctx):
    author = str(ctx.author)
    if author == "vboss890":
        await ctx.reply('"An apple a day keeps anyone away if you throw it hard enough!"')
    elif author == "kefayt_":
        await ctx.reply('"Wake up with a stinky finger."')
    elif author == ".bernso":
        await ctx.reply("TBATE > World After The Fall")
    elif author == "2314937462561":
        await ctx.reply("Your gay.")
    elif author == "ceo_of_india425":
        await ctx.reply("Bro does not own india :pray:")
    else:
        await ctx.reply("Dm '.bernso' or the owner of the server to get your own quote.")
        
    

@bot.command(help = "State wheather you are black or white and the bot will put you in a race.")
async def race(ctx, option=None):
    if option.lower() == "white":
        await ctx.send("You'd lose the race")
    elif option.lower() == 'black':
        await ctx.send("You'd win the race")
    elif option == None:
        await ctx.send("Invalid option, available options: `black`, `white`")
    else:
        await ctx.send("Invalid option, available options: `black`, `white`")



@bot.command(name = "pass_gcse's", help = "Guesses the chance of you passing your GCSE's")
async def pass_gcse(ctx):
    if ctx.author.id == 550262161998479380:
        await ctx.reply('You stupid monkey you dont have a chance of passing') 
    elif ctx.author.id == 581916234057252865: 
        await ctx.reply('jew') 
    else: 
        await ctx.reply(f"You have a **{random.randint(0,100)}%** chance to pass your GCSEs")

@bot.command(help = 'Tells you the amount of friends you have (unless your a special)')
async def friends(ctx):
    if ctx.author.id == 712946563508469832: 
        await ctx.reply('Bro is god') 
    elif ctx.author.id == 581916234057252865: 
        await ctx.reply('Nuh uh') 
    elif ctx.author.id == 550262161998479380: 
        await ctx.reply('Bros only friends are the monkeys.') 
    else:
        await ctx.reply(f'You have **{random.randint(0, 15)}** friends.')

@bot.command(help = 'NUH UH')
async def kys(ctx):
    await ctx.reply('https://tenor.com/view/yuta-jjk-jujutsu-kaisen-i-will-kill-myself-okkotsu-gif-1986392651623942939')

@bot.command(help = 'Replies to your message (in a very kind way)')
async def bye(ctx):
    await ctx.reply('Never come back! :wave:')

@bot.command(help = 'Replies to your message', name = 'NUH-UH')
async def nuh_uh(ctx):
    await ctx.reply('YUH-UH')

@bot.command(help = 'Replies to your message', name='YUH-UH')
async def yuh_uh(ctx):
    await ctx.reply('NUH-UH')

@bot.command(help = 'Enter an equation and the bot will comlete it for you (this cannot contain any algebra)')
async def calc(ctx, *, equation: str):
    try:
        result = eval(equation)
        await ctx.reply(f"The result of the calculation is: **{result}**")
    except Exception as e:
        await ctx.reply(f"Invalid equation or operation. Error: {str(e)}")

@bot.command(help = "Replies to your message with the state of my internet")
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

@bot.command(help = "Add two or more numbers.")
async def add(ctx, *numbers: int):
    if len(numbers) >= 2:
        total = sum(numbers)
        await ctx.reply(f"The sum of the numbers is: **{total}**")
    else:
        await ctx.reply("Please provide at least two numbers after the '!add' command.")

# Define the !stop_big_text command
@bot.command(help="Stop making your text big.")
async def stop_big_text(ctx):
    await ctx.reply("Stop making your text big you moron")

# Define the !best command
@bot.command(help="Assert superiority.")
async def best(ctx):
    member = ctx.guild.get_member(712946563508469832)
    await ctx.reply(f"{member.mention} is DA GOAT")

# Define the !website command
@bot.command(help="Link to Bernso's website. \nITS A WIP OK?")
async def website(ctx):
    await ctx.reply("My website:\nhttps://bernso.locum.dunz.net")

# Define the !monkeys command
@bot.command(help="Description of monkeys.")
async def monkeys(ctx):
    await ctx.reply("Like water melon and chicken")

@bot.command(help = "Sends you @.berso's youtube channel.")
async def ytchannel(ctx):
    await ctx.reply("YouTube:\nhttps://www.youtube.com/@bernso2547")

# Define the !formula1 command
@bot.command(help="The only right opinion on Formula 1.")
async def formula1(ctx):
    await ctx.reply("Estaban Occon DA GOAT! (I hate lewis now, that money hungry freak)")

# Define the !spotify command
@bot.command(help="Link to Bernso's Spotify playlist.")
async def spotify(ctx):
    await ctx.reply("My spotify playlist:\nhttps://open.spotify.com/playlist/6Mg5z7FrNYZ4DBVZvnjsP1?si=905dd469d16748e0")

@bot.command(help = "Uhhh, you figure it out")
async def kys_japan(ctx):
    await ctx.reply("自殺する")

# Define the !manga command
@bot.command(help="Favorite manga.")
async def manga(ctx):
    await ctx.reply("Juujika No Rokin :on: :top:")

@bot.command(help = "Bot will make a guess on when you'll die")
async def die_when(ctx):
    time = ['days', 'years', 'months', 'seconds', 'minutes']
    await ctx.reply(f"You will die in {random.randint(1,100)} {random.choice(time)}")

@bot.command(help = "What is there to say? It is the best series ever.")
async def best_series(ctx):
    await ctx.reply("The Fate series :fire:")

@bot.command(help = "Bans the user inputed.")
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

@bot.command(help = "Kicks the user inputed from the current server.")
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
    member.add_roles(discord.utils.get(member.guild.roles, name="Unverified"))
    if log_channel:
        # Create an embedded message for member join event
        embed = discord.Embed(title="Member Joined", description=f"{member.mention} has joined the server! \nWelcome!", color=discord.Color.green())
        await log_channel.send(embed=embed)
        await general_chat.send(embed=embed)
    else:
        general_chat.send(f"Cannot find {log_channel}")

# Event for when a member leaves the server
@bot.event
async def on_member_remove(member):
    # Get the log channel
    log_channel = bot.get_channel(BOT_LOG_CHANNEL_ID)
    if log_channel:
        # Create an embedded message for member leave event
        embed = discord.Embed(title="Member Left", description=f"{member.mention} has left the server.", color=discord.Color.red())
        await log_channel.send(embed=embed)

@bot.command(help="Checks your ethnicity.")
async def ethnicity(ctx):
    # List of ethnicities
    ethnicities = ['Black', 'White', 'Monkey', 'African', 'Chinese', 'Japanese', 'Kung-fu Panda', 'Nazi', 'Polar Bear', 'Polish', 'Jew']
    
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
    await ctx.reply("World After The Fall :on: :top:, any other opinion is invalid")

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
        await ctx.reply('YOU FINALLY JOINED')
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
        await member.remove_roles(muted_role)

        # reply a message confirming the mute
        await ctx.reply(f"{member.mention} has been unmuted")
    else:
        # If the user doesn't have the necessary permissions, reply an error message
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

    rude_words = ["n1gger", "rape", "niigger", "0thisrodormyrod0", "knee grow", 
    "fuck", "shit", "bitch", "cunt", "ass", "faggot", "fag", 
    "faggots", "faggot", "nigger", "nigga", "niggers", "niggas", 
    "piss", "penis", "penises", "penis", "dick", "nega", "negro", 
    "negros", "negas", "niga", "cum", "semen", "ejaculate", "f.u.c.k.i.n.g", 
    "f.u.c.k", "f.u.c", "f.u", "fu", "fck", "fcking", "fckn", 
    "fckyou", "fckr", "fckoff", "fckface", "fckd", "fcked", 
    "fcku", "fckers", "fckr", "fcky", "fckn", "fcku", "b1tch", 
    "b1tches", "b1tch", "b1tch3s", "bitch", "bitches", "bitch3s", 
    "b!tch", "b!tches", "b!tch3s", "biatch", "biatches", "biatch3s", 
    "b!atch", "b!atches", "b!atch3s", "b1tch", "b1tches", "b1tch3s", 
    "bitck", "bitckes", "bitck3s", "b!tck", "b!tckes", "b!tck3s", 
    "b1tck", "b1tckes", "b1tck3s", "bitck", "bitckes", "bitck3s", 
    "d!ck", "d!cks", "d!ckhead", "d!ckheads", "dick", "dicks", 
    "dickhead", "dickheads", "d!ck", "d!cks", "d!ckhead", "d!ckheads", 
    "d1ck", "d1cks", "d1ckhead", "d1ckheads", "diick", "diicks", 
    "diickhead", "diickheads", "di1ck", "di1cks", "di1ckhead", "di1ckheads", 
    "di1ckhead", "di1ckheads", "f4ggot", "f4ggots", "f4g", "f4gs", 
    "faggot", "faggots", "fag", "fags", "f4ggot", "f4ggots", 
    "f4g", "f4gs", "fag", "fags", "f4ggot", "f4ggots", "f4g", 
    "f4gs", "fag", "fags", "n1gga", "n1ggas", "n1gger", "n1ggers", 
    "nigga", "niggas", "nigger", "niggers", "n1gga", "n1ggas", "azz", "azzhole", "b!+ch", "b!tch3s", "b!tch3z", "b!tch3z", "b!tchez", "b!tchz", 
    "b!tchz", "b00bz", "b00bs", "b00bz", "b1+ch", "b1tch", "b1tch3s", "b1tch3z", 
    "b1tch3z", "b1tchez", "b1tchz", "b1tchz", "b1tch3s", "b1tch3z", "b1tch3z", 
    "b1tchez", "b1tchz", "b1tchz", "b1tch3s", "b1tch3z", "b1tch3z", "b1tchez", 
    "b1tchz", "b1tchz", "b1tch3s", "b1tch3z", "b1tch3z", "b1tchez", "b1tchz", 
    "b1tchz", "b1tch3s", "b1tch3z", "b1tch3z", "b1tchez", "b1tchz", "b1tchz", 
    "b1tch3s", "b1tch3z", "b1tch3z", "b1tchez", "b1tchz", "b1tchz", "bi+ch", 
    "bi+ches", "bi+chez", "bi+tch", "bi+tches", "bi+tchez", "bi+ch", "bi+ches", 
    "bi+chez", "bi+tch", "bi+tches", "bi+tchez", "biach", "biachez", "biachez", 
    "biatch", "biatches", "biatchez", "biatchez", "biatch", "biatches", "biatchez", 
    "biatchez", "biatch", "biatches", "biatchez", "biatchez", "big tits", "bigtits", 
    "bigtits", "biotch", "biotches", "biotches", "bi+ch", "bi+ches", "bi+chez", 
    "bi+tch", "bi+tches", "bi+tchez", "bi+ch", "bi+ches", "bi+chez", "bi+tch", 
    "bi+tches", "bi+tchez", "bit+hes", "bit+chez", "bit+ches", "bitc", "bitchez", 
    "bitchez", "bitche", "bitches", "bitches", "bitchi", "bitchy", "bitchy", "blow job", 
    "blowjob", "blowjobs", "blowjobs", "boiolas", "boiolas", "boob", "boobs", "boobs", 
    "booby", "booby", "boody", "boody", "booger", "booger", "boooty", "booty", "booty", 
    "booobs", "booobs", "boooty", "boooty", "boooobs", "boooobs", "booooobs", "booooobs", 
    "booooooobs", "booooooobs", "boooooooobs", "boooooooobs", "booooooooobs", "booooooooobs", 
    "boooooooool", "boooooooool", "booooooooool", "booooooooool", "boooooooooool", "boooooooooool", 
    "booooooooooooobs", "booooooooooooobs", "b00bs", "bootee", "bootee", "bootee", "bootee", 
    "bootie", "bootie", "bootie", "bootie", "booty", "booty", "booty", "booty", "booty", 
    "booty", "booty call", "booty call", "booty call", "booty call", "breasts", "breasts", 
    "breasts", "breasts", "bunny fucker", "bunny fucker", "bunny fucker", "bunny fucker", 
    "bunnyfucker", "bunnyfucker", "bunnyfucker", "bunnyfucker", "butt", "butt", "butt fuck", 
    "butt fuck", "butt fuck", "butt fuck", "buttfuck", "buttfuck", "buttfuck", "buttfuck", 
    "butthead", "butthead", "butthead", "butthead", "butthole", "butthole", "butthole", 
    "butthole surf", "butthole surf", "butthole surf", "butthole surf", "butthurts", 
    "butthurts", "butthurts", "butthurts", "buttmuch", "buttmuch", "buttmuch", "buttmuch", 
    "buttplug", "buttplug", "buttplug", "buttplug", "c-0-c-k", "c-0-c-k", "c-0-c-k", 
    "c-0-c-k", "c0ck", "c0ck", "c0ck", "c0ck", "c0cksucker", "c0cksucker", "c0cksucker", 
    "c0cksucker", "carpet muncher", "carpet muncher", "carpet muncher", "carpet muncher", 
    "cawk", "cawk", "cawk", "cawk", "cawks", "cawks", "cawks", "cawks", "chink", "chink", 
    "chink", "chink", "cipa", "cipa", "cipa", "cipa", "cl1t", "cl1t", "cl1t", "cl1t", "climax", 
    "climax", "climax", "climax", "clit", "clit", "clit", "clit", "clit licker", "clit licker", 
    "clit licker", "clit licker", "clitoris", "clitoris", "clitoris", "clitoris", "clitorus", 
    "clitorus", "clitorus", "clitorus", "clits", "clits", "clits", "clits", "clitty", "clitty", 
    "clitty litter", "clitty litter", "clitty litter", "clitty litter", "clitty litter", 
    "clitty litter", "cocain", "cocain", "cocain", "cocain", "cocaine", "cocaine", "cocaine", 
    "cocaine","cocaine", "coccydynia", "coccydynia", "cock", "cock", "cock block", "cock block", "cock block", 
    "cock block", "cock face", "cock face", "cock face", "cock face", "cock head", "cock head", 
    "cock head", "cock head", "cock master", "cock master", "cock master", "cock master", 
    "cock sucker", "cock sucker", "cock sucker", "cock sucker", "cock-sucker", "cock-sucker", 
    "cock-sucker", "cock-sucker", "cockbite", "cockbite", "cockbite", "cockbite", "cockblock", 
    "cockblock", "cockblock", "cockblock", "cockface", "cockface", "cockface", "cockface", 
    "cockfucker", "cockfucker", "cockfucker", "cockfucker", "cockhead", "cockhead", "cockhead", 
    "cockhead", "cockhead", "cockhead", "cockmaster", "cockmaster", "cockmaster", "cockmaster", 
    "cockmongler", "cockmongler", "cockmongler", "cockmongler", "cockmunch", "cockmunch", 
    "cockmunch", "cockmunch", "cockmuncher", "cockmuncher", "cockmuncher", "cockmuncher", 
    "cocknob", "cocknob", "cocknob", "cocknob", "cocknose", "cocknose", "cocknose", "cocknose", 
    "cocknugget", "cocknugget", "cocknugget", "cocknugget", "cockshit", "cockshit", "cockshit", 
    "cockshit", "cocksucker", "cocksucker", "cocksucker", "cocksucker", "cockwaffle", "cockwaffle", 
    "cockwaffle", "cockwaffle", "coochie", "coochie", "coochy", "coochy", "cooky", "cooky", 
    "cooky", "cooky", "cooly", "cooly", "cooly", "cooly", "cornhole", "cornhole", "cornhole", 
    "cornhole", "crap", "crap", "crap", "crap", "crappy", "crappy", "crappy", "crappy", "cum", 
    "cum", "cum chugger", "cum chugger", "cum chugger", "cum chugger", "cum dumpster", 
    "cum dumpster", "cum dumpster", "cum dumpster", "cum guzzler", "cum guzzler", "cum guzzler", 
    "cum guzzler", "cumdump", "cumdump", "cumdump", "cumdump", "cumdumpster", "cumdumpster", 
    "cumdumpster", "cumdumpster", "cumguzzler", "cumguzzler", "cumguzzler", "cumguzzler", 
    "cummer", "cummer", "cummer", "cummer", "cumshot", "cumshot", "cumshot", "cumshot", 
    "cunilingus", "cunilingus", "cunilingus", "cunilingus", "cunillingus", "cunillingus", 
    "cunillingus", "cunillingus", "cunnilingus", "cunnilingus", "cunnilingus", "cunnilingus", 
    "cunt", "cunt", "cunt", "cunt", "cuntbag", "cuntbag", "cuntbag", "cuntbag", "cuntlick", 
    "cuntlick", "cuntlick", "cuntlick", "cuntlicker", "cuntlicker", "cuntlicker", "cuntlicker", 
    "cuntlicking", "cuntlicking", "cuntlicking", "cuntlicking", "cuntrag", "cuntrag", "cuntrag", 
    "cuntrag", "cuntslut", "cuntslut", "cuntslut", "cuntslut", "cyalis", "cyalis", "cyalis", 
    "cyalis", "cyberfuc", "cyberfuc", "cyberfuc", "cyberfuc", "cyberfuck", "cyberfuck", 
    "cyberfuck", "cyberfuck", "cyberfuck", "cyberfuck", "cyberfucked", "cyberfucked", 
    "cyberfucked", "cyberfucked", "cyberfucker", "cyberfucker", "cyberfucker", "cyberfucker", 
    "cyberfuckers", "cyberfuckers", "cyberfuckers", "cyberfuckers", "cyberfucking", 
    "cyberfucking", "cyberfucking", "cyberfucking", "d0ng", "d0ng", "d0ng", "d0ng", "d0uch3", 
    "d0uch3", "d0uch3", "d0uch3", "d0uche", "d0uche", "d0uche", "d0uche", "d1ck", "d1ck", "d1ck", 
    "d1ck", "d1ld0", "d1ld0", "d1ld0", "d1ldo", "d1ldo", "d1ldo", "d1ldo", "dago", "dago", "dago", 
    "dago", "dag0", "dag0", "dag0", "dag0", "dammit", "dammit", "dammit", "dammit", "damn", "damn", 
    "damn", "damn", "damnation", "damnation", "damnation", "damnation", "damnit", "damnit", "damnit", 
    "damnit", "dawgie-style", "dawgie-style", "dawgie-style", "dawgie-style", "d!ck", "d!ck", "d!ck", 
    "d!ck", "d1ck", "d1ck", "d1ck", "d1ck", "defecate", "defecate", "defecate", "defecate", "dick", 
    "dick", "dickbag", "dickbag", "dickbeaters", "dickbeaters", "dickbrain", "dickbrain", "dickdipper", 
    "dickdipper", "dickface", "dickface", "dickflipper", "dickflipper", "dickfuck", "dickfuck", 
    "dickfucker", "dickfucker", "dickhead", "dickhead", "dickhole", "dickhole", "dickish", "dickish", 
    "dickish", "dickjuice","dickead", "dickless", "dickless", "dicklick", "dicklick", "dicklicker", "dicklicker", 
    "dickman", "dickman", "dickmilk", "dickmilk", "dickripper", "dickripper", "dicksipper", 
    "dicksipper", "dickslap", "dickslap", "dick-sneeze", "dick-sneeze", "dicksucker", 
    "dicksucker", "dicksucking", "dicksucking", "dicktickler", "dicktickler", "dickwad", 
    "dickwad", "dickweasel", "dickweasel", "dickweed", "dickweed", "dickwhipper", "dickwhipper", 
    "dickwod", "dickwod", "dickzipper", "dickzipper", "diddle", "diddle", "dike", "dike", "dike", 
    "dike", "dildo", "dildo", "dingle", "dingle", "dingleberry", "dingleberry", "dink", "dink", 
    "dink", "dink", "dinks", "dinks", "dinks", "dinks", "dipship", "dipship", "dipshit", "dipshit", 
    "dipstick", "dipstick", "dirsa", "dirsa", "dirty", "dirty", "dirty", "dirty", "dirty sanchez", 
    "dirty sanchez", "dirty sanchez", "dirty sanchez", "dive", "dive", "dive", "dive", "dix", "dix", 
    "dix", "dix", "dog style", "dog style", "dog style", "dog style", "dog-fucker", "dog-fucker", 
    "dog-fucker", "dog-fucker", "doggie style", "doggie style", "doggie style", "doggie style", 
    "doggiestyle", "doggiestyle", "doggiestyle", "doggiestyle", "doggin", "doggin", "doggin", "doggin", 
    "dogging", "dogging", "dogging", "dogging", "doggy style", "doggy style", "doggy style", "doggy style", 
    "doggystyle", "doggystyle", "doggystyle", "doggystyle", "dolcett", "dolcett", "dolcett", "dolcett", 
    "dominatrix", "dominatrix", "dominatrix", "dominatrix", "dommes", "dommes", "dommes", "dommes", 
    "donkey punch", "donkey punch", "donkey punch", "donkey punch", "doochbag", "doochbag", "doochbag", 
    "doochbag", "dookie", "dookie", "dookie", "dookie", "doosh", "doosh", "doosh", "doosh", "douche", 
    "douche", "douchebag", "douchebag", "douchebags", "douchebags", "douche-fag", "douche-fag", 
    "douche-fag", "douche-fag", "douchewaffle", "douchewaffle", "douchewaffle", "douchewaffle", 
    "douchey", "douchey", "douchey", "douchey", "dp action", "dp action", "dp action", "dp action", 
    "drunk", "drunk", "drunk", "drunk", "dry hump", "dry hump", "dry hump", "dry hump", "duche", 
    "duche", "duche", "duche", "dumass", "dumass", "dumass", "dumass", "dumb ass", "dumb ass", 
    "dumb ass", "dumb ass", "dumbass", "dumbass", "dumbass", "dumbass", "dumbasses", "dumbasses", 
    "dumbasses", "dumbasses", "dumbfuck", "dumbfuck", "dumbfuck", "dumbfuck", "dumbshit", "dumbshit", 
    "dumbshit", "dumbshit", "dummy", "dummy", "dummy", "dummy", "dumshit", "dumshit", "dumshit", 
    "dumshit", "dyke", "dyke", "dyke", "dyke", "dykes", "dykes", "dykes", "dykes", "eat a dick", 
    "eat a dick", "eat a dick", "eat a dick", "eat hair pie", "eat hair pie", "eat hair pie", 
    "eat hair pie", "eat my ass", "eat my ass", "eat my ass", "eat my ass", "eat my", "eat my", 
    "eat my", "eat my", "ecstacy", "ecstacy", "ecstacy", "ecstacy", "ejaculate", "ejaculate", 
    "ejaculate", "ejaculate", "ejaculated", "ejaculated", "ejaculated", "ejaculated", "ejaculating", 
    "ejaculating", "ejaculating", "ejaculating", "ejaculation", "ejaculation", "ejaculation", 
    "ejaculation", "ejakulate", "ejakulate", "ejakulate", "ejakulate", "erect", "erect", "erect", 
    "erect", "erection", "erection", "erection", "erection", "erotic", "erotic", "erotic", "erotic", 
    "erotism", "erotism", "erotism", "erotism", "escort", "escort", "escort", "escort", "essohbee", 
    "essohbee", "essohbee", "essohbee", "eunuch", "eunuch", "eunuch", "eunuch", "extacy", "extacy", 
    "extacy", "extacy", "extasy", "extasy", "extasy", "extasy", "f u c k", "f u c k", "f u c k", 
    "f u c k", "f u c k", "f u c k", "f u c k", "f u c k", "f u c k", "f u c k", "f u c k", "f u c k", 
    "f u c k", "f u c k", "f u c k", "f u c k", "f u c k", "f u c k",
    "n1gger", "n1ggers", "nigga", "niggas", "nigger", "niggers", 
    "n1gga", "n1ggas", "n1gger", "n1ggers", "nigga", "niggas", 
    "nigger", "niggers", "n1gga", "n1ggas", "n1gger", "n1ggers", 
    "nigga", "niggas", "nigger", "niggers", "n1gga", "n1ggas", 
    "n1gger", "n1ggers", "nigga", "niggas", "nigger", "niggers", 
    "n1gga", "n1ggas", "n1gger", "n1ggers", "nigga", "niggas", 
    "nigger", "niggers", "n1gga", "n1ggas", "n1gger", "n1ggers", 
    "nigga", "niggas", "nigger", "niggers", "n1gga", "n1ggas", 
    "n1gger", "n1ggers", "nigga", "niggas", "nigger", "niggers", 
    "n1gga", "n1ggas", "n1gger", "n1ggers", "nigga", "niggas", 
    "nigger", "niggers", "n1gga", "n1ggas", "n1gger", "n1ggers", 
    "nigga", "niggas", "nigger", "niggers", "n1gga", "n1ggas", 
    "n1gger", "n1ggers", "nigga", "niggas", "nigger", "niggers", 
    "n1gga", "n1ggas", "n1gger", "n1ggers", "nigga", "niggas", 
    "nigger", "niggers", "n1gga", "n1ggas", "n1gger", "n1ggers", 
    "nigga", "niggas", "nigger", "niggers", "n1gga", "n1ggas", 
    "n1gger", "n1ggers", "nigga", "niggas", "nigger", "niggers", 
    "n1gga", "n1ggas", "n1gger", "n1ggers", "nigga", "niggas", 
    "nigger", "niggers", "n1gga", "n1ggas", "n1gger", "n1ggers", 
    "nigga", "niggas", "nigger", "niggers", "n1gga", "n1ggas", 
    "n1gger", "n1ggers", "nigga", "niggas", "nigger", "niggers", 
    "n1gga", "n1ggas", "n1gger", "n1ggers", "nigga", "niggas", "🇳", "🇺", "🇬", "🇦", "🇫", "🅰️"
    "nigger", "niggers", "n1gga", "n1ggas", "n1gger", "n1ggers", "rape", "niigger", "0ThisRodOrMyRod0", "knee grow", "0ThisRodOrMyRod0", "fuck", "shit", "bitch", "cunt", "ass", "faggot", "fag", "faggots", "faggot", "nigger", "nigga", "niggers", "niggas", "piss", "penis", "penises", "penis", "dick", "nega", "negro", "negros", "negas", "niga", "cum", "semen", "ejaculate", "F.U.C.K.I.N.G"]


    # Check if the message contains any rude words
    content = message.content.lower()
    for word in rude_words:
        if word in content:
            # If a rude word is found, delete the message and warn the user
            await message.delete()
            await message.channel.send(f"{message.author.mention}, please refrain from using rude language.")
            break  # Stop checking

    # Save the updated records to a pickle file
    with open(RECORDS_FILENAME, 'wb') as file:
        pickle.dump(message_records, file)

    print.info(f'\nChannel([{message_record["channel"]}]) \nUser id({message_record["user_id"]}) \nUsername({message_record["username"]}) \nMessage({message_record["message_content"]})\nServer name({message_record["server_name"]})\n')

    contentyes = message.content.lower()
    for word in rude_words:
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
            print.warning("Invalid channel ID")

    if message.author == bot.user:
        return
    else:
        try:
            if message.channel != 'Direct Message with Unknown User':
                cur.execute(f"SELECT * FROM GUILD_{message.guild.id} WHERE user_id={message.author.id}")
                result = cur.fetchone()

                if result is not None and result[1] == 99:
                    await message.channel.send(f"{message.author.mention} advanced to lvl {result[2] + 1}")
                    cur.execute(f"UPDATE GUILD_{message.guild.id} SET exp=0, lvl={result[2] + 1} WHERE user_id={message.author.id}")
                    con.commit()
                else:
                    cur.execute(f"UPDATE GUILD_{message.guild.id} SET exp={result[1] + 1} WHERE user_id={message.author.id}")
                    con.commit()

        except sqlite3.OperationalError:
            pass
    

@bot.command(name = "console-embed", help="You'll be able to send messages through the console if you have the appropriate permissions")
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
            print.warning("Invalid insufficient permissions")




    

@bot.command(help="Removes roles to a selected user.")
async def remove_role(ctx, member: discord.Member, *roles):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.administrator:
        # Iterate over each role provided
        for role_name in roles:
            # Check if the role name is 'all'
            if role_name.lower() == 'all':
                # If 'all' is specified, add all roles to the member
                for role in ctx.guild.roles:
                    if role != 1234086390073917453:
                        if role != ctx.guild.default_role:  # Avoid adding the @everyone role
                            await member.remove_roles(role)
                await ctx.send(f"All available roles have been removed from {member.mention}")
            else:
                # Check if the role exists in the server
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role:
                    await member.remove_roles(role)
                    await ctx.send(f"Removed role '{role_name}' from {member.mention}")
                else:
                    await ctx.send(f"Role '{role_name}' does not exist.")
    else:
        # If the user doesn't have the necessary permissions, reply with an error message
        await ctx.reply("You don't have permission to use this command.")

@bot.command(name = 'NEIN', help = "NEIN")
async def nein(ctx):
    await ctx.reply("9")

@bot.command(name = "..", help = "Why are you speechless?")
async def speechless(ctx):
    await ctx.reply("Why are you speechless?")

@bot.command(name = ".", help = "Why are you speechless?")
async def speechless(ctx):
    await ctx.reply("Why are you speechless?")

@bot.command(name = "...", help = "Why are you speechless?")
async def speechless(ctx):
    await ctx.reply("Why are you speechless?")




@bot.command(name = "console-msg", help="You'll be able to send messages through the console if you have the appropriate permissions")
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
            print.warning("Invalid role ID or insufficient permissions")




@bot.command(help="Add roles to a selected user.")
async def add_role(ctx, member: discord.Member, *roles):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.manage_roles:
        # Iterate over each role provided
        for role_name in roles:
            # Check if the role name is 'all'
            if role_name.lower() == 'all':
                # If 'all' is specified, add all roles to the member
                for role in ctx.guild.roles:
                    if role != ctx.guild.default_role: # Avoid adding the @everyone role
                        if role != 1234086390073917453: 
                            await member.add_roles(role)
                await ctx.send(f"All available roles have been added to {member.mention}")
            else:
                # Check if the role exists in the server
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role:
                    if role in member.roles:
                        # If the member already has the role, remove it
                        await member.remove_roles(role)
                        await ctx.send(f"Removed role '{role_name}' from {member.mention}")
                    else:
                        # If the member doesn't have the role, add it
                        await member.add_roles(role)
                        await ctx.send(f"Added role '{role_name}' to {member.mention}")
                else:
                    await ctx.send(f"Role '{role_name}' does not exist.")
    else:
        # If the user doesn't have the necessary permissions, reply with an error message
        await ctx.reply("You don't have permission to use this command.")


@bot.command(help="Set the channel for role change logs.")
async def set_role_log_channel(ctx, channel: discord.TextChannel):
    # Check if the user invoking the command has the necessary permissions
    if ctx.author.guild_permissions.administrator:
        # Save the channel ID to a database or file
        # Replace this part with your preferred method of storing data
        channel_id = channel.id
        # In this example, we're simply printing the channel ID
        print.success(f"Role log channel set to: {channel_id}")
        await ctx.send(f"Role log channel has been set to {channel.mention}")
    else:
        await ctx.send("You don't have permission to use this command.")




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
                    embed.add_field(name="Role Added", value=f"{moderator.mention} added role {role.mention} to {after.mention}", inline=False)
            if removed_roles:
                for role in removed_roles:
                    embed = discord.Embed(title="Role Changes", color=discord.Color.red())
                    embed.add_field(name="Role Removed", value=f"{moderator.mention} removed role {role.mention} from {after.mention}", inline=False)
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


@bot.command(name='change_name', help='Change the nickname of the user\n\nTHE USER MUST BE:\n- user ID\nOR\n- user name')
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

@bot.command(help="Delete a specified number of messages in the channel. \nAlways add 1 to the count when using this command as your message counts as a message for the bot to delete.\nThis can only delete up to 100 messages (sadly)")
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
        await progress_message.edit(content=f"Deleted {len(messages_to_delete)} out of {amount} messages. Command ran by: {ctx.author.mention}")
    else:
        # If the user doesn't have the necessary permissions, reply with an error message
        await ctx.reply("You don't have permission to use this command.")

@bot.command(help = "Makes you depressed")
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
    else:
        # Log the error to console
        print.warning('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



@bot.command(name = "search", help="Search for available commands.")
async def search_command(ctx, command_name: str):
    command_names = [cmd.name for cmd in bot.commands]
    if command_name in command_names:
        command = bot.get_command(command_name)
        if command:
            command_help = command.help if command.help else "No help information available."
            embed = discord.Embed(title=f"Command: {command_name}", description=f"**Help:**\n{command_help}", color=discord.Color.blue())
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"The command **{command_name}** is available.")
    else:
        await ctx.reply(f"The command **{command_name}** is not available.")




bot.run(TOKEN)