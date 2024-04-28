import os
import discord
from dotenv import load_dotenv
import pickle
from random import randint
from discord.ext import commands


os.system('cls')

# Load environment variables
load_dotenv()
TOKEN = os.getenv('ENVDISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('ENVCHANNEL_ID'))

# Bot setup
intents = discord.Intents.default()
#bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
intents.message_content = True

# Filename for storing message records
RECORDS_FILENAME = os.getenv('ENVRECORDS_FILENAME')

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


@bot.command()
async def roll(ctx):
    await ctx.send(f'You rolled: **{randint(1, 666)}**')

# Handling bot startup
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Erika"))

    # Change bot avatar
    with open('projectK.gif', 'rb') as f:
        avatar_bytes = f.read()
    await bot.user.edit(avatar=avatar_bytes)
    await bot.user.edit(username="Bernso")

# Adds the 'Muted' role
async def add_mute_role(guild, user):
    role = discord.utils.get(guild.roles, name="Muted")  # Assuming the role name is "Muted"
    if role:
        await user.add_roles(role)
        return True
    else:
        return False

# Removes the 'Muted' role
async def remove_mute_role(guild, user):
    role = discord.utils.get(guild.roles, name="Muted")  # Assuming the role name is "Muted"
    if role:
        await user.remove_roles(role)
        return True
    else:
        return False

# Handles incoming messages
@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return
    from responses import get_response
    user_message = message.content.lower()  # Convert message to lowercase for comparisons
    response = await get_response(user_message, message)
    
    # Check for the !mute command
    if user_message.startswith('!mute'):
        # Check if the user has the 'Bernso' role
        if discord.utils.get(message.author.roles, name=("Bernso" or "yuka")):
            # Check if the user has permission to manage roles
            if message.author.guild_permissions.manage_roles:
                # Get the mentioned user
                if message.mentions:
                    mentioned_user = message.mentions[0]
                    # Add the mute role to the mentioned user
                    if await add_mute_role(message.guild, mentioned_user):
                        await message.reply(f"{mentioned_user.mention} has been muted.")
                    else:
                        await message.reply("Muted role not found. Please create a role named 'Muted'.")
                else:
                    await message.reply("Please mention a user to mute.")
            else:
                await message.reply("You do not have permission to use this command.")
                print(f"{message.author} tried to use a command out of their control.")
        else:
            await message.reply("You do not have permission to use this command.")
            print(f"{message.author} tried to use a command out of their control.")
    elif user_message.startswith('!unmute'):  # Check for the !unmute command
        if discord.utils.get(message.author.roles, name=("Bernso" or "yuka")):
            if message.author.guild_permissions.manage_roles:  # Check if the user has permission to manage roles
                if message.mentions:
                    mentioned_user = message.mentions[0]
                    if await remove_mute_role(message.guild, mentioned_user):
                        await message.reply(f"{mentioned_user.mention} has been unmuted.")
                    else:
                        await message.reply("Muted role not found. Please create a role named 'Muted'.")
                else:
                    await message.reply("Please mention a user to unmute.")
            else:
                await message.reply("You do not have permission to use this command.")
                print(f"{message.author} tried to use a command out of their control.")
        else:
            await message.reply("You do not have permission to use this command.")
            print(f"{message.author} tried to use a command out of their control.")
    else:
        if response:
            await message.reply(response, mention_author=True)

        # Record the message details
        message_record = {
            'channel': str(message.channel),
            'user_id': str(message.author.id),
            'username': str(message.author),
            'message_content': message.content,
            'server_id': str(message.guild),
            'server_name': str(message.guild),
            'bot_response': response
        }
        message_records.append(message_record)

        # Save the updated records to a pickle file
        with open(RECORDS_FILENAME, 'wb') as file:
            pickle.dump(message_records, file)

        print(f'\nChannel([{message_record["channel"]}]) \nUser id({message_record["user_id"]}) \nUsername({message_record["username"]}) \nMessage({message_record["message_content"]})\nResponse({message_record["bot_response"]})\nServer name({message_record["server_name"]})\n')


# Sends message history
async def send_message_history(message, message_records):
    # Extract message content, username, and server name for each record
    message_history = '\n'.join([f"{record.get('message_content', 'Unknown')} - {record.get('username', 'Unknown')} ({record.get('server_name', 'Unknown')})" for record in message_records])
    
    # Split message into chunks of 1900 characters or less
    chunks = [message_history[i:i+1900] for i in range(0, len(message_history), 1900)]
    
    # Send each chunk as a separate message
    for chunk in chunks:
        await message.channel.send(f"```{chunk}```")
    
    # Reply to the user to inform them that all message history chunks have been sent
    await message.reply("All message history has been uploaded :thumbsup:")

    


        
# Main entry point
def main():
    # Prompt user to open message records file when space bar is pressed
    
    key_input = input("Type 1 to open the message records file: ")
    if key_input.lower() == '1':
        try:
            with open(RECORDS_FILENAME, 'rb') as file:
                message_records = pickle.load(file)
            print("Message records file opened successfully!")
            print("Contents:")
            for record in message_records:
                print(record)
        except FileNotFoundError:
            print("Message records file not found.")
        input()
    else: 
        print("Exiting...")
        #sleep(1)
        os.system("cls")
        print("Exited")
        

   
    bot.run(TOKEN)



if __name__ == '__main__':
    main()
