import discord
import random
from Old.main import send_message_history
import pickle
import os

# THIS HAS BEEN TRANSFERRED TO A NEW STYLE WITH COMMANDS INSTEAD OF RESPONSES



# Return None to not send a message

RECORDS_FILENAME = os.getenv('RECORDS_FILENAME')

# Get bot response
async def get_response(user_input: str, message: discord.Message) -> str:
    lowered: str = user_input.lower()
    
    #if 'hello' in lowered:
    #    return 'What do you want?'
    
    #elif '!message history' in lowered:
    #    try:
    #        with open(RECORDS_FILENAME, 'rb') as file:
    #            message_records = pickle.load(file)
    #        await send_message_history(message, message_records)
    #        return None  
    #    except FileNotFoundError:
    #        print("Message records file not found.")
            
    
    
    #elif 'how are you' in lowered:
    #    return 'kys'
     
     
    #elif "!bot will i pass my gcse's?" in lowered: 
    #    if message.author == "vboss890": 
    #        return 'You stupid monkey you dont have a chance of passing' 
    #    elif message.author == 'kefayt_': 
    #        return 'jew' 
    #    else: 
    #        return f"You have a **{random.randint(0,100)}%** chance to pass your GCSe's" 
     
    #elif '!friends' in lowered: 
    #    if message.author.id == '712946563508469832': 
    #        return 'Bro is god' 
    #    elif message.author == 'kefayt_': 
    #        return 'Nuh uh' 
    #    elif message.author == 'vboss890': 
    #        return 'Bros only friends are the monkeys.' 
    #    return f'You have {random.randint(-1, 15)} friends.'
    
    #elif 'kys' in lowered:
    #    return 'https://tenor.com/view/yuta-jjk-jujutsu-kaisen-i-will-kill-myself-okkotsu-gif-1986392651623942939'
    #
    #elif 'bye' in lowered:
    #    return 'Never come back! :wave:'
    
    #elif 'nuh-uh' in lowered:
    #    return 'YUH-UH'
    #
    #elif 'yuh-uh' in lowered:
    #    return 'NUH-UH'
    #
    #elif 'nuh uh' in lowered:
    #    return 'YUH-UH'
    #
    #elif 'yuh uh'  in lowered:
    #    return 'NUH-UH'
    
    #elif '!roll' in lowered:
    #    return f'You rolled: **{random.randint(1, 666)}**'
    
    #elif '!who am i?' in lowered:
    #    if message.author == '.bernso':
    #        return 'a nazi! (he might be hitler himself, or so he thinks)'
    #    elif message.author == 'vboss890':
    #        return 'a monkey!'
    #    elif message.author == 'kefayt_':
    #        return 'a jew who narrowly escaped being gassed (by me)'
    #    elif message.author == 'y.uka':
    #        return 'DA GOAT'
    #    elif message.author == 'swayzz1820':
    #        return 'YOU FINALLY JOINED'
    #    else:
    #        return 'DM .bernso to get your own quote.'
    
    #elif '!manhwa' in lowered:
    #    return 'World After The Fall :on: :top:, any other opinion is invalid'
    #
    #elif '!vishwa' in lowered:
    #    return '... is a monkey!'
    #
    #elif '!rouse' in lowered:
    #    return '... is a cheese muncher!'
    #
    #elif '!daniel' in lowered:
    #    return '... is an italian facist!'
    #
    #elif '!dhruv' in lowered:
    #    return '... is gay!'
    #
    #elif '!ben' in lowered:
    #    
    #    return '... is a nazi! (he might be hitler himself, or so he thinks)'
    #   
    #elif '!kasper' in lowered:
    #    
    #    return '... was gassed back in 1945 (he returned from the dead)'
    #
    #elif '!anime' in lowered:
    #    return 'Ragna Crimson :on: :top:'
    
    #elif '!lightnovel' in lowered:
    #    return 'The Beginning After The End - TBATE :on: :top:'
    
    #elif '!ethnicity' in lowered:
    #    ethinicities = ['Black', 'White', 'Monkey', 'African', 'Chinese', 'Japanese', 'Kung-fu Panda', 'Nazi', 'Polar Bear', 'Polish', 'Jew']
    #    if message.author == 'vboss890':
    #        return f"Your ethnicity is: {ethinicities[0]} {ethinicities[2]}"
    #    elif message.author == 'Bernso':
    #        return f"your ethinicity is: {ethinicities}"
    #    elif message.author == 'kefayt_':
    #        return f"Your ethnicities are: {ethinicities[9]} {ethinicities[10]}"
    #    else:
    #        return f"Your ethnicity is: {random.choice(ethinicities)}"
    
    #elif '!bestseries' in lowered:
    #    return 'FATE :fire:'
    
    #elif '!when will i die?' in lowered:
    #    time = ['days', 'years', 'months', 'seconds', 'minutes']
    #    return f"You will die in {random.randint(1,100)} {random.choice(time)}"
    
    #elif '#' in lowered:
    #    return 'Stop making your text big you moron'
    #
    #elif ' is the best' in lowered:
    #    return 'NUH-UH @.bernso is the BEST'
    #
    #elif '!website' in lowered:
    #    return 'My website:\n   https://bernso.locum.dunz.net'
    #
    #elif '!monkeys' in lowered:
    #    return 'Like water melon and chicken'
    #
    #elif '!formula 1' in lowered:
    #    return 'Estavan Occon DA GOAT! (I hate lewis now, that money hungry freak)'
    #
    #elif '!spotify' in lowered:
    #    return 'My spotify playlist:\nhttps://open.spotify.com/playlist/6Mg5z7FrNYZ4DBVZvnjsP1?si=905dd469d16748e0'
    #
    #elif '!manga' in lowered:
    #    return 'Juujika No Rokin :on: :top:'
    
    #elif '!add' in lowered:
    #    numbers = [int(num) for num in lowered.split() if num.isdigit()]
    #    if len(numbers) >= 2:
    #        return f"I am asian, the answer is: **{sum(numbers)}**"
    #    else:
    #        return "Please provide at least two numbers after the '!add' command."
    #
    #elif '!times' in lowered:
    #    numbers = [int(num) for num in lowered.split() if num.isdigit()]
    #    if len(numbers) >= 2:
    #        result = 1
    #        for num in numbers:
    #            result *= num
    #        return f"I am asian, the answer is: **{result}**"
    #    else:
    #        return "Please provide at least two numbers after the '!multiply' command."
    #
    #elif '!internet state' in lowered:
    #    return "My Wi-Fi is finally back up!"
    
    #elif '!calc' in lowered:
    #    try:
    #        equation = lowered.split('!calc ')[1] 
    #        result = eval(equation)
    #        return f"I am asian, the answer is: **{result}**"
    #    except Exception as e:
    #        return f"Invalid equation or operation. Error: {str(e)}"
    #
    
    
    #elif '!help' in lowered:
    #    return "# Commands: \n*(caps do not matter)* \n\n1.   `hello`\n2. `how are you`\n3.   `kys`\n4. `bye`\n5.   `!roll` This goes from numbers 1 through to 666\n6.    `!vishwa`\n7.   `!rouse`\n8.    `!daniel`\n9.   `!dhruv`\n10.    `!ben`\n11.  `!mute {the user}`\n12.    `!add {the numbers you want to add serpeated by a space}` e.g. '!add 5 4 3' the output would be: '12'\n13.   `!kasper`\n14.  `!times {the numbers you want to multiply serpeated by a space}` e.g. !times 5 4 3, the output would be: '60'\n15.    `!calc {the equation}` This 'equation' can be anything, e.g. (1+2)/3 the output would be 1\n16.    `!message history` I regret add this feature\n17.    `nuh uh`\n18.   `yuh uh`\n19.   `!monkeys`\n19. `!bot will i pass my gcse's?` Outputs a percentage (depending on who sent the message)\n20.   `!Who am I?` Depending on who you are, the output will be different.\n21.  `!spotify` Will return @.bersno's spotify playlist.\n22.  `!website`\n23. `!friends` Will attempt to guess how many friends you have (depends based on who you are)\n24.  `!manhwa`\n25.  `!manga`\n26.   `!formula 1`\n27.   `!bestseries`\n28.  `!lightnovel`\n29.  `!anime`\n30.   `!ethnicity`\n31. `!internet state`\n32.  `!when will i die?`"

    #else: 
    #    return None