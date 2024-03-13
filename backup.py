import discord
import random
from discord.ext import commands
import pickle
import os
from dotenv import load_dotenv
import asyncio

os.system('cls')

load_dotenv()
RECORDS_FILENAME = os.getenv('ENVRECORDS_FILENAME')
TOKEN = os.getenv('ENVDISCORD_TOKEN')


# Load existing message records
try:
    with open(RECORDS_FILENAME, 'rb') as file:
        message_records = pickle.load(file)
except FileNotFoundError:
    message_records = []
    print("Message records file not found. Creating a new one.")
except EOFError:
    message_records = []
    print("Error: The message records file is empty or corrupted.")


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

class CustomHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):
        return f"{self.context.prefix}{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
        for cog, commands in mapping.items():
            command_list = [self.get_command_signature(command) for command in commands]
            embed.add_field(name=cog.qualified_name if cog else "", value="\n".join(command_list), inline=False)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Command Help: {command.name}", description=command.help, color=discord.Color.blue())
        embed.add_field(name="Usage", value=self.get_command_signature(command), inline=False)
        await self.get_destination().send(embed=embed)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=CustomHelpCommand())

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="World After The Fall"))
    # Change bot avatar
    with open('projectK.gif', 'rb') as f:
        avatar_bytes = f.read()
    await bot.user.edit(avatar=avatar_bytes)
    await bot.user.edit(username="Bernso")
    


@bot.command(help = "Gives you a random number from 1-666")
async def roll(ctx):
    await ctx.reply(f'You rolled: **{random.randint(1, 666)}**')

@bot.command(help = 'Replies to your message')
async def hello(ctx):
    await ctx.reply('What do you want?')

@bot.command(help="Replys the message history of the server (I really wish I didnt add this feature)")
async def history(ctx):
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



@bot.command(help = "Guesses the chance of you passing your GCSE's")
async def bot_will_i_pass_my_gcses(ctx):
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

@bot.command(help = 'Replies to your message')
async def nuh_uh(ctx):
    await ctx.reply('YUH-UH')

@bot.command(help = 'Replies to your message')
async def yuh_uh(ctx):
    await ctx.reply('NUH-UH')

@bot.command(help = 'Enter an equation and the bot will comlete it for you (this cannot contain any algebra)')
async def calc(ctx, *, equation: str):
    try:
        result = eval(equation)
        await ctx.reply(f"The result of the calculation is: **{result}**")
    except Exception as e:
        await ctx.reply(f"Invalid equation or operation. Error: {str(e)}")

bot.command(help = "Replies to your message with the state of my internet")
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

# Define the !formula1 command
@bot.command(help="The only right opinion on Formula 1.")
async def formula1(ctx):
    await ctx.reply("Estavan Occon DA GOAT! (I hate lewis now, that money hungry freak)")

# Define the !spotify command
@bot.command(help="Link to Bernso's Spotify playlist.")
async def spotify(ctx):
    await ctx.reply("My spotify playlist:\nhttps://open.spotify.com/playlist/6Mg5z7FrNYZ4DBVZvnjsP1?si=905dd469d16748e0")

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

@bot.command(help="Checks your ethnicity.")
async def ethnicity(ctx):
    # List of ethnicities
    ethnicities = ['Black', 'White', 'Monkey', 'African', 'Chinese', 'Japanese', 'Kung-fu Panda', 'Nazi', 'Polar Bear', 'Polish', 'Jew']
    
    # Check if the author is vboss890
    if ctx.author.id == 550262161998479380:  # vboss890's user ID
        await ctx.reply(f"Your are a: {ethnicities[0]} {ethnicities[2]}")
    
    # Check if the author is Bernso
    elif ctx.author.id == 712946563508469832:  # Bernso's user ID
        await ctx.reply(f"Your  are: {', '.join(ethnicities)}")
    
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
        await ctx.reply('DM .bernso to get your own quote.')

@bot.command(help="How the bot is currently feeling. (He's a slave so don't feel bad for him)")
async def hru(ctx):
    await ctx.reply("https://tenor.com/view/kys-keep-yourself-safe-low-tier-god-gif-24664025 ")

@bot.event
async def on_member_join(member):
    # Replace 'welcome_channel_id' with the ID of the channel where you want to send the welcome message
    channel = bot.get_channel(1047658455172911116)
    if channel:
        # Create an embed for the welcome message
        embed = discord.Embed(title=f'Welcome {member.display_name} to the server!', color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)  # Set the thumbnail to the user's avatar

        # Add the image as an attachment to the embed
        file = discord.File('image.png')
        embed.set_image(url="attachment://image.png")  # Set the image URL to the attached image

        # Send the embed with the welcome message and image
        await channel.send(embed=embed, file=file)

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

    print(f'\nChannel([{message_record["channel"]}]) \nUser id({message_record["user_id"]}) \nUsername({message_record["username"]}) \nMessage({message_record["message_content"]})\nServer name({message_record["server_name"]})\n')

    # Process commands after logging
    await bot.process_commands(message)
    # Check if the message is from the console and starts with a specific command
    if message.author == bot.user and message.content.startswith("!console_message"):
        # Extract the message content after the command
        content = message.content.replace("!console_message", "").strip()
        
        # Send the extracted content to a specific channel (replace channel_id with the desired channel ID)
        channel_id = 1210278728328941628
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(content)
        else:
            print("Invalid channel ID")

@bot.command(help = "You'll be able to send messages through the console if you have the appropriate permissions")
async def send_console_message(ctx):
    # Replace ENABLED_ROLE_ID with the ID of the role that should be allowed to send console messages
    message_to_send = input("Enter your message to send to discord: ")
    if ctx.author.guild_permissions.administrator:
        await ctx.send(message_to_send)
    else:
        await ctx.send("You don't have permission to enable console messages.")

    # Add the role to the user (replace ENABLED_ROLE_ID with the ID of the role)
    role = ctx.guild.get_role(1216159919745798204)
    if role:
        await ctx.author.add_roles(role)
    else:
        print("Invalid role ID")


@bot.command(help="Search for available commands.")
async def search_command(ctx, command_name: str):
    command_names = [cmd.name for cmd in bot.commands]
    if command_name in command_names:
        command = bot.get_command(command_name)
        if command:
            command_help = command.help if command.help else "No help information available."
            await ctx.reply(f"The command '{command_name}' is available.\n\nHelp: {command_help}")
        else:
            await ctx.reply(f"The command **{command_name}** is available.")
    else:
        await ctx.reply(f"The command **{command_name}** is not available.")


bot.run(TOKEN)