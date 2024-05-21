import discord #line:1
from discord .ext import commands ,tasks #line:2
from discord .ext .commands import MemberConverter #line:3
from discord import Embed #line:4
import random #line:5
import pickle #line:6
import os #line:7
from dotenv import load_dotenv #line:8
import asyncio #line:9
import traceback #line:10
import sys #line:11
import sqlite3 #line:12
import subprocess #line:13
import loguru #line:14
import time #line:15
import warnings #line:16
from typing import Union #line:17
import datetime #line:18
os .system ('cls')#line:21
load_dotenv ()#line:23
RECORDS_FILENAME =os .getenv ('ENVRECORDS_FILENAME')#line:24
TOKEN =os .getenv ('ENVDISCORD_TOKEN')#line:25
ENABLED_USER_ID =712946563508469832 #line:26
BOT_LOG_CHANNEL_ID =1234100559431077939 #line:27
VERIFIED_ROLE_NAME ="Verified"#line:28
class myLogger :#line:31
    def info (O00OOOOO0OOOO0OOO ):#line:32
        loguru .logger .info (O00OOOOO0OOOO0OOO )#line:33
    def warning (OOO0000000OO00OO0 ):#line:35
        loguru .logger .warning (OOO0000000OO00OO0 )#line:36
    def error (O0OO0000000O00OO0 ):#line:38
        loguru .logger .error (O0OO0000000O00OO0 )#line:39
    def success (O0000O0O0O0O00OOO ):#line:41
        loguru .logger .success (O0000O0O0O0O00OOO )#line:42
try :#line:46
    with open (RECORDS_FILENAME ,'rb')as file :#line:47
        message_records =pickle .load (file )#line:48
except FileNotFoundError :#line:49
    message_records =[]#line:50
    myLogger .warning ("Message records file not found. Creating a new one.")#line:51
    yes =open ('message_records.pkl','w')#line:52
    yes .close ()#line:53
except EOFError :#line:54
    message_records =[]#line:55
    myLogger .error ("The message records file is empty or corrupted.")#line:56
async def reply_message_history (O0O0O0OOOOO0OO000 ,O00O0O0O000OO000O ):#line:60
    OOOO000OOOOO0O0OO ='\n'.join ([f"{OO0OO0O000OOO0O0O.get('message_content', 'Unknown')} - {OO0OO0O000OOO0O0O.get('username', 'Unknown')} ({OO0OO0O000OOO0O0O.get('server_name', 'Unknown')})"for OO0OO0O000OOO0O0O in O00O0O0O000OO000O ])#line:64
    O000OOO0OOOOOO0O0 =[OOOO000OOOOO0O0OO [O00OO00O0000O0O00 :O00OO00O0000O0O00 +1900 ]for O00OO00O0000O0O00 in range (0 ,len (OOOO000OOOOO0O0OO ),1900 )]#line:67
    for OO0OO000OOO00OOO0 in O000OOO0OOOOOO0O0 :#line:70
        await O0O0O0OOOOO0OO000 .channel .reply (f"```{OO0OO000OOO00OOO0}```")#line:71
    await O0O0O0OOOOO0OO000 .reply ("All message history has been uploaded :thumbsup:")#line:74
async def send_timed_message ():#line:78
    await bot .wait_until_ready ()#line:79
    OO00OOOO0O0OO0OO0 =bot .get_channel (1225352074955591713 )#line:80
    OOO00OOOO000OO000 =""#line:81
    while not bot .is_closed ():#line:83
        if OOO00OOOO000OO000 :#line:84
            await OO00OOOO0O0OO0OO0 .send (OOO00OOOO000OO000 )#line:85
        await asyncio .sleep (10000 )#line:86
class CustomHelpCommand (commands .HelpCommand ):#line:91
    def __init__ (OOO0O0OO00O000O0O ):#line:92
        super ().__init__ ()#line:93
        OOO0O0OO00O000O0O .prefix =None #line:94
    def get_command_signature (OOO00000O0OOO0OOO ,OO0OOOOOO00O000OO ):#line:96
        if OOO00000O0OOO0OOO .prefix :#line:97
            return f"{OOO00000O0OOO0OOO.prefix}{OO0OOOOOO00O000OO.qualified_name} {OO0OOOOOO00O000OO.signature}"#line:98
        else :#line:99
            return f"{OO0OOOOOO00O000OO.qualified_name} {OO0OOOOOO00O000OO.signature}"#line:100
    async def send_bot_help (OOO00O00O00O00OOO ,O0OOOOOO00OOO0000 ):#line:102
        OOOOO0O0OOO0OOO00 =25 #line:103
        OO0OO0OO000OOO0O0 =[OOO00O00O00O00OOO .get_command_signature (OO0O00O0000O0OO00 )for OOO0O00000000O0O0 ,OO00O0OO0000OO00O in O0OOOOOO00OOO0000 .items ()for OO0O00O0000O0OO00 in OO00O0OO0000OO00O ]#line:104
        OO00OO00OO00000OO =[OO0OO0OO000OOO0O0 [OO0O0OO000OOO0OOO :OO0O0OO000OOO0OOO +OOOOO0O0OOO0OOO00 ]for OO0O0OO000OOO0OOO in range (0 ,len (OO0OO0OO000OOO0O0 ),OOOOO0O0OOO0OOO00 )]#line:105
        O0OO0O0OO0O00OOO0 =[]#line:107
        for OO0O0000O00O000OO ,O0O00OOOO00OOOOOO in enumerate (OO00OO00OO00000OO ,start =1 ):#line:108
            O000O00OOOO00O000 =discord .Embed (title =f"Bot Commands (Page {OO0O0000O00O000OO})",color =discord .Color .blue ())#line:109
            O000O00OOOO00O000 .description ="\n".join (O0O00OOOO00OOOOOO )#line:110
            O0OO0O0OO0O00OOO0 .append (O000O00OOOO00O000 )#line:111
        O000O000000OO0O00 =await OOO00O00O00O00OOO .context .send (embed =O0OO0O0OO0O00OOO0 [0 ])#line:113
        if len (O0OO0O0OO0O00OOO0 )>1 :#line:115
            OO00OO00000O0O0O0 =Pages (O0OO0O0OO0O00OOO0 )#line:116
            await O000O000000OO0O00 .edit (view =OO00OO00000O0O0O0 )#line:117
    async def send_command_help (OOOO0O0000O000000 ,O000O00O000O0OO00 ):#line:119
        OO000OO0O0OO000O0 =discord .Embed (title =f"Command Help: {O000O00O000O0OO00.name}",description =O000O00O000O0OO00 .help ,color =discord .Color .blue ())#line:120
        OO000OO0O0OO000O0 .add_field (name ="Usage",value =OOOO0O0000O000000 .get_command_signature (O000O00O000O0OO00 ),inline =False )#line:121
        await OOOO0O0000O000000 .get_destination ().send (embed =OO000OO0O0OO000O0 )#line:122
class Pages (discord .ui .View ):#line:124
    def __init__ (O0OOO0OO00OOO0000 ,O00OOOO0O0O0O0OOO ):#line:125
        super ().__init__ ()#line:126
        O0OOO0OO00OOO0000 .pages =O00OOOO0O0O0O0OOO #line:127
        O0OOO0OO00OOO0000 .current_page =0 #line:128
    @discord .ui .button (label ="⬅️",style =discord .ButtonStyle .grey )#line:130
    async def previous_button_callback (OOOO0OO0O0OOO0OOO ,O000000O0000OO0O0 :discord .Interaction ,OOO0OOO00O0O00O00 :discord .ui .Button ):#line:131
        OOOO0OO0O0OOO0OOO .current_page =max (0 ,OOOO0OO0O0OOO0OOO .current_page -1 )#line:132
        await O000000O0000OO0O0 .message .edit (embed =OOOO0OO0O0OOO0OOO .pages [OOOO0OO0O0OOO0OOO .current_page ],view =OOOO0OO0O0OOO0OOO )#line:133
    @discord .ui .button (label ="➡️",style =discord .ButtonStyle .grey )#line:135
    async def next_button_callback (OOOOOO00OO0OO00OO ,O0OO0000OO00OOO00 :discord .Interaction ,O00O000OOOOO000O0 :discord .ui .Button ):#line:136
        OOOOOO00OO0OO00OO .current_page =min (len (OOOOOO00OO0OO00OO .pages )-1 ,OOOOOO00OO0OO00OO .current_page +1 )#line:137
        await O0OO0000OO00OOO00 .message .edit (embed =OOOOOO00OO0OO00OO .pages [OOOOOO00OO0OO00OO .current_page ],view =OOOOOO00OO0OO00OO )#line:138
    async def start (O000000O00OOOO0O0 ,OOOOO00O0O0OOOOO0 :commands .Context ):#line:140
        O000000O00OOOO0O0 .current_page =0 #line:141
        O000000O00OOOO0O0 .message =await OOOOO00O0O0OOOOO0 .send (embed =O000000O00OOOO0O0 .pages [O000000O00OOOO0O0 .current_page ],view =O000000O00OOOO0O0 )#line:142
con =sqlite3 .connect ('level.db')#line:147
cur =con .cursor ()#line:148
intents =discord .Intents .all ()#line:149
bot_prefix ='.'#line:150
help_command =CustomHelpCommand ()#line:151
help_command .prefix =bot_prefix #line:152
bot =commands .Bot (command_prefix =bot_prefix ,intents =intents ,help_command =help_command )#line:153
@bot .command (help ="Creates a poll with a question and multiple options. Separate the question and options using '|' symbol. Example: !poll What is your favorite color? | Red | Blue | Green")#line:157
async def poll (O0000OO00O0000O00 ,*,question_and_options ):#line:158
    if O0000OO00O0000O00 .author .guild_permissions .administrator :#line:159
        await O0000OO00O0000O00 .message .delete ()#line:160
        O0OOOO0O0000O0000 =question_and_options .split ('|')#line:162
        O00000OOOOOO0OOOO =O0OOOO0O0000O0000 [0 ].strip ()#line:163
        O00000OO0O000O00O =[O00OO00O0O000O0O0 .strip ()for O00OO00O0O000O0O0 in O0OOOO0O0000O0000 [1 :]]#line:164
        if len (O00000OO0O000O00O )>10 :#line:166
            await O0000OO00O0000O00 .send (f"{O0000OO00O0000O00.author.mention} You can only have up to 10 options in a poll.")#line:167
            return #line:168
        O0O0000OOO00OO000 =discord .Embed (title =f"Poll: {O00000OOOOOO0OOOO}",color =discord .Color .blue ())#line:171
        for O0OOOO00OO00O0OOO ,O0OOOO00OO0O00O00 in enumerate (O00000OO0O000O00O ):#line:174
            O0O0000OOO00OO000 .add_field (name =f"Option {O0OOOO00OO00O0OOO + 1}",value =O0OOOO00OO0O00O00 ,inline =False )#line:175
        O0OO00O0OOOO00000 =await O0000OO00O0000O00 .send (embed =O0O0000OOO00OO000 )#line:178
        for O0OOOO00OO00O0OOO in range (len (O00000OO0O000O00O )):#line:179
            if O0OOOO00OO00O0OOO ==9 :#line:180
                await O0OO00O0OOOO00000 .add_reaction ("🔟")#line:181
            else :#line:182
                await O0OO00O0OOOO00000 .add_reaction (chr (0x0031 +O0OOOO00OO00O0OOO )+"\uFE0F\u20E3")#line:183
    else :#line:184
        await O0000OO00O0000O00 .message .delete ()#line:185
        await O0000OO00O0000O00 .send (f"{O0000OO00O0000O00.author.mention} You do not have permission to use this command.")#line:186
@bot .event #line:189
async def on_raw_reaction_add (O00O0OOO0000O00OO ):#line:190
    O0O000OOO0OOO0O00 =O00O0OOO0000O00OO .message_id #line:192
    OOOOO000O0O000OO0 =O00O0OOO0000O00OO .channel_id #line:193
    if O00O0OOO0000O00OO .event_type !='REACTION_ADD'or not O00O0OOO0000O00OO .member or O00O0OOO0000O00OO .member .bot :#line:194
        return #line:195
    O000OOO000OOOO0OO =bot .get_channel (OOOOO000O0O000OO0 )#line:196
    try :#line:197
        O00O0O0OOO0O00O00 =await O000OOO000OOOO0OO .fetch_message (O0O000OOO0OOO0O00 )#line:198
    except discord .NotFound :#line:199
        return #line:200
    if not O00O0O0OOO0O00O00 .embeds :#line:201
        return #line:202
    O00O0OOO00O0O0OO0 =O00O0O0OOO0O00O00 .embeds [0 ]#line:203
    if not O00O0OOO00O0O0OO0 .title or not O00O0OOO00O0O0OO0 .title .startswith ("Poll:"):#line:204
        return #line:205
    OOO0O0O0O00000000 =O00O0OOO0000O00OO .emoji #line:208
    if isinstance (OOO0O0O0O00000000 ,discord .PartialEmoji ):#line:209
        OOO0O0O0O00000000 =OOO0O0O0O00000000 .name #line:210
    for O0O00O0O0OOOO0000 in O00O0OOO00O0O0OO0 .fields :#line:211
        if O0O00O0O0OOOO0000 .name .startswith ("Option")and O0O00O0O0OOOO0000 .value ==OOO0O0O0O00000000 :#line:212
            await O00O0O0OOO0O00O00 .channel .send (f"{O00O0OOO0000O00OO.member.display_name} voted for {OOO0O0O0O00000000}.")#line:213
@bot .event #line:216
async def on_ready ():#line:217
    myLogger .info (f'Logged in as {bot.user.name}')#line:218
    myLogger .info (f'Bot ID: {bot.user.id}')#line:219
    myLogger .info (' ')#line:220
    await bot .change_presence (status =discord .Status .dnd ,activity =discord .Activity (type =discord .ActivityType .listening ,name ="Erika"))#line:224
    bot .loop .create_task (send_timed_message ())#line:226
    O00OOO0O0OOO000O0 =bot .get_channel (1234091236097396787 )#line:227
    if O00OOO0O0OOO000O0 :#line:228
        async for O0O0O0OOOO0OOOO00 in O00OOO0O0OOO000O0 .history ():#line:229
            await O0O0O0OOOO0OOOO00 .delete ()#line:231
        OO0OOOO00OO0OO0O0 =discord .Embed (title ="Verification",description ="Click below to verify.")#line:233
        await O00OOO0O0OOO000O0 .send (embed =OO0OOOO00OO0OO0O0 ,view =Verification ())#line:234
    else :#line:235
        myLogger .error ("Could not send verification message for whatever reason.")#line:236
    with open ('IMG_0935.JPEG','rb')as OO0O0O0000O0O0OO0 :#line:238
        O000OOO00OOOOO00O =OO0O0O0000O0O0OO0 .read ()#line:239
        OO0O0O0000O0O0OO0 .close ()#line:240
@bot .command (help ="Starts up the leveling system if it hasnt already.")#line:245
async def init (OO000O0OO0O0OOO0O ):#line:246
    if OO000O0OO0O0OOO0O .author .guild_permissions .administrator :#line:247
        cur .execute (f'''CREATE TABLE IF NOT EXISTS GUILD_{OO000O0OO0O0OOO0O.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')#line:249
        for O00O00O00O00OO0OO in OO000O0OO0O0OOO0O .guild .members :#line:251
            if not O00O00O00O00OO0OO .bot :#line:252
                cur .execute (f"INSERT INTO GUILD_{OO000O0OO0O0OOO0O.guild.id} (user_id) VALUES ({O00O00O00O00OO0OO.id})")#line:253
        con .commit ()#line:255
        await OO000O0OO0O0OOO0O .channel .send ("Leveling system initialized")#line:257
    else :#line:258
        await OO000O0OO0O0OOO0O .reply ("You do not haver permission to use this command.")#line:259
async def level_up_notification (OOOOOO0OOO00O0OOO ,O000O00O0OO0OOOOO ,O000OO0OO00OO0O0O ):#line:262
    OOO000OOOO00OO00O =f"Congratulations {OOOOOO0OOO00O0OOO.mention}! You've reached level {O000O00O0OO0OOOOO}!"#line:263
    await O000OO0OO00OO0O0O .send (OOO000OOOO00OO00O )#line:264
@bot .command (help ="Edit a user's experience.\n For the <amount> of xp you can use 'reset' to reset the user's XP.")#line:267
async def editxp (O00000OO00O0O00O0 ,O0OOO00000OO0000O :discord .Member ,OO0O0OO0OO0O0OOO0 ):#line:268
    if O00000OO00O0O00O0 .author .guild_permissions .administrator :#line:269
        try :#line:270
            cur .execute (f"SELECT * FROM GUILD_{O00000OO00O0O00O0.guild.id} WHERE user_id={O0OOO00000OO0000O.id}")#line:271
            OO00OO00OO0OO000O =cur .fetchone ()#line:272
            if OO00OO00OO0OO000O :#line:274
                if OO0O0OO0OO0O0OOO0 =="reset":#line:275
                    OO0OO0OOOOOO00O00 =0 #line:276
                else :#line:277
                    OO0OO0OOOOOO00O00 =max (0 ,OO00OO00OO0OO000O [1 ]+int (OO0O0OO0OO0O0OOO0 ))#line:278
                O0O0OO0O0O0OOOOOO =(OO00OO00OO0OO000O [1 ]//50 )+1 #line:281
                O0O0000O0000O0000 =(OO0OO0OOOOOO00O00 //50 )+1 #line:282
                O0O000000O0O000OO =OO00OO00OO0OO000O [1 ]%50 #line:283
                O0O0O00000O00000O =OO0OO0OOOOOO00O00 %50 #line:284
                O0O0OOOO000000000 =min ((O0O0OO0O0O0OOOOOO *50 ),50 )#line:287
                O0O0O0O00O000OO0O =min ((O0O0000O0000O0000 *50 ),50 )#line:288
                cur .execute (f"UPDATE GUILD_{O00000OO00O0O00O0.guild.id} SET exp={OO0OO0OOOOOO00O00} WHERE user_id={O0OOO00000OO0000O.id}")#line:290
                con .commit ()#line:291
                if O0O0000O0000O0000 >O0O0OO0O0O0OOOOOO :#line:294
                    OOOO00OOOOOO0OO0O =1217998981246881832 #line:296
                    OO0000O00O0O0OO00 =bot .get_channel (OOOO00OOOOOO0OO0O )#line:297
                    if OO0000O00O0O0OO00 :#line:298
                        await level_up_notification (O0OOO00000OO0000O ,O0O0000O0000O0000 ,OO0000O00O0O0OO00 )#line:299
                    if O0O0000O0000O0000 %5 ==0 :#line:302
                        for O0OOOOOOO00000000 in range (O0O0000O0000O0000 -5 ,0 ,-5 ):#line:304
                            OO00OO00000000OOO =f"level-{O0OOOOOOO00000000}"#line:305
                            OO0OOOOOO0OO0O00O =discord .utils .get (O00000OO00O0O00O0 .guild .roles ,name =OO00OO00000000OOO )#line:306
                            if not OO0OOOOOO0OO0O00O :#line:307
                                OO0OOOOOO0OO0O00O =await O00000OO00O0O00O0 .guild .create_role (name =OO00OO00000000OOO )#line:308
                            await O0OOO00000OO0000O .add_roles (OO0OOOOOO0OO0O00O )#line:309
                O0O0000O0O00OOOOO =discord .Embed (title ="XP and Level Change",color =discord .Color .gold ())#line:312
                O0O0000O0O00OOOOO .set_thumbnail (url =O0OOO00000OO0000O .avatar )#line:313
                O0O0000O0O00OOOOO .add_field (name ="User",value =O0OOO00000OO0000O .mention ,inline =False )#line:314
                O0O0000O0O00OOOOO .add_field (name ="Old XP",value =f"{O0O000000O0O000OO}/{O0O0OOOO000000000} (Level {O0O0OO0O0O0OOOOOO})",inline =False )#line:316
                O0O0000O0O00OOOOO .add_field (name ="New XP",value =f"{O0O0O00000O00000O}/{O0O0O0O00O000OO0O} (Level {O0O0000O0000O0000})",inline =False )#line:318
                await O00000OO00O0O00O0 .send (embed =O0O0000O0O00OOOOO )#line:320
            else :#line:321
                await O00000OO00O0O00O0 .send ("User not found in the database.")#line:322
        except sqlite3 .OperationalError as O0O0000000O0000O0 :#line:323
            await O00000OO00O0O00O0 .send ("Database error occurred.")#line:324
            myLogger .error ("SQLite Error:",O0O0000000O0000O0 )#line:325
    else :#line:326
        await O00000OO00O0O00O0 .reply ("You do not have permission to use this command.")#line:327
@bot .command (help ="Shows the specified user's experience and levels.")#line:330
async def xp (O0OO00OOO0O00O0O0 ,user :discord .User =None ):#line:331
    try :#line:332
        if user is None :#line:333
            user =O0OO00OOO0O00O0O0 .author #line:334
        cur .execute (f"SELECT * FROM GUILD_{O0OO00OOO0O00O0O0.guild.id} WHERE user_id={user.id}")#line:336
        O00O00OOO000OO000 =cur .fetchone ()#line:337
        if O00O00OOO000OO000 is not None :#line:339
            OO0O00O0O0OO00OOO =O00O00OOO000OO000 [1 ]#line:340
            OO0O0O00O0OOO0O0O =(OO0O00O0O0OO00OOO //50 )+1 #line:341
            O0O0OOO00OOO0OO0O =OO0O00O0O0OO00OOO %50 #line:342
            O0O0O0O0OO0O0OO00 =min ((OO0O0O00O0OOO0O0O *50 ),50 )#line:345
            O0OOO00O0O0O00OOO =Embed (title =f"{user.display_name}",color =discord .Color .green ())#line:348
            O0OOO00O0O0O00OOO .set_thumbnail (url =user .avatar )#line:349
            O0OOO00O0O0O00OOO .add_field (name ="XP",value =f"{O0O0OOO00OOO0OO0O}/{O0O0O0O0OO0O0OO00} XP",inline =True )#line:350
            O0OOO00O0O0O00OOO .add_field (name ="Level",value =OO0O0O00O0OOO0O0O ,inline =True )#line:351
            await O0OO00OOO0O00O0O0 .send (embed =O0OOO00O0O0O00OOO )#line:353
        else :#line:354
            await O0OO00OOO0O00O0O0 .send ("Hmm no such user in the database")#line:355
    except sqlite3 .OperationalError :#line:356
        await O0OO00OOO0O00O0O0 .send ("Database not initialized")#line:357
@bot .command (help ="Shows the top 5 highest level people in the server.")#line:360
async def leaderboard (O000O0OOOO0O000O0 ):#line:361
    try :#line:362
        cur .execute (f"SELECT user_id, MAX(exp) FROM GUILD_{O000O0OOOO0O000O0.guild.id} GROUP BY user_id ORDER BY MAX(exp) DESC LIMIT 5")#line:363
        O000OO00O00000OOO =cur .fetchall ()#line:364
        if O000OO00O00000OOO :#line:366
            O00O0O0O0OOO00000 =discord .Embed (title ="Leaderboard",color =discord .Color .blue ())#line:367
            for OOO000O0O00O0OO0O ,(O00000O00OO0O0000 ,O00000OOO0O00O00O )in enumerate (O000OO00O00000OOO ,start =1 ):#line:369
                OOOOOO000OO0OO00O =O000O0OOOO0O000O0 .guild .get_member (O00000O00OO0O0000 )#line:370
                if OOOOOO000OO0OO00O :#line:371
                    OO000O00OO0OO0OOO =(O00000OOO0O00O00O //50 )+1 #line:372
                    O0O00O0000000O00O =O00000OOO0O00O00O %50 #line:373
                    O00O0O0O0OOO00000 .add_field (name =f"{OOO000O0O00O0OO0O}. {OOOOOO000OO0OO00O.display_name}",value =f"XP: {O0O00O0000000O00O} | Level: {OO000O00OO0OO0OOO}",inline =False )#line:375
            await O000O0OOOO0O000O0 .send (embed =O00O0O0O0OOO00000 )#line:377
        else :#line:378
            await O000O0OOOO0O000O0 .send ("No users found in the database.")#line:379
    except sqlite3 .OperationalError :#line:380
        await O000O0OOOO0O000O0 .send ("Database not initialized")#line:381
    except Exception as OO0000O00O000OO00 :#line:382
        myLogger .error (f"An error has occurred: {OO0000O00O000OO00}")#line:383
@bot .command (name ="role_colour")#line:387
async def changecolor (OOO000000O0O0O0O0 ,OO0O0O000O0OOO000 :str ,OOO00000OOO0OO0O0 :discord .Color ):#line:388
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
    """#line:407
    if OOO000000O0O0O0O0 .author .guild_permissions .administrator :#line:408
        O00O00OO00OOOO0OO =OOO000000O0O0O0O0 .guild #line:409
        O0O0O0O0O000O00OO =discord .utils .get (O00O00OO00OOOO0OO .roles ,name =OO0O0O000O0OOO000 )#line:410
        if O0O0O0O0O000O00OO :#line:412
            try :#line:413
                await O0O0O0O0O000O00OO .edit (color =OOO00000OOO0OO0O0 )#line:414
                await OOO000000O0O0O0O0 .reply (f"Changed color of role {OO0O0O000O0OOO000} to {OOO00000OOO0OO0O0}")#line:415
                OO00OO00O0OO0OOOO =discord .Embed (title ="Role Color Changed",description =f"The color of role {O0O0O0O0O000O00OO.mention} has been changed to {OOO00000OOO0OO0O0}.",color =OOO00000OOO0OO0O0 )#line:422
                OO00OO00O0OO0OOOO .set_author (name =OOO000000O0O0O0O0 .author .name ,icon_url =OOO000000O0O0O0O0 .author .avatar )#line:423
                OO00OO00O0OO0OOOO .set_footer (text ="Role Color Change Notification")#line:424
                O000O0OO0000OOO00 =bot .get_channel (1208431780529578014 )#line:426
                await O000O0OO0000OOO00 .send (embed =OO00OO00O0OO0OOOO )#line:427
            except discord .Forbidden :#line:429
                await OOO000000O0O0O0O0 .reply ("I don't have permissions to edit roles.")#line:430
            except discord .HTTPException :#line:431
                await OOO000000O0O0O0O0 .reply ("Failed to change color.")#line:432
        else :#line:433
            await OOO000000O0O0O0O0 .send (f"Role {OO0O0O000O0OOO000} not found.")#line:434
    else :#line:435
        await OOO000000O0O0O0O0 .reply ("You do not have permission to use this command.")#line:436
class Verification (discord .ui .View ):#line:439
    def __init__ (O000OOOO0OO0OOO0O ):#line:440
        super ().__init__ (timeout =None )#line:441
    @discord .ui .button (label ="Verify",custom_id ="Verify",style =discord .ButtonStyle .success )#line:443
    async def verify (O00O0OOOO0O000O0O ,O00O0OOO0OOOO0O00 ,O000OOO000O00O00O ):#line:444
        OO0O0OOO00OOOO0O0 =1234090799571013712 #line:445
        OOO00000OOOOOOO0O =1234090964549767212 #line:446
        OOOO0000O0O00000O =O00O0OOO0OOOO0O00 .user #line:447
        if OO0O0OOO00OOOO0O0 not in [O0O00OOO0O00OOO0O .id for O0O00OOO0O00OOO0O in OOOO0000O0O00000O .roles ]:#line:448
            await OOOO0000O0O00000O .remove_roles (OOOO0000O0O00000O .guild .get_role (OOO00000OOOOOOO0O ))#line:449
            await OOOO0000O0O00000O .add_roles (OOOO0000O0O00000O .guild .get_role (OO0O0OOO00OOOO0O0 ))#line:450
            await OOOO0000O0O00000O .send ("You have been verified!")#line:451
@bot .command (help ="Creates the verify message people can use to verify.")#line:454
async def start_verify (O0OOOOO0O0OOOO0OO ):#line:455
    if O0OOOOO0O0OOOO0OO .author .guild_permissions .administrator :#line:456
        O00OOO00OOOOOO000 =discord .Embed (title ="Verification",description ="Click below to verify.")#line:457
        await O0OOOOO0O0OOOO0OO .send (embed =O00OOO00OOOOOO000 ,view =Verification ())#line:458
    else :#line:459
        await O0OOOOO0O0OOOO0OO .reply ("You cannot use this command. Required = Administrator")#line:460
@bot .command (name ='runfile',help ="Do not put .py after the file name as it will not work\nThe current working files are:\n- " "hello.py\n- fakehack.py\n- PassGen.py")#line:465
async def run_file (OOO000O0O00O0OOOO ,O00OOOO00000O0O0O :str ):#line:466
    try :#line:467
        O0O0O0000O0O0OOO0 =subprocess .run (['python',f'{O00OOOO00000O0O0O}.py'],capture_output =True ,text =True )#line:469
        OOO00OO00OOOOOO00 =O0O0O0000O0O0OOO0 .stdout #line:470
        await OOO000O0O00O0OOOO .send (f"Output:\n```{OOO00OO00OOOOOO00}```")#line:473
    except Exception as O00OO000O00OO0O0O :#line:474
        await OOO000O0O00O0OOOO .send (f"An error occurred: {str(O00OO000O00OO0O0O)}")#line:475
@bot .command (name ='dm_runfile',help ="Do not put .py after the file name as it will not work\nThe current working files are:\n- " "hello.py\n- fakehack.py\n- PassGen.py")#line:480
async def dm_run_file (O0O0OO00O0O0OO000 ,O00O00O0OOO00O0OO :str ):#line:481
    try :#line:482
        O00000O0O000000OO =O0O0OO00O0O0OO000 .author #line:483
        O00O0OO0O00O0000O =subprocess .run (['python',f'{O00O00O0OOO00O0OO}.py'],capture_output =True ,text =True )#line:485
        OO00OO000000OOOO0 =O00O0OO0O00O0000O .stdout #line:486
        await O00000O0O000000OO .send (f"Output:\n```{OO00OO000000OOOO0}```")#line:489
        await O0O0OO00O0O0OO000 .send (f"{O00000O0O000000OO.mention} check your dms")#line:490
    except Exception as OOO00000OOOOOO0O0 :#line:491
        await O0O0OO00O0O0OO000 .send (f"An error occurred: {str(OOO00000OOOOOO0O0)}")#line:492
@bot .command (name ='dm-test',help ="Say the command followed by the number of messages you want the bot to send to your DM.")#line:495
async def dm_test (OO00O000OO0OOOOOO ,O0O0O0OOOO0O0O00O :int ):#line:496
    OOO0O000000OOO00O ="QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*()_+-={[]};:/?.><,|~`"#line:497
    O0OOO0OO0O0O00OO0 =OO00O000OO0OOOOOO .author #line:498
    try :#line:499
        if O0O0O0OOOO0O0O00O ==1 :#line:500
            await O0OOO0OO0O0O00OO0 .send (f"Hello Monkey! {random.choice(OOO0O000000OOO00O)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}")#line:501
            await O0OOO0OO0O0O00OO0 .send ("https://tenor.com/view/monkey-freiza-dbs-dbz-gif-25933202")#line:502
            await OO00O000OO0OOOOOO .reply (f"{O0O0O0OOOO0O0O00O} message(s) sent to your DM.")#line:503
        else :#line:504
            for _O0OO000O00OOO00O0 in range (O0O0O0OOOO0O0O00O //2 ):#line:505
                await O0OOO0OO0O0O00OO0 .send (f"Hello Monkey! {random.choice(OOO0O000000OOO00O)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}")#line:506
                await O0OOO0OO0O0O00OO0 .send ("https://tenor.com/view/monkey-freiza-dbs-dbz-gif-25933202")#line:507
            await OO00O000OO0OOOOOO .reply (f"{O0O0O0OOOO0O0O00O//2} message(s) sent to your DM.")#line:508
    except Exception as OO0OO00000O0O0O00 :#line:509
        await OO00O000OO0OOOOOO .send (f"An error occurred: {str(OO0OO00000O0O0O00)}\nThis error is most likely due to your DMs being private. " f"Please make them public.")#line:512
@bot .command (help ="The bot will randomly generate a password for you based on the length you requested.\n\nThe <special_chars> " "is boolean, it will be 'True' or 'False'.",name ='pass-gen')#line:519
async def password_gen (OOOO0OO00O0O00O0O ,OO0OO00OO0O0O00OO :int ,O00O00OO0O0O000O0 :bool ):#line:520
    O0000OOO0000OOO00 =OOOO0OO00O0O00O0O .author #line:521
    O0OOOO0OOOOOO0OOO ="QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"#line:522
    if O00O00OO0O0O000O0 :#line:523
        O0OOOO0OOOOOO0OOO +="!@#$%^&*()_+-={[]};:/?.><,|~`"#line:524
    OOOOO000O0O0OOO0O =''.join (random .choice (O0OOOO0OOOOOO0OOO )for _OOO0O0O0OOO000OO0 in range (OO0OO00OO0O0O00OO ))#line:525
    await O0000OOO0000OOO00 .send (f"Your password is:\n```{OOOOO000O0O0OOO0O}```")#line:526
    await OOOO0OO00O0O00O0O .reply ("Your generated password has been sent to your dm's.")#line:527
@bot .command (help ="Shows the users ping.")#line:530
async def ping (OO00OO00O000O00OO ):#line:531
    await OO00OO00O000O00OO .reply (f"Your ping is:   `{round(bot.latency * 1000)} ms`")#line:532
@bot .command (help ="Deletes a specified role.")#line:535
async def delete_role (OO0O0O0O00O00O00O ,O0O0O0000OO0O0O0O :str ):#line:536
    OOO00O000O0OO0OOO =OO0O0O0O00O00O00O .guild #line:537
    OOOO0000OO0OOOOOO =discord .utils .get (OOO00O000O0OO0OOO .roles ,name =O0O0O0000OO0O0O0O )#line:540
    if not OOOO0000OO0OOOOOO :#line:543
        O0000OO0OO00OOOO0 =discord .Embed (title ="Error",description =f"Role '{O0O0O0000OO0O0O0O}' not found.",color =discord .Color .red ())#line:548
        await OO0O0O0O00O00O00O .send (embed =O0000OO0OO00OOOO0 )#line:549
        return #line:550
    await OOOO0000OO0OOOOOO .delete ()#line:553
    O0OOO000OOO00000O =OO0O0O0O00O00O00O .author .mention #line:556
    O0000OO0OO00OOOO0 =discord .Embed (title ="Role Deleted",description =f"Role {OOOO0000OO0OOOOOO} has been deleted by {O0OOO000OOO00000O}.",color =discord .Color .red ())#line:563
    await OO0O0O0O00O00O00O .send (embed =O0000OO0OO00OOOO0 )#line:564
@bot .command (help ="Creates a mentionable role with a name and color, and optionally assigns it to mentioned members.")#line:567
async def create_role (OO0O0OO00OOOO0000 ,OO0OOOOO0OO00OO0O :str ,O0O00O000OO00000O :discord .Color ,*OO0000O0OOOOOO0OO :discord .Member ):#line:568
    if OO0O0OO00OOOO0000 .author .guild_permissions .administrator :#line:569
        OO0O000OOOOOOO0O0 =OO0O0OO00OOOO0000 .guild #line:570
        if discord .utils .get (OO0O000OOOOOOO0O0 .roles ,name =OO0OOOOO0OO00OO0O ):#line:573
            OO0O00OOO00O00O0O =discord .Embed (title ="Error",description =f"Role '{OO0OOOOO0OO00OO0O}' already exists.",color =discord .Color .red ())#line:578
            await OO0O0OO00OOOO0000 .send (embed =OO0O00OOO00O00O0O )#line:579
            return #line:580
        OO0000OOOO0O00OOO =await OO0O000OOOOOOO0O0 .create_role (name =OO0OOOOO0OO00OO0O ,color =O0O00O000OO00000O ,mentionable =True )#line:583
        await OO0000OOOO0O00OOO .edit (position =1 )#line:586
        for OO0O00OOO000O0OO0 in OO0000O0OOOOOO0OO :#line:589
            await OO0O00OOO000O0OO0 .add_roles (OO0000OOOO0O00OOO )#line:590
        if OO0000O0OOOOOO0OO :#line:592
            OOOOOO0O0OOO0000O =", ".join (O00000O0O00O00O0O .mention for O00000O0O00O00O0O in OO0000O0OOOOOO0OO )#line:593
            OO0O00OOO00O00O0O =discord .Embed (title ="Role Created",description =f"Role '{OO0OOOOO0OO00OO0O}' created and assigned to {OOOOOO0O0OOO0000O} by {OO0O0OO00OOOO0000.author.mention}.",color =discord .Color .green ())#line:598
        else :#line:599
            OO0O00OOO00O00O0O =discord .Embed (title ="Role Created",description =f"Role '{OO0OOOOO0OO00OO0O}' created by {OO0O0OO00OOOO0000.author.mention}.",color =discord .Color .green ())#line:604
        await OO0O0OO00OOOO0000 .send (embed =OO0O00OOO00O00O0O )#line:606
@bot .command (help ="This is just a test command, it will create embed message that go from pages 1 through 6 with interactable " "buttons.")#line:611
async def page_test (OO0O0OOO00OOOOOO0 :commands .Context ):#line:612
    OOOOOOOOO0OOO0000 =[discord .Embed (title =f"Page {OO00OOOOO000O0000}",description =f"Content for page {OO00OOOOO000O0000}")for OO00OOOOO000O0000 in range (1 ,6 )]#line:613
    O000OO0O00000OOO0 =Pages (OOOOOOOOO0OOO0000 )#line:614
    await O000OO0O00000OOO0 .start (OO0O0OOO00OOOOOO0 )#line:615
@bot .command (help ="Replies to your messag with a link to my linktree.")#line:618
async def linktree (OO00OO0O000O0OO00 ):#line:619
    await OO00OO0O000O0OO00 .reply ('Link to Linktree:\nhttps://linktr.ee/Bernso')#line:620
@bot .command (help ="Sends my GitHub page.")#line:623
async def github (OO00OO0OO00000000 ):#line:624
    await OO00OO0OO00000000 .reply ("Link to GitHub:\nhttps://github.com/Bernso")#line:625
@bot .command (help ="Gives you a random number from 1-666")#line:628
async def roll (O0OO00O00O00O00O0 ):#line:629
    await O0OO00O00O00O00O0 .reply (f'You rolled: **{random.randint(1, 666)}**')#line:630
@bot .command (help ='Replies to your message')#line:633
async def hello (OOO000O0OO00O00O0 ):#line:634
    await OOO000O0OO00O00O0 .reply ('What do you want?')#line:635
giveaways ={}#line:640
@bot .command (help ="Start a giveaway. Usage: .giveaway <prize> <duration>")#line:642
async def giveaway (OO0O0OOOOOO00OO00 ,OOO00OO00O00OO00O ,O0O000O000O0OO000 ):#line:643
    if OO0O0OOOOOO00OO00 .user .guild_permissions .administrator :#line:644
        OOO0OO0O0OOO0OO0O =''.join (random .choices ('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',k =6 ))#line:646
        OO0O0OO0O00OOO0O0 ,OOOOO0OO00O0O000O =O0O000O000O0OO000 [:-1 ],O0O000O000O0OO000 [-1 ]#line:649
        if OOOOO0OO00O0O000O =='s':#line:650
            OOOOOO000O000O000 =int (OO0O0OO0O00OOO0O0 )#line:651
        elif OOOOO0OO00O0O000O =='m':#line:652
            OOOOOO000O000O000 =int (OO0O0OO0O00OOO0O0 )*60 #line:653
        elif OOOOO0OO00O0O000O =='h':#line:654
            OOOOOO000O000O000 =int (OO0O0OO0O00OOO0O0 )*3600 #line:655
        elif OOOOO0OO00O0O000O =='d':#line:656
            OOOOOO000O000O000 =int (OO0O0OO0O00OOO0O0 )*86400 #line:657
        else :#line:658
            await OO0O0OOOOOO00OO00 .send ("Invalid duration format. Use 's' for seconds, 'm' for minutes, 'h' for hours, 'd' for days.")#line:659
            return #line:660
        await OO0O0OOOOOO00OO00 .send (f"Giveaway Code: {OOO0OO0O0OOO0OO0O}")#line:663
        O0000O0OO000O00O0 =discord .Embed (title =f"🎉 Giveaway: {OOO00OO00O00OO00O}",description =f"React with 🎉 to enter!\nDuration: {O0O000O000O0OO000}",color =0x00ff00 )#line:666
        O00OOO00O0000OOO0 =datetime .datetime .utcnow ()+datetime .timedelta (seconds =OOOOOO000O000O000 )#line:669
        O00OOO00O0000OOO0 =O00OOO00O0000OOO0 .replace (microsecond =0 )#line:670
        O0000O0OO000O00O0 .set_footer (text =f"Giveaway ends at {O00OOO00O0000OOO0} UTC")#line:672
        O0OOO000OOOO0000O =await OO0O0OOOOOO00OO00 .send (embed =O0000O0OO000O00O0 )#line:673
        await O0OOO000OOOO0000O .add_reaction ("🎉")#line:676
        giveaways [OOO0OO0O0OOO0OO0O ]={'prize':OOO00OO00O00OO00O ,'end_time':O00OOO00O0000OOO0 ,'participants':[],'message_id':O0OOO000OOOO0000O .id }#line:683
        await end_giveaway (OOO0OO0O0OOO0OO0O ,O0OOO000OOOO0000O )#line:686
    else :#line:687
        await OO0O0OOOOOO00OO00 .reply ("You do not have permission to run this command.")#line:688
@bot .command (help ="Reroll the winner of a giveaway. Usage: .reroll <giveaway_code>")#line:690
async def reroll (OOOOOOOO0O0O0O00O ,O0O00000O0OOO00O0 ):#line:691
    if O0O00000O0OOO00O0 not in giveaways :#line:692
        await OOOOOOOO0O0O0O00O .send ("This giveaway does not exist.")#line:693
        return #line:694
    O0O000000OO00OOOO =giveaways [O0O00000O0OOO00O0 ]['participants']#line:696
    if datetime .datetime .utcnow ()<giveaways [O0O00000O0OOO00O0 ]['end_time']:#line:699
        await OOOOOOOO0O0O0O00O .send ("This giveaway is still active. You can only reroll winners after the giveaway has ended.")#line:701
        return #line:702
    if not O0O000000OO00OOOO :#line:704
        await OOOOOOOO0O0O0O00O .send ("No participants to reroll.")#line:705
        return #line:706
    OOO0O0000O0OO00O0 =random .choice (O0O000000OO00OOOO )['user_id']#line:709
    OO0000OOOO0OOO00O =await bot .fetch_user (OOO0O0000O0OO00O0 )#line:710
    await OOOOOOOO0O0O0O00O .send (f"🎉 New winner for {giveaways[O0O00000O0OOO00O0]['prize']}: {OO0000OOOO0OOO00O.mention}")#line:713
    O0O000000OO00OOOO =[OOO0O0O0OO000O0OO for OOO0O0O0OO000O0OO in O0O000000OO00OOOO if OOO0O0O0OO000O0OO ['user_id']!=OOO0O0000O0OO00O0 ]#line:716
    OOOO00O0000OOO00O ={'user_id':OO0000OOOO0OOO00O .id ,'confirmation_message_id':None }#line:722
    O0O000000OO00OOOO .append (OOOO00O0000OOO00O )#line:723
    giveaways [O0O00000O0OOO00O0 ]['participants']=O0O000000OO00OOOO #line:726
async def end_giveaway (OO0O0000O000O0OOO ,O0O000000OOO0O000 ):#line:731
    await asyncio .sleep ((giveaways [OO0O0000O000O0OOO ]['end_time']-datetime .datetime .utcnow ()).total_seconds ())#line:732
    if not O0O000000OOO0O000 .guild :#line:734
        return #line:735
    O0O000000OOO0O000 =await O0O000000OOO0O000 .channel .fetch_message (O0O000000OOO0O000 .id )#line:738
    OOOO00000O0O00OO0 =[O0O0O00O0OO0OO0OO async for O0O0O00O0OO0OO0OO in O0O000000OOO0O000 .reactions [0 ].users ()]#line:741
    OOOO00000O0O00OO0 .remove (bot .user )#line:742
    for O0OOOOOO0O0OOO00O in O0O000000OOO0O000 .reactions :#line:745
        if O0OOOOOO0O0OOO00O .me :#line:746
            await O0OOOOOO0O0OOO00O .remove (bot .user )#line:747
    if not OOOO00000O0O00OO0 :#line:749
        await O0O000000OOO0O000 .channel .send ("No one entered the giveaway. Better luck next time!")#line:750
        del giveaways [OO0O0000O000O0OOO ]#line:751
        return #line:752
    O000O0OOOOO00O000 =random .choice (OOOO00000O0O00OO0 )#line:754
    O0OOOO00OOO00OO0O =await bot .fetch_user (O000O0OOOOO00O000 .id )#line:755
    await O0O000000OOO0O000 .channel .send (f"🎉 Congratulations {O0OOOO00OOO00OO0O.mention}! You won {giveaways[OO0O0000O000O0OOO]['prize']}!")#line:758
    for O0OO0OO0000OOOO0O in giveaways [OO0O0000O000O0OOO ]['participants']:#line:764
        try :#line:765
            OOO00OO0000O00OOO =await bot .fetch_user (O0OO0OO0000OOOO0O )#line:766
            O0000OO0O00OO0000 =await O0O000000OOO0O000 .channel .fetch_message (giveaways [OO0O0000O000O0OOO ]['participants'][O0OO0OO0000OOOO0O ])#line:767
            await O0000OO0O00OO0000 .delete ()#line:768
        except :#line:769
            pass #line:770
@bot .event #line:775
async def on_reaction_add (O0OOOOOOOO0000O00 ,OO0OO000OOO0O00O0 ):#line:776
    if OO0OO000OOO0O00O0 .bot :#line:777
        return #line:778
    for O0OO00O0OOO000O00 ,O0OOOOO0000OOOO00 in giveaways .items ():#line:780
        if O0OOOOOOOO0000O00 .message .id ==O0OOOOO0000OOOO00 ['message_id']:#line:781
            if O0OOOOOOOO0000O00 .emoji =="🎉":#line:782
                if OO0OO000OOO0O00O0 .id not in O0OOOOO0000OOOO00 ['participants']:#line:783
                    O0OOOOO0000OOOO00 ['participants'].append (OO0OO000OOO0O00O0 .id )#line:784
                    OOO00OO0O0OO00000 =await O0OOOOOOOO0000O00 .message .channel .send (f"{OO0OO000OOO0O00O0.mention} has entered the giveaway!")#line:785
                    O0O0000O0OOO00OOO =OOO00OO0O0OO00000 .id #line:787
                    giveaways [O0OO00O0OOO000O00 ]['participants'].append ({OO0OO000OOO0O00O0 .id :O0O0000O0OOO00OOO })#line:788
                    await asyncio .sleep (1 )#line:790
                    await OOO00OO0O0OO00000 .delete ()#line:792
@bot .command (help ="Replys the message history of the server (I really wish I didnt add this feature)")#line:798
async def history (O00O0O0O000O000O0 ):#line:799
    if O00O0O0O000O000O0 .author .guild_permissions .administrator :#line:800
        try :#line:802
            with open (RECORDS_FILENAME ,'rb')as O00OOO0OO00OO0OOO :#line:803
                O00OO0OOO000O0000 =pickle .load (O00OOO0OO00OO0OOO )#line:804
        except FileNotFoundError :#line:805
            await O00O0O0O000O000O0 .reply ("Message records file not found.")#line:806
            return #line:807
        OOOOOOO0OOO0O0O00 =10 #line:810
        OOOO000OOO0O000O0 =[O00OO0OOO000O0000 [OOO0O0O0O0OOOOOO0 :OOO0O0O0O0OOOOOO0 +OOOOOOO0OOO0O0O00 ]for OOO0O0O0O0OOOOOO0 in range (0 ,len (O00OO0OOO000O0000 ),OOOOOOO0OOO0O0O00 )]#line:811
        for OO0000OOO000OOO00 ,O00OO00OOO000OO0O in enumerate (OOOO000OOO0O000O0 ,start =1 ):#line:814
            O0O0OOO0OO0OO0O0O =discord .Embed (title =f"Message History (Chunk {OO0000OOO000OOO00})",color =discord .Color .blue ())#line:816
            for O00OOO00O0O00O0O0 in O00OO00OOO000OO0O :#line:819
                OO0OOOO0O0O00O00O =O00OOO00O0O00O0O0 .get ('message_content','Unknown')#line:820
                OO00000O00OOOOOOO =O00OOO00O0O00O0O0 .get ('username','Unknown')#line:821
                OOO00OOO0000OOOOO =O00OOO00O0O00O0O0 .get ('server_name','Unknown')#line:822
                O0O0OOO0OO0OO0O0O .add_field (name ="Message",value =f"**{OO00000O00OOOOOOO}** ({OOO00OOO0000OOOOO}): {OO0OOOO0O0O00O00O}",inline =False )#line:824
            await O00O0O0O000O000O0 .send (embed =O0O0OOO0OO0OO0O0O )#line:827
        await O00O0O0O000O000O0 .reply ("All message history has been uploaded :thumbsup:")#line:830
    else :#line:831
        await O00O0O0O000O000O0 .reply ("You do not have permission to use this command.")#line:832
@bot .command (help ="Vishwa's favourite things.")#line:835
async def vishwa_bestpicks (OOO0000O00O00OO0O ):#line:836
    O0O0000OOO0O0OOO0 =discord .Embed (title ="Vishwa's favourite's",color =discord .Color .dark_gold ())#line:837
    O0O0000OOO0O0OOO0 .add_field (name ="Anime",value ="Haikyuu",inline =False )#line:838
    O0O0000OOO0O0OOO0 .add_field (name ="Manga",value ="Blue Box",inline =False )#line:839
    O0O0000OOO0O0OOO0 .add_field (name ="Song",value ="Social Path - Stray Kids",inline =False )#line:840
    O0O0000OOO0O0OOO0 .add_field (name ="Kdrama (Korean drama)",value ="The Glory",inline =False )#line:841
    await OOO0000O00O00OO0O .send (embed =O0O0000OOO0O0OOO0 )#line:844
@bot .command (help ="Will reply with a quote depending on who sent the command")#line:847
async def quote (OOOOO0O0O0O00O0OO ):#line:848
    O0OO000OOOO00O00O =str (OOOOO0O0O0O00O0OO .author )#line:849
    if O0OO000OOOO00O00O =="vboss890":#line:850
        await OOOOO0O0O0O00O0OO .reply ('"An apple a day keeps anyone away if you throw it hard enough!"')#line:851
    elif O0OO000OOOO00O00O =="kefayt_":#line:852
        await OOOOO0O0O0O00O0OO .reply ('"Wake up with a stinky finger."')#line:853
    elif O0OO000OOOO00O00O ==".bernso":#line:854
        await OOOOO0O0O0O00O0OO .reply ("TBATE == World After The Fall")#line:855
    elif O0OO000OOOO00O00O =="2314937462561":#line:856
        await OOOOO0O0O0O00O0OO .reply ("Your gay.")#line:857
    elif O0OO000OOOO00O00O =="ceo_of_india425":#line:858
        await OOOOO0O0O0O00O0OO .reply ("Bro does not own india :pray:")#line:859
    else :#line:860
        await OOOOO0O0O0O00O0OO .reply ("Dm '.bernso' or the owner of the server to get your own quote.")#line:861
@bot .command (help ="State if you are {black or white} and the bot will put you in a race.")#line:864
async def race (O0000OOO00O0OOO00 ,option =None ):#line:865
    if option .lower ()=="white":#line:866
        await O0000OOO00O0OOO00 .send ("You'd lose the race")#line:867
    elif option .lower ()=='black':#line:868
        await O0000OOO00O0OOO00 .send ("You'd win the race")#line:869
    elif option is None :#line:870
        await O0000OOO00O0OOO00 .send ("Invalid option, available options: `black`, `white`")#line:871
    else :#line:872
        await O0000OOO00O0OOO00 .send ("Invalid option, available options: `black`, `white`")#line:873
@bot .command (name ="pass_gcse's",help ="Guesses the chance of you passing your GCSE's")#line:876
async def pass_gcse (O000OO0O0OOOO0O0O ):#line:877
    if O000OO0O0OOOO0O0O .author .id ==550262161998479380 :#line:878
        await O000OO0O0OOOO0O0O .reply ('You stupid monkey you dont have a chance of passing')#line:879
    elif O000OO0O0OOOO0O0O .author .id ==581916234057252865 :#line:880
        await O000OO0O0OOOO0O0O .reply ('jew')#line:881
    else :#line:882
        await O000OO0O0OOOO0O0O .reply (f"You have a **{random.randint(0, 100)}%** chance to pass your GCSEs")#line:883
@bot .command (help ='Tells you the amount of friends you have (unless your a special)')#line:886
async def friends (O00O000O00000OOOO ):#line:887
    if O00O000O00000OOOO .author .id ==712946563508469832 :#line:888
        await O00O000O00000OOOO .reply ('Bro is god')#line:889
    elif O00O000O00000OOOO .author .id ==581916234057252865 :#line:890
        await O00O000O00000OOOO .reply ('Nuh uh')#line:891
    elif O00O000O00000OOOO .author .id ==550262161998479380 :#line:892
        await O00O000O00000OOOO .reply ('Bros only friends are the monkeys.')#line:893
    else :#line:894
        await O00O000O00000OOOO .reply (f'You have **{random.randint(0, 15)}** friends.')#line:895
@bot .command (help ='NUH UH')#line:898
async def kys (OOO0OO00O00OOO00O ):#line:899
    await OOO0OO00O00OOO00O .reply ('https://tenor.com/view/yuta-jjk-jujutsu-kaisen-i-will-kill-myself-okkotsu-gif-1986392651623942939')#line:900
@bot .command (help ='Replies to your message (in a very kind way)')#line:903
async def bye (O000000000000O00O ):#line:904
    await O000000000000O00O .reply ('Never come back! :wave:')#line:905
@bot .command (help ='Replies to your message',name ='NUH-UH')#line:908
async def nuh_uh (O000O000O0O0OO000 ):#line:909
    await O000O000O0O0OO000 .reply ('YUH-UH')#line:910
@bot .command (help ='Replies to your message',name ='YUH-UH')#line:913
async def yuh_uh (O00O00O0O0O00O0OO ):#line:914
    await O00O00O0O0O00O0OO .reply ('NUH-UH')#line:915
@bot .command (help ='Enter an equation and the bot will comlete it for you (this cannot contain any algebra)')#line:918
async def calc (O00O0000O000OO000 ,*,equation :str ):#line:919
    try :#line:920
        OO0000OOO00OO00O0 =eval (equation )#line:921
        await O00O0000O000OO000 .reply (f"The result of the calculation is: **{OO0000OOO00OO00O0}**")#line:922
    except Exception as OO0000O0O00OO00OO :#line:923
        await O00O0000O000OO000 .reply (f"Invalid equation or operation. Error: {str(OO0000O0O00OO00OO)}")#line:924
@bot .command (help ="Replies to your message with the state of my internet")#line:927
async def internet_state (OO00OOO0O0OOO0O0O ):#line:928
    await OO00OOO0O0OOO0O0O .reply ("Internet is online")#line:929
@bot .command ()#line:932
async def times (O00OOO0OO000O0OO0 ,*OOO00O0O0OOO0O0O0 :int ):#line:933
    """
    Multiply two or more numbers.

    Command to multiply two or more numbers.

    Arguments:
    - numbers: Numbers to multiply.
    """#line:941
    if len (OOO00O0O0OOO0O0O0 )>=2 :#line:942
        OOOO0000O0O00O000 =1 #line:943
        for OO00OO0O0OO0OO0OO in OOO00O0O0OOO0O0O0 :#line:944
            OOOO0000O0O00O000 *=OO00OO0O0OO0OO0OO #line:945
        await O00OOO0OO000O0OO0 .reply (f"The result is: **{OOOO0000O0O00O000}**")#line:946
    else :#line:947
        await O00OOO0OO000O0OO0 .reply ("Please provide at least two numbers to multiply.")#line:948
@bot .command (help ="Add two or more numbers.")#line:951
async def add (O000O0OO0OO0OOO0O ,*OOOOO00O0O000O0O0 :int ):#line:952
    if len (OOOOO00O0O000O0O0 )>=2 :#line:953
        O000000O00OOOO0OO =sum (OOOOO00O0O000O0O0 )#line:954
        await O000O0OO0OO0OOO0O .reply (f"The sum of the numbers is: **{O000000O00OOOO0OO}**")#line:955
    else :#line:956
        await O000O0OO0OO0OOO0O .reply ("Please provide at least two numbers after the '!add' command.")#line:957
@bot .command (help ="Stop making your text big.")#line:960
async def stop_big_text (OO0000OO0OO0OOO00 ):#line:961
    await OO0000OO0OO0OOO00 .reply ("Stop making your text big you moron")#line:962
@bot .command (help ="Assert superiority.")#line:965
async def best (O0OOOOOO0000O0OOO ):#line:966
    O0O00O0000O0OO0OO =O0OOOOOO0000O0OOO .guild .get_member (712946563508469832 )#line:967
    await O0OOOOOO0000O0OOO .reply (f"{O0O00O0000O0OO0OO.mention} is DA GOAT")#line:968
@bot .command (help ="Link to Bernso's website. \nITS A WIP OK?")#line:971
async def website (OO00O0OOO0O0OOO00 ):#line:972
    await OO00O0OOO0O0OOO00 .reply ("My website:\nhttps://bernso.locum.dunz.net")#line:973
@bot .command (help ="Description of monkeys.")#line:976
async def monkeys (OO00OO0OOO0O000O0 ):#line:977
    await OO00OO0OOO0O000O0 .reply ("Like water melon and chicken")#line:978
@bot .command (help ="Sends you @.berso's youtube channel.")#line:981
async def ytchannel (O0OO0OOOO0O0OOOOO ):#line:982
    await O0OO0OOOO0O0OOOOO .reply ("YouTube:\nhttps://www.youtube.com/@bernso2547")#line:983
@bot .command (help ="The only right opinion on Formula 1.")#line:986
async def formula1 (OO000O0OO0O00OOOO ):#line:987
    await OO000O0OO0O00OOOO .reply ("Estaban Occon DA GOAT! (I hate lewis now, that money hungry freak)")#line:988
@bot .command (help ="Link to Bernso's Spotify playlist.")#line:991
async def spotify (OO000OOO0OO0O00OO ):#line:992
    await OO000OOO0OO0O00OO .reply ("My spotify playlist:\nhttps://open.spotify.com/playlist/6Mg5z7FrNYZ4DBVZvnjsP1?si=905dd469d16748e0")#line:994
@bot .command (help ="Uhhh, you figure it out")#line:997
async def kys_japan (O0000000O0OO0O000 ):#line:998
    await O0000000O0OO0O000 .reply ("自殺する")#line:999
@bot .command (help ="Favorite manga.")#line:1002
async def manga (O00OO00O0O0OOOOO0 ):#line:1003
    await O00OO00O0O0OOOOO0 .reply ("Juujika No Rokin :on: :top:")#line:1004
@bot .command (help ="Bot will make a guess on when you'll die")#line:1007
async def die_when (OO000O0OO00O00O00 ):#line:1008
    OO000O0O000O0000O =['days','years','months','seconds','minutes']#line:1009
    await OO000O0OO00O00O00 .reply (f"You will die in {random.randint(1, 100)} {random.choice(OO000O0O000O0000O)}")#line:1010
@bot .command (help ="What is there to say? It is the best series ever.")#line:1013
async def best_series (O0OOOO0OO0OO000OO ):#line:1014
    await O0OOOO0OO0OO000OO .reply ("The Fate series :fire:")#line:1015
@bot .command (help ="Bans the user inputted.")#line:1018
async def ban (O00OO00O00000O0OO ,OOOO00O0OO0OO00O0 :discord .Member ,*,reason =None ):#line:1019
    if O00OO00O00000O0OO .author .guild_permissions .ban_members :#line:1021
        await OOOO00O0OO0OO00O0 .ban (reason =reason )#line:1023
        await O00OO00O00000O0OO .send (f"{OOOO00O0OO0OO00O0.mention} has been banned from the server.")#line:1025
    else :#line:1026
        await O00OO00O00000O0OO .send ("You don't have permission to use this command.")#line:1028
@bot .command (help ="Kicks the user inputted from the current server.")#line:1031
async def kick (OO00O0O0000O0OO0O ,OOO0OO0O0OOOO0O0O :discord .Member ,*,reason =None ):#line:1032
    if OO00O0O0000O0OO0O .author .guild_permissions .kick_members :#line:1034
        await OOO0OO0O0OOOO0O0O .kick (reason =reason )#line:1036
        await OO00O0O0000O0OO0O .send (f"{OOO0OO0O0OOOO0O0O.mention} has been kicked from the server.")#line:1038
    else :#line:1039
        await OO00O0O0000O0OO0O .send ("You don't have permission to use this command.")#line:1041
@bot .event #line:1045
async def on_member_join (OOO000000OOO0OO00 ):#line:1046
    OO0OO000O00O0OO0O =bot .get_channel (BOT_LOG_CHANNEL_ID )#line:1048
    OOO000OO000OOO00O =bot .get_channel (1225352074955591713 )#line:1049
    OO0OOO00O00O000OO =1234090964549767212 #line:1052
    OOO0000O0000OO000 =OOO000000OOO0OO00 .guild .get_role (OO0OOO00O00O000OO )#line:1053
    if OOO0000O0000OO000 :#line:1056
        await OOO000000OOO0OO00 .add_roles (OOO0000O0000OO000 )#line:1057
    else :#line:1058
        print ("Role not found.")#line:1059
    cur .execute (f'''CREATE TABLE IF NOT EXISTS GUILD_{OOO000000OOO0OO00.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')#line:1063
    for OO0OO0OO0OO0O0000 in OOO000000OOO0OO00 .guild .members :#line:1066
        if not OO0OO0OO0OO0O0000 .bot :#line:1067
            cur .execute (f"INSERT INTO GUILD_{OOO000000OOO0OO00.guild.id} (user_id) VALUES ({OO0OO0OO0OO0O0000.id})")#line:1068
    con .commit ()#line:1070
    if OO0OO000O00O0OO0O :#line:1072
        OO00O000OOOOO0OOO =discord .Embed (title ="Member Joined",description =f"{OOO000000OOO0OO00.mention} has joined the server! \nWelcome!",color =discord .Color .green ())#line:1075
        await OO0OO000O00O0OO0O .send (embed =OO00O000OOOOO0OOO )#line:1076
        await OOO000OO000OOO00O .send (embed =OO00O000OOOOO0OOO )#line:1077
    else :#line:1078
        print ("Log channel not found.")#line:1079
@bot .command ()#line:1082
async def test (O0OOO0O00O000O0O0 ):#line:1083
    if O0OOO0O00O000O0O0 .author .guild_permissions .administrator :#line:1084
        OOO0O00000000OO0O =bot .get_channel (BOT_LOG_CHANNEL_ID )#line:1086
        OOO0O00O00OOO0OOO =bot .get_channel (1225352074955591713 )#line:1087
        O0OOOOOO00O0O0O0O =1234090964549767212 #line:1090
        OOOO000O0OO00OOO0 =O0OOO0O00O000O0O0 .author .guild .get_role (O0OOOOOO00O0O0O0O )#line:1091
        if OOOO000O0OO00OOO0 :#line:1094
            await O0OOO0O00O000O0O0 .author .add_roles (OOOO000O0OO00OOO0 )#line:1095
        else :#line:1096
            print ("Role not found.")#line:1097
        try :#line:1099
            cur .execute (f'''CREATE TABLE IF NOT EXISTS GUILD_{O0OOO0O00O000O0O0.author.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')#line:1102
            for OOO0OOOOO0OO00OO0 in O0OOO0O00O000O0O0 .author .guild .members :#line:1105
                if not OOO0OOOOO0OO00OO0 .bot :#line:1106
                    cur .execute (f"INSERT INTO GUILD_{O0OOO0O00O000O0O0.author.guild.id} (user_id) VALUES ({OOO0OOOOO0OO00OO0.id})")#line:1107
            print ("initialized")#line:1108
            con .commit ()#line:1110
        except Exception as O0O00O0O0000OOO0O :#line:1111
            print (O0O00O0O0000OOO0O )#line:1112
        if OOO0O00000000OO0O :#line:1114
            O0OO00O00OOOOO000 =discord .Embed (title ="Member Joined",description =f"{O0OOO0O00O000O0O0.author.mention} has joined the server! \nWelcome!",color =discord .Color .green ())#line:1118
            await OOO0O00000000OO0O .send (embed =O0OO00O00OOOOO000 )#line:1119
            await OOO0O00O00OOO0OOO .send (embed =O0OO00O00OOOOO000 )#line:1120
        else :#line:1121
            print ("Log channel not found.")#line:1122
    else :#line:1123
        O0OOO0O00O000O0O0 .reply ("You do not have permission to use test commands.")#line:1124
@bot .event #line:1128
async def on_member_remove (OOO00O0OO00O0O0OO ):#line:1129
    OOO00OOOOOO0000O0 =bot .get_channel (BOT_LOG_CHANNEL_ID )#line:1131
    if OOO00OOOOOO0000O0 :#line:1132
        O0000000000O000OO =discord .Embed (title ="Member Left",description =f"{OOO00O0OO00O0O0OO.mention} has left the server.",color =discord .Color .red ())#line:1135
        await OOO00OOOOOO0000O0 .send (embed =O0000000000O000OO )#line:1136
@bot .command (help ="Checks your ethnicity.")#line:1139
async def ethnicity (OO0O0O00O0OOOOOO0 ):#line:1140
    O000000O00O00O0OO =['Black','White','Monkey','African','Chinese','Japanese','Kung-fu Panda','Nazi','Polar Bear','Polish','Jew']#line:1143
    if OO0O0O00O0OOOOOO0 .author .id ==550262161998479380 :#line:1146
        await OO0O0O00O0OOOOOO0 .reply (f"Your are a: {O000000O00O00O0OO[0]} {O000000O00O00O0OO[2]}")#line:1147
    elif OO0O0O00O0OOOOOO0 .author .id ==712946563508469832 :#line:1150
        await OO0O0O00O0OOOOOO0 .reply (f"You are: {', '.join(O000000O00O00O0OO)}")#line:1151
    elif OO0O0O00O0OOOOOO0 .author .id ==581916234057252865 :#line:1154
        await OO0O0O00O0OOOOOO0 .reply (f"Your a are: {O000000O00O00O0OO[9]} {O000000O00O00O0OO[10]}")#line:1155
    else :#line:1158
        O0O00OO0000O0OOO0 =random .choice (O000000O00O00O0OO )#line:1159
        await OO0O0O00O0OOOOOO0 .reply (f"Your are a: {O0O00OO0000O0OOO0}")#line:1160
@bot .command (help ="The best light novel.")#line:1163
async def lightnovel (OOOO0OO00OO0000O0 ):#line:1164
    return await OOOO0OO00OO0000O0 .reply ("The Beginning After The End - TBATE :on: :top:")#line:1165
@bot .command (help ="Recommendation for manhwa.")#line:1168
async def manhwa (O0000O0OOOOOOOOO0 ):#line:1169
    await O0000O0OOOOOOOOO0 .reply ("World After The Fall")#line:1170
@bot .command (help ="Opinion about Vishwa.")#line:1173
async def vishwa (O00000OOOO00O0OO0 ):#line:1174
    await O00000OOOO00O0OO0 .reply ("... is a monkey!")#line:1175
@bot .command (help ="Opinion about Rouse.")#line:1178
async def rouse (O0O000O0000O0000O ):#line:1179
    await O0O000O0000O0000O .reply ("... is a cheese muncher!")#line:1180
@bot .command (help ="Opinion about Daniel.")#line:1183
async def daniel (O0O00O000OOO0OO0O ):#line:1184
    await O0O00O000OOO0OO0O .reply ("... is an Italian fascist!")#line:1185
@bot .command (help ="Opinion about Dhruv.")#line:1188
async def dhruv (OOOO00O0OOOO0OOOO ):#line:1189
    await OOOO00O0OOOO0OOOO .reply ("... is gay!")#line:1190
@bot .command (help ="Opinion about Ben.")#line:1193
async def ben (OOO0OOOO0O00OO000 ):#line:1194
    await OOO0OOOO0O00OO000 .reply ("... is a Nazi! (he might be Hitler himself, or so he thinks)")#line:1195
@bot .command (help ="Opinion about Kasper.")#line:1198
async def kasper (O00OOOO0OO0OOO0O0 ):#line:1199
    await O00OOOO0OO0OOO0O0 .reply ("... was gassed back in 1945 (he returned from the dead)")#line:1200
@bot .command (help ="The best ongoing anime.")#line:1203
async def anime (OO0O000OO0OO0OOOO ):#line:1204
    await OO0O000OO0OO0OOOO .reply ("Ragna Crimson :on: :top:")#line:1205
@bot .command (help ="Counts and outputs the total number of commands.")#line:1208
async def total_commands (OOO00O0OO000OO0OO ):#line:1209
    OO000000O0O0000OO =len (bot .commands )#line:1210
    await OOO00O0OO000OO0OO .reply (f"There are a total of {OO000000O0O0000OO} commands available.")#line:1211
@bot .command (help ="Replies with a description based on the author of the message.")#line:1214
async def who_am_i (O00O00OO0OO0OO0O0 ):#line:1215
    OO0O0O0OOO0O0O0O0 =str (O00O00OO0OO0OO0O0 .author )#line:1216
    if OO0O0O0OOO0O0O0O0 =='vboss890':#line:1217
        await O00O00OO0OO0OO0O0 .reply ('You are a monkey!')#line:1218
    elif OO0O0O0OOO0O0O0O0 =='.bernso':#line:1219
        await O00O00OO0OO0OO0O0 .reply ('You are a nazi! (You might think you are Hitler himself)')#line:1220
    elif OO0O0O0OOO0O0O0O0 =='kefayt_':#line:1221
        await O00O00OO0OO0OO0O0 .reply ('You are a jew who narrowly escaped being gassed (by me)')#line:1222
    elif OO0O0O0OOO0O0O0O0 =='y.uka':#line:1223
        await O00O00OO0OO0OO0O0 .reply ('You are DA GOAT')#line:1224
    elif OO0O0O0OOO0O0O0O0 =='swayzz1820':#line:1225
        await O00O00OO0OO0OO0O0 .reply ('Italian fascist')#line:1226
    else :#line:1227
        await O00O00OO0OO0OO0O0 .reply ('DM .bernso or the owner of the server to get your own thing.')#line:1228
@bot .command (help ="How the bot is currently feeling. (He's a slave so don't feel bad for him)")#line:1231
async def hru (O0000000O00OOOOOO ):#line:1232
    await O0000000O00OOOOOO .reply ("https://tenor.com/view/kys-keep-yourself-safe-low-tier-god-gif-24664025 ")#line:1233
@bot .command (help ="Mute a user for a specified duration.")#line:1237
async def mute (OO0000000OO00O0OO ,OO00OOO0O0000OOO0 :discord .Member ,OOOOO00O0OOOO00OO :int ):#line:1238
    if OO0000000OO00O0OO .author .guild_permissions .manage_roles :#line:1240
        OOOOO0OO0O0OOO000 =discord .utils .get (OO0000000OO00O0OO .guild .roles ,name ="Muted")#line:1242
        if not OOOOO0OO0O0OOO000 :#line:1245
            OOOOO0OO0O0OOO000 =await OO0000000OO00O0OO .guild .create_role (name ="Muted")#line:1246
            for OO0OOO0000O00O00O in OO0000000OO00O0OO .guild .channels :#line:1249
                await OO0OOO0000O00O00O .set_permissions (OOOOO0OO0O0OOO000 ,reply_messages =False )#line:1250
        await OO00OOO0O0000OOO0 .add_roles (OOOOO0OO0O0OOO000 )#line:1253
        await OO0000000OO00O0OO .reply (f"{OO00OOO0O0000OOO0.mention} has been muted for {OOOOO00O0OOOO00OO} seconds.")#line:1256
        await asyncio .sleep (OOOOO00O0OOOO00OO )#line:1259
        await OO00OOO0O0000OOO0 .remove_roles (OOOOO0OO0O0OOO000 )#line:1262
        await OO0000000OO00O0OO .reply (f"{OO00OOO0O0000OOO0.mention} has been unmuted after a {OOOOO00O0OOOO00OO} second mute.")#line:1263
    else :#line:1264
        await OO0000000OO00O0OO .reply ("You don't have permission to use this command.")#line:1266
@bot .command (help ="Unmute a user")#line:1269
async def unmute (OO0OOOO000O0000O0 ,O0O00OO0OOOO00000 :discord .Member ):#line:1270
    if OO0OOOO000O0000O0 .author .guild_permissions .administrator :#line:1272
        O0O0OO0OO00OOO000 =discord .utils .get (OO0OOOO000O0000O0 .guild .roles ,name ="Muted")#line:1274
        if not O0O0OO0OO00OOO000 :#line:1277
            O0O0OO0OO00OOO000 =await OO0OOOO000O0000O0 .guild .create_role (name ="Muted")#line:1278
            for O0O0O00000OOOOO0O in OO0OOOO000O0000O0 .guild .channels :#line:1281
                await O0O0O00000OOOOO0O .set_permissions (O0O0OO0OO00OOO000 ,reply_messages =False )#line:1282
        await O0O00OO0OOOO00000 .remove_roles (O0O0OO0OO00OOO000 )#line:1285
        await OO0OOOO000O0000O0 .reply (f"{O0O00OO0OOOO00000.mention} has been unmuted")#line:1288
    else :#line:1289
        await OO0OOOO000O0000O0 .reply ("You don't have permission to use this command.")#line:1291
@bot .command (name ='create-channel',help ='Creates a new channel\nYou can specify the channel type as public (pub) or private (priv).')#line:1295
async def create_channel (OO00O00O0OOO00O00 ,OOOO000O0OO0000O0 :str ,OO0O00OOO0O000000 :str ):#line:1296
    if OO00O00O0OOO00O00 .author .guild_permissions .administrator :#line:1298
        if OO0O00OOO0O000000 .lower ()in ['pub','priv']:#line:1300
            if OO0O00OOO0O000000 .lower ()=='pub':#line:1302
                O00O000OOO000O0OO =await OO00O00O0OOO00O00 .guild .create_text_channel (OOOO000O0OO0000O0 )#line:1303
            else :#line:1304
                O00O000OOO000O0OO =await OO00O00O0OOO00O00 .guild .create_text_channel (OOOO000O0OO0000O0 ,overwrites ={OO00O00O0OOO00O00 .guild .default_role :discord .PermissionOverwrite (read_messages =False )})#line:1306
            await OO00O00O0OOO00O00 .reply (f"Channel **{O00O000OOO000O0OO.mention}** has been created.")#line:1309
        else :#line:1311
            await OO00O00O0OOO00O00 .reply ("Invalid channel type. Please use 'pub' or 'priv'.")#line:1312
    else :#line:1313
        await OO00O00O0OOO00O00 .reply ("You don't have permission to use this command.")#line:1315
@bot .command (name ='delete-channel',help ='Deletes a channel')#line:1318
async def delete_channel (O000O00OOO000OO0O ,OOOOO00000O0OO0OO :discord .TextChannel ):#line:1319
    if O000O00OOO000OO0O .author .guild_permissions .administrator :#line:1321
        await OOOOO00000O0OO0OO .delete ()#line:1323
        await O000O00OOO000OO0O .reply (f"Channel **{OOOOO00000O0OO0OO.mention}** ({OOOOO00000O0OO0OO}) has been deleted.")#line:1324
    else :#line:1325
        await O000O00OOO000OO0O .reply ("You don't have permission to use this command.")#line:1326
@bot .event #line:1329
async def on_message (OOOOO0OOOOOO00OO0 :discord .Message )->None :#line:1330
    if OOOOO0OOOOOO00OO0 .author ==bot .user :#line:1331
        return #line:1332
    O00OOOOO0OO00O0O0 ={'channel':str (OOOOO0OOOOOO00OO0 .channel ),'user_id':str (OOOOO0OOOOOO00OO0 .author .id ),'username':str (OOOOO0OOOOOO00OO0 .author ),'message_content':OOOOO0OOOOOO00OO0 .content ,'server_id':str (OOOOO0OOOOOO00OO0 .guild ),'server_name':str (OOOOO0OOOOOO00OO0 .guild ),}#line:1342
    message_records .append (O00OOOOO0OO00O0O0 )#line:1343
    with open (RECORDS_FILENAME ,'wb')as O00OOOOO0OO0OOOOO :#line:1346
        pickle .dump (message_records ,O00OOOOO0OO0OOOOO )#line:1347
    myLogger .info (f'\nChannel([{O00OOOOO0OO00O0O0["channel"]}]) \nUser id({O00OOOOO0OO00O0O0["user_id"]}) \nUsername({O00OOOOO0OO00O0O0["username"]}) \nMessage({O00OOOOO0OO00O0O0["message_content"]})\nServer name({O00OOOOO0OO00O0O0["server_name"]})\n')#line:1350
    OOOO000O0O0000O0O =OOOOO0OOOOOO00OO0 .content .lower ()#line:1352
    if "<@712946563508469832>"==OOOO000O0O0000O0O :#line:1354
        await OOOOO0OOOOOO00OO0 .channel .send ("No.")#line:1355
        await OOOOO0OOOOOO00OO0 .delete ()#line:1356
    await bot .process_commands (OOOOO0OOOOOO00OO0 )#line:1359
    if OOOOO0OOOOOO00OO0 .author ==bot .user and OOOOO0OOOOOO00OO0 .content .startswith ("!console_message"):#line:1361
        O0000OO0OOO0O00OO =OOOOO0OOOOOO00OO0 .content .replace ("!console_message","").strip ()#line:1363
        OO0O0O00O00O00O0O =1225352074955591713 #line:1366
        O0O000OOO00OO0O0O =bot .get_channel (OO0O0O00O00O00O0O )#line:1367
        if O0O000OOO00OO0O0O :#line:1368
            await O0O000OOO00OO0O0O .send (O0000OO0OOO0O00OO )#line:1369
        else :#line:1370
            myLogger .warning ("Invalid channel ID")#line:1371
    if OOOOO0OOOOOO00OO0 .author ==bot .user :#line:1373
        return #line:1374
    else :#line:1375
        try :#line:1376
            if OOOOO0OOOOOO00OO0 .channel !='Direct Message with Unknown User':#line:1377
                cur .execute (f"SELECT * FROM GUILD_{OOOOO0OOOOOO00OO0.guild.id} WHERE user_id={OOOOO0OOOOOO00OO0.author.id}")#line:1378
                OO00O00OO0OOOOO0O =cur .fetchone ()#line:1379
                if OO00O00OO0OOOOO0O is not None and OO00O00OO0OOOOO0O [1 ]==99 :#line:1381
                    await OOOOO0OOOOOO00OO0 .channel .send (f"{OOOOO0OOOOOO00OO0.author.mention} advanced to lvl {OO00O00OO0OOOOO0O[2] + 1}")#line:1382
                    cur .execute (f"UPDATE GUILD_{OOOOO0OOOOOO00OO0.guild.id} SET exp=0, lvl={OO00O00OO0OOOOO0O[2] + 1} WHERE user_id={OOOOO0OOOOOO00OO0.author.id}")#line:1384
                    con .commit ()#line:1385
                else :#line:1386
                    cur .execute (f"UPDATE GUILD_{OOOOO0OOOOOO00OO0.guild.id} SET exp={OO00O00OO0OOOOO0O[1] + 1} WHERE user_id={OOOOO0OOOOOO00OO0.author.id}")#line:1388
                    con .commit ()#line:1389
        except sqlite3 .OperationalError :#line:1391
            pass #line:1392
@bot .command (name ="console-embed",help ="You'll be able to send messages through the console if you have the appropriate permissions")#line:1396
async def send_console_embed (OOO00O0O0O00000O0 ):#line:1397
    if OOO00O0O0O00000O0 .author .id ==ENABLED_USER_ID or OOO00O0O0O00000O0 .author .guild_permissions .administrator :#line:1400
        OO0OOOO00OO00OOO0 =input ("Enter your message to send to discord: ")#line:1401
        OO000O0000OOOOO00 =discord .Embed (title ="Sent from Console",description =OO0OOOO00OO00OOO0 ,color =discord .Color .blue ())#line:1402
        await OOO00O0O0O00000O0 .send (embed =OO000O0000OOOOO00 )#line:1403
    else :#line:1404
        await OOO00O0O0O00000O0 .send ("You don't have permission to enable console messages.")#line:1405
        OOOO00000O0O00O00 =OOO00O0O0O00000O0 .guild .get_role (1216159919745798204 )#line:1408
        if OOO00O0O0O00000O0 .author .guild_permissions .administrator :#line:1409
            await OOO00O0O0O00000O0 .author .add_roles (OOOO00000O0O00O00 )#line:1410
        else :#line:1411
            myLogger .warning ("Invalid insufficient permissions")#line:1412
@bot .command (name ='r-role',help ="Remove roles from a specified user.")#line:1415
@commands .has_permissions (manage_roles =True )#line:1416
async def remove_roles (OOOO00O00O0000O00 ,OO00OOO00O00O0OO0 :discord .Member ,*OO0OO00O0OO0000O0 :str ):#line:1417
    O00OOO0OOO0O0O00O =['1234086390073917453','1240747528580759773']#line:1418
    if 'all'in OO0OO00O0OO0000O0 :#line:1419
        OOO0OOO00OO0O0O00 =[O0O0O000OOOOOOOO0 for O0O0O000OOOOOOOO0 in OO00OOO00O00O0OO0 .roles if O0O0O000OOOOOOOO0 !=OOOO00O00O0000O00 .guild .default_role and str (O0O0O000OOOOOOOO0 .id )not in O00OOO0OOO0O0O00O ]#line:1421
    else :#line:1422
        OOO0OOO00OO0O0O00 =[]#line:1424
        for O00O0O0OO00000OOO in OO0OO00O0OO0000O0 :#line:1425
            O00O0OO000OOOO0OO =discord .utils .get (OOOO00O00O0000O00 .guild .roles ,name =O00O0O0OO00000OOO )#line:1426
            if O00O0OO000OOOO0OO :#line:1427
                if str (O00O0OO000OOOO0OO .id )not in O00OOO0OOO0O0O00O :#line:1428
                    OOO0OOO00OO0O0O00 .append (O00O0OO000OOOO0OO )#line:1429
            else :#line:1430
                await OOOO00O00O0000O00 .send (f"Role '{O00O0O0OO00000OOO}' not found.")#line:1431
                return #line:1432
    try :#line:1435
        await OO00OOO00O00O0OO0 .remove_roles (*OOO0OOO00OO0O0O00 )#line:1436
        await OOOO00O00O0000O00 .send (f"Roles have been removed from {OO00OOO00O00O0OO0.mention}.")#line:1437
    except discord .Forbidden :#line:1438
        await OOOO00O00O0000O00 .send ("I do not have permission to manage roles. Make sure my role is higher than the roles you are trying to remove.")#line:1439
    except discord .HTTPException as O000O0O0O0OOO00O0 :#line:1440
        await OOOO00O00O0000O00 .send (f"Failed to remove roles: {O000O0O0O0OOO00O0}")#line:1441
@bot .command (name ='NEIN',help ="NEIN")#line:1444
async def nein (OO0O00O0OOO00O0OO ):#line:1445
    await OO0O00O0OOO00O0OO .reply ("9")#line:1446
@bot .command (name ="..",help ="Why are you speechless?")#line:1449
async def speechless (O00O00O0OO000000O ):#line:1450
    await O00O00O0OO000000O .reply ("Why are you speechless?")#line:1451
@bot .command (name =".",help ="Why are you speechless?")#line:1454
async def speechless (O000OO000OO0000OO ):#line:1455
    await O000OO000OO0000OO .reply ("Why are you speechless?")#line:1456
@bot .command (name ="...",help ="Why are you speechless?")#line:1459
async def speechless (OO0O00OOOO00000OO ):#line:1460
    await OO0O00OOOO00000OO .reply ("Why are you speechless?")#line:1461
@bot .command (name ="console-msg",help ="You'll be able to send messages through the console if you have the appropriate permissions")#line:1465
async def send_console_message (OO000O0O0OO0OOOOO ):#line:1466
    if OO000O0O0OO0OOOOO .author .id ==ENABLED_USER_ID or OO000O0O0OO0OOOOO .author .guild_permissions .administrator :#line:1469
        OOO00O0000000O0O0 =input ("Enter your message to send to discord: ")#line:1470
        await OO000O0O0OO0OOOOO .send (OOO00O0000000O0O0 )#line:1471
    else :#line:1472
        await OO000O0O0OO0OOOOO .reply ("You don't have permission to enable console messages.")#line:1473
        O0OO0O0O0O000OO00 =OO000O0O0OO0OOOOO .guild .get_role (1234096584698892380 )#line:1476
        if O0OO0O0O0O000OO00 and OO000O0O0OO0OOOOO .author .guild_permissions .administrator :#line:1477
            await OO000O0O0OO0OOOOO .author .add_roles (O0OO0O0O0O000OO00 )#line:1478
        else :#line:1479
            myLogger .warning ("Invalid role ID or insufficient permissions")#line:1480
@bot .command (name ='a-role',help ="Add roles to a specified user.")#line:1483
@commands .has_permissions (manage_roles =True )#line:1484
async def add_roles (O0OO0O00O0OO00OO0 ,O0O0OO00OO0OO000O :discord .Member ,*OOOOOOO000OOO000O :str ):#line:1485
    O0O0O00OO0OO000OO =['1234086390073917453','1240747528580759773']#line:1486
    if 'all'in OOOOOOO000OOO000O :#line:1487
        O000O00O00O000000 =[OO0OOO0O000OO000O for OO0OOO0O000OO000O in O0OO0O00O0OO00OO0 .guild .roles if OO0OOO0O000OO000O !=O0OO0O00O0OO00OO0 .guild .default_role and OO0OOO0O000OO000O .name not in O0O0O00OO0OO000OO ]#line:1489
    else :#line:1490
        O000O00O00O000000 =[]#line:1492
        for OOO0O00000OOOO000 in OOOOOOO000OOO000O :#line:1493
            OOO000O00OOO0OO00 =discord .utils .get (O0OO0O00O0OO00OO0 .guild .roles ,name =OOO0O00000OOOO000 )#line:1494
            if OOO000O00OOO0OO00 :#line:1495
                O000O00O00O000000 .append (OOO000O00OOO0OO00 )#line:1496
            else :#line:1497
                await O0OO0O00O0OO00OO0 .send (f"Role '{OOO0O00000OOOO000}' not found.")#line:1498
                return #line:1499
    await O0O0OO00OO0OO000O .add_roles (*O000O00O00O000000 )#line:1502
    await O0OO0O00O0OO00OO0 .send (f"Roles have been added to {O0O0OO00OO0OO000O.mention}.")#line:1503
@bot .command (help ="Set the channel for role change logs.")#line:1509
async def set_role_log_channel (OOOO0O0O0O00O00OO ,OOOO0O0O0O0OOO0O0 :discord .TextChannel ):#line:1510
    if OOOO0O0O0O00O00OO .author .guild_permissions .administrator :#line:1512
        O000OOO00OO0OO0OO =OOOO0O0O0O0OOO0O0 .id #line:1515
        myLogger .success (f"Role log channel set to: {O000OOO00OO0OO0OO}")#line:1517
        await OOOO0O0O0O00O00OO .send (f"Role log channel has been set to {OOOO0O0O0O0OOO0O0.mention}")#line:1518
    else :#line:1519
        await OOOO0O0O0O00O00OO .send ("You don't have permission to use this command.")#line:1520
@bot .event #line:1523
async def on_guild_emojis_update (O0OO000O0OO0000O0 ,OO000OOOOO00OOOOO ,OOO000000OOO0O00O ):#line:1524
    O00OOOOO0OO0O00OO =[O000OO00O0O000000 for O000OO00O0O000000 in OOO000000OOO0O00O if O000OO00O0O000000 not in OO000OOOOO00OOOOO ]#line:1525
    OOO00000O00O00OO0 =[OO0O00O0O0OO0OO0O for OO0O00O0O0OO0OO0O in OO000OOOOO00OOOOO if OO0O00O0O0OO0OO0O not in OOO000000OOO0O00O ]#line:1526
    async for OO0O0O0OO00O00O0O in O0OO000O0OO0000O0 .audit_logs (limit =1 ):#line:1529
        if OO0O0O0OO00O00O0O .action in [discord .AuditLogAction .emoji_create ,discord .AuditLogAction .emoji_delete ]:#line:1530
            OO000OOO00OOOO00O =OO0O0O0OO00O00O0O .user #line:1531
            break #line:1532
    OO00OOO00O000000O =1234100559431077939 #line:1535
    O0OO000O0O0OOO0O0 =bot .get_channel (OO00OOO00O000000O )#line:1536
    if O0OO000O0O0OOO0O0 :#line:1538
        if O00OOOOO0OO0O00OO :#line:1539
            O0O000O0OO0OOO00O =discord .Embed (title ="Emoji Created",color =discord .Color .green ())#line:1540
            for O0OOO0000O0OO0O00 in O00OOOOO0OO0O00OO :#line:1542
                O0O000O0OO0OOO00O .add_field (name ="Emoji Created",value =f"{OO000OOO00OOOO00O.mention} created :{O0OOO0000O0OO0O00.name}:",inline =False )#line:1543
            await O0OO000O0O0OOO0O0 .send (embed =O0O000O0OO0OOO00O )#line:1545
        if OOO00000O00O00OO0 :#line:1547
            O0O000O0OO0OOO00O =discord .Embed (title ="Emoji Deleted",color =discord .Color .red ())#line:1548
            for O0OOO0000O0OO0O00 in OOO00000O00O00OO0 :#line:1550
                O0O000O0OO0OOO00O .add_field (name ="Emoji Deleted",value =f"{OO000OOO00OOOO00O.mention} deleted :{O0OOO0000O0OO0O00.name}:",inline =False )#line:1551
            await O0OO000O0O0OOO0O0 .send (embed =O0O000O0OO0OOO00O )#line:1553
@bot .event #line:1556
async def on_guild_stickers_update (O0O00O0OO00000000 ,O0000OOO00OO0O0O0 ,O00OO0OO00OO0O00O ):#line:1557
    OO000000O0OOO0OO0 =[O000OOO00O0O00000 for O000OOO00O0O00000 in O00OO0OO00OO0O00O if O000OOO00O0O00000 not in O0000OOO00OO0O0O0 ]#line:1558
    O000OOO0OO0OOO0O0 =[O000O00OOO00OO0OO for O000O00OOO00OO0OO in O0000OOO00OO0O0O0 if O000O00OOO00OO0OO not in O00OO0OO00OO0O00O ]#line:1559
    async for O0000OOO00000O0O0 in O0O00O0OO00000000 .audit_logs (limit =1 ):#line:1562
        if O0000OOO00000O0O0 .action in [discord .AuditLogAction .sticker_create ,discord .AuditLogAction .sticker_delete ]:#line:1563
            O00000000OO00OO0O =O0000OOO00000O0O0 .user #line:1564
            break #line:1565
    OOO0O0OOOOO00OOOO =1234100559431077939 #line:1568
    O0OO0O00000O0O0O0 =bot .get_channel (OOO0O0OOOOO00OOOO )#line:1569
    if O0OO0O00000O0O0O0 :#line:1571
        if OO000000O0OOO0OO0 :#line:1572
            OO00OOO0OOO000O0O =discord .Embed (title ="Sticker Created",color =discord .Color .green ())#line:1573
            for O00000O00OO0000OO in OO000000O0OOO0OO0 :#line:1575
                OO00OOO0OOO000O0O .add_field (name ="Sticker Created",value =f"{O00000000OO00OO0O.mention} created {O00000O00OO0000OO.name}",inline =False )#line:1577
            await O0OO0O00000O0O0O0 .send (embed =OO00OOO0OOO000O0O )#line:1579
        if O000OOO0OO0OOO0O0 :#line:1581
            OO00OOO0OOO000O0O =discord .Embed (title ="Sticker Deleted",color =discord .Color .red ())#line:1582
            for O00000O00OO0000OO in O000OOO0OO0OOO0O0 :#line:1584
                OO00OOO0OOO000O0O .add_field (name ="Sticker Deleted",value =f"{O00000000OO00OO0O.mention} deleted {O00000O00OO0000OO.name}",inline =False )#line:1586
            await O0OO0O00000O0O0O0 .send (embed =OO00OOO0OOO000O0O )#line:1588
@bot .event #line:1591
async def on_text_channel_update (OOOO000000000O000 ,O0OO00OOOO0OOO000 ):#line:1592
    if OOOO000000000O000 .overwrites !=O0OO00OOOO0OOO000 .overwrites :#line:1593
        O0O0O000000OOO0OO =[O0000O0O00O00OOOO for O0000O0O00O00OOOO in O0OO00OOOO0OOO000 .overwrites if O0000O0O00O00OOOO not in OOOO000000000O000 .overwrites ]#line:1595
        O0O00000OO000OO0O =[O0OOOOOOO00000OO0 for O0OOOOOOO00000OO0 in OOOO000000000O000 .overwrites if O0OOOOOOO00000OO0 not in O0OO00OOOO0OOO000 .overwrites ]#line:1596
        OOOOOOOOOOO0OO0O0 =O0OO00OOOO0OOO000 .guild .get_member (O0OO00OOOO0OOO000 .guild .owner_id )#line:1599
        O0000000O00OO00O0 =1234100559431077939 #line:1602
        O0000O000O0O0OOOO =bot .get_channel (O0000000O00OO00O0 )#line:1603
        if O0000O000O0O0OOOO :#line:1604
            for OOO0O00OO0OOO00O0 in O0O0O000000OOO0OO :#line:1605
                OOO0000O0O0OO000O =discord .Embed (title ="Permission Changes",color =discord .Color .green ())#line:1606
                OOO0000O0O0OO000O .add_field (name ="Permission Added",value =f"{OOOOOOOOOOO0OO0O0.mention} added permission {OOO0O00OO0OOO00O0[0].mention} for {OOO0O00OO0OOO00O0[1].mention} in {O0OO00OOOO0OOO000.mention}",inline =False )#line:1609
                await O0000O000O0O0OOOO .send (embed =OOO0000O0O0OO000O )#line:1610
            for OOO0O00OO0OOO00O0 in O0O00000OO000OO0O :#line:1612
                OOO0000O0O0OO000O =discord .Embed (title ="Permission Changes",color =discord .Color .red ())#line:1613
                OOO0000O0O0OO000O .add_field (name ="Permission Removed",value =f"{OOOOOOOOOOO0OO0O0.mention} removed permission {OOO0O00OO0OOO00O0[0].mention} for {OOO0O00OO0OOO00O0[1].mention} in {O0OO00OOOO0OOO000.mention}",inline =False )#line:1616
                await O0000O000O0O0OOOO .send (embed =OOO0000O0O0OO000O )#line:1617
@bot .event #line:1620
async def on_guild_channel_create (OO000OO0OOOO000OO ):#line:1621
    async for OO0OO0OO0O0OOOOOO in OO000OO0OOOO000OO .guild .audit_logs (limit =1 ,action =discord .AuditLogAction .channel_create ):#line:1623
        O0000O000O0O000O0 =OO0OO0OO0O0OOOOOO .user #line:1624
        break #line:1625
    OO0O0OOOOOO0O00O0 =1234100559431077939 #line:1628
    O000OO0OOO000000O =bot .get_channel (OO0O0OOOOOO0O00O0 )#line:1629
    if O000OO0OOO000000O :#line:1631
        OOOOO0O0O000OOO0O =discord .Embed (title ="Channel Changes",color =discord .Color .green ())#line:1632
        OOOOO0O0O000OOO0O .add_field (name ="Channel Created",value =f"{O0000O000O0O000O0.mention} created channel '{OO000OO0OOOO000OO.name}'",inline =False )#line:1634
        await O000OO0OOO000000O .send (embed =OOOOO0O0O000OOO0O )#line:1635
@bot .event #line:1638
async def on_guild_channel_delete (OOOO00OO0OOOOO0O0 ):#line:1639
    async for OOO0O00O000OO0O00 in OOOO00OO0OOOOO0O0 .guild .audit_logs (limit =1 ,action =discord .AuditLogAction .channel_delete ):#line:1641
        O0OOO00O0OOO00OOO =OOO0O00O000OO0O00 .user #line:1642
        break #line:1643
    O0O0O000OOOO0O000 =1234100559431077939 #line:1646
    OO0O000OOO0OOOO00 =bot .get_channel (O0O0O000OOOO0O000 )#line:1647
    if OO0O000OOO0OOOO00 :#line:1649
        O00OOO00000O000OO =discord .Embed (title ="Channel Changes",color =discord .Color .red ())#line:1650
        O00OOO00000O000OO .add_field (name ="Channel Deleted",value =f"{O0OOO00O0OOO00OOO.mention} deleted channel '{OOOO00OO0OOOOO0O0.name}'",inline =False )#line:1652
        await OO0O000OOO0OOOO00 .send (embed =O00OOO00000O000OO )#line:1653
@bot .event #line:1656
async def on_member_update (O0OO0OO00O000OOOO ,O0OOOO0000OOO000O ):#line:1657
    if O0OO0OO00O000OOOO .roles !=O0OOOO0000OOO000O .roles :#line:1658
        O00OO00O000O00OOO =[OOO000O00000000O0 for OOO000O00000000O0 in O0OOOO0000OOO000O .roles if OOO000O00000000O0 not in O0OO0OO00O000OOOO .roles and str (OOO000O00000000O0 )]#line:1660
        OO00OO00OOOO0O0OO =[OOO000OO0OO00O000 for OOO000OO0OO00O000 in O0OO0OO00O000OOOO .roles if OOO000OO0OO00O000 not in O0OOOO0000OOO000O .roles and str (OOO000OO0OO00O000 )]#line:1661
        OOO00OO000OOOOO0O =O0OOOO0000OOO000O .guild .get_member (O0OOOO0000OOO000O .guild .owner_id )#line:1664
        OOO00OOO0OO0OOO00 =1234100559431077939 #line:1667
        O000O0O00OOO00OOO =bot .get_channel (OOO00OOO0OO0OOO00 )#line:1668
        if O000O0O00OOO00OOO :#line:1669
            if O00OO00O000O00OOO :#line:1670
                for O0000O0000OOO00O0 in O00OO00O000O00OOO :#line:1671
                    O00O000O0OOO000OO =discord .Embed (title ="Role Changes",color =discord .Color .green ())#line:1672
                    O00O000O0OOO000OO .add_field (name ="Role Added",value =f"{OOO00OO000OOOOO0O.mention} added role {O0000O0000OOO00O0.mention} to {O0OOOO0000OOO000O.mention}",inline =False )#line:1675
            if OO00OO00OOOO0O0OO :#line:1676
                for O0000O0000OOO00O0 in OO00OO00OOOO0O0OO :#line:1677
                    O00O000O0OOO000OO =discord .Embed (title ="Role Changes",color =discord .Color .red ())#line:1678
                    O00O000O0OOO000OO .add_field (name ="Role Removed",value =f"{OOO00OO000OOOOO0O.mention} removed role {O0000O0000OOO00O0.mention} from {O0OOOO0000OOO000O.mention}",inline =False )#line:1681
            await O000O0O00OOO00OOO .send (embed =O00O000O0OOO000OO )#line:1682
@bot .event #line:1685
async def on_guild_role_create (OOO00OO00OO0OOOOO ):#line:1686
    O0000O0O00O0O0OOO =OOO00OO00OO0OOOOO .guild .get_member (OOO00OO00OO0OOOOO .guild .owner_id )#line:1688
    OO0O00O0O0OOOOOO0 =1234100559431077939 #line:1691
    OOOOO000OO000OO0O =bot .get_channel (OO0O00O0O0OOOOOO0 )#line:1692
    if OOOOO000OO000OO0O :#line:1693
        OOOOOOOO000OOO00O =discord .Embed (title ="Role Changes",color =discord .Color .green ())#line:1694
        OOOOOOOO000OOO00O .add_field (name ="Role Created",value =f"{O0000O0O00O0O0OOO.mention} created role {OOO00OO00OO0OOOOO.mention}",inline =False )#line:1695
        await OOOOO000OO000OO0O .send (embed =OOOOOOOO000OOO00O )#line:1696
@bot .event #line:1699
async def on_guild_role_delete (OO0000OO00O0O0000 ):#line:1700
    O0OOOO00OOOO00O00 =OO0000OO00O0O0000 .guild .get_member (OO0000OO00O0O0000 .guild .owner_id )#line:1701
    OOOOOOOO0O0OO0O00 =1234100559431077939 #line:1702
    O0O0O0O0O00O00000 =bot .get_channel (OOOOOOOO0O0OO0O00 )#line:1703
    if O0O0O0O0O00O00000 :#line:1705
        O000O0000OOO000O0 =discord .Embed (title ="Role Changes",color =discord .Color .red ())#line:1706
        O000O0000OOO000O0 .add_field (name ="Role Deleted",value =f"{O0OOOO00OOOO00O00.mention} deleted role '{OO0000OO00O0O0000.name}'",inline =False )#line:1707
        await O0O0O0O0O00O00000 .send (embed =O000O0000OOO000O0 )#line:1708
@bot .command (name ='change_name',help ='Change the nickname of the user\n\nTHE USER MUST BE:\n- user ID\nOR\n- user name')#line:1712
async def change_name (O00O0O00O00O00OOO ,OO0OOOOOO0OOO00OO ,O0O0OOOOOOOOOO0OO ):#line:1713
    if O00O0O00O00O00OOO .author .guild_permissions .administrator :#line:1715
        OO0OOOOOO0OOO00OO =discord .utils .get (O00O0O00O00O00OOO .guild .members ,name =OO0OOOOOO0OOO00OO )#line:1717
        if OO0OOOOOO0OOO00OO :#line:1718
            await OO0OOOOOO0OOO00OO .edit (nick =O0O0OOOOOOOOOO0OO )#line:1720
            await O00O0O00O00O00OOO .send (f"Changed nickname of {OO0OOOOOO0OOO00OO.mention} to {O0O0OOOOOOOOOO0OO}")#line:1721
        else :#line:1722
            await O00O0O00O00O00OOO .send (f"User '{OO0OOOOOO0OOO00OO}' does not exist.")#line:1723
    else :#line:1724
        await O00O0O00O00O00OOO .reply ("You don't have permission to use this command.")#line:1725
@bot .command (name ='remove_name',help ='Removes a nickname from the given user')#line:1728
async def remove_nickname (O000O00000OOO0O00 ,OOOO0O0O0O0O000O0 ):#line:1729
    if O000O00000OOO0O00 .author .guild_permissions .administrator :#line:1730
        OOOO0O0O0O0O000O0 =discord .utils .get (O000O00000OOO0O00 .guild .members ,name =OOOO0O0O0O0O000O0 )#line:1731
        if OOOO0O0O0O0O000O0 :#line:1732
            await OOOO0O0O0O0O000O0 .edit (nick =None )#line:1733
            await O000O00000OOO0O00 .send (f"Removed nickname of {OOOO0O0O0O0O000O0.mention}")#line:1734
        else :#line:1735
            await O000O00000OOO0O00 .send (f"User '{OOOO0O0O0O0O000O0}' does not exist.")#line:1736
    else :#line:1737
        O000O00000OOO0O00 .reply ("You do not have permission to use this command.")#line:1738
@bot .command (name ='get_pfp',help ="Get a user's profile picture\n<user> can be either a user ID, user name or display name")#line:1742
async def get_pfp (O0O000OO00O00OO00 ,*,user ):#line:1743
    O0OOO0O00O00OOOO0 =MemberConverter ()#line:1745
    try :#line:1746
        O0OO0O00O00O0OOO0 =await O0OOO0O00O00OOOO0 .convert (O0O000OO00O00OO00 ,user )#line:1747
    except :#line:1748
        await O0O000OO00O00OO00 .reply (f"User '{user}' does not exist, or does not have a profile picture.")#line:1749
        return #line:1750
    if O0OO0O00O00O0OOO0 :#line:1753
        await O0O000OO00O00OO00 .reply (O0OO0O00O00O0OOO0 .avatar .url )#line:1754
    else :#line:1755
        await O0O000OO00O00OO00 .reply (f"User '{user}' does not exist, or does not have a profile picture.")#line:1756
@bot .command (help ="Delete a specified number of messages in the channel. \nAlways add 1 to the count when using this command as your message counts as a message for the bot to delete.\nThis can only delete up to 100 messages (sadly)")#line:1760
async def purge (OOOOO0O00O0OOOOOO ,O0OOO00OOOO0OO00O :int ):#line:1761
    if OOOOO0O00O0OOOOOO .author .guild_permissions .administrator :#line:1763
        await OOOOO0O00O0OOOOOO .message .delete ()#line:1765
        O00O0O0OOO0OO0OO0 =await OOOOO0O00O0OOOOOO .send (f"Deleting messages... 0/{O0OOO00OOOO0OO00O} messages deleted so far.")#line:1768
        O0O00OOO0OO00OO00 =[]#line:1771
        async for O0O00O00OO0O0OOOO in OOOOO0O00O0OOOOOO .channel .history (limit =O0OOO00OOOO0OO00O +1 ):#line:1772
            if O0O00O00OO0O0OOOO .id !=O00O0O0OOO0OO0OO0 .id :#line:1773
                O0O00OOO0OO00OO00 .append (O0O00O00OO0O0OOOO )#line:1774
        await OOOOO0O00O0OOOOOO .channel .delete_messages (O0O00OOO0OO00OO00 )#line:1777
        await O00O0O0OOO0OO0OO0 .edit (content =f"Deleted {len(O0O00OOO0OO00OO00)} out of {O0OOO00OOOO0OO00O} messages. Command ran by: {OOOOO0O00O0OOOOOO.author.mention}")#line:1781
    else :#line:1782
        await OOOOO0O00O0OOOOOO .reply ("You don't have permission to use this command.")#line:1784
@bot .command (help ="Makes you depressed")#line:1787
async def depression (O0OOO0OOO0O0OO0OO ):#line:1788
    OO000OOOOO0O0OOO0 =discord .utils .get (O0OOO0OOO0O0OO0OO .guild .roles ,name ='depressed')#line:1789
    if OO000OOOOO0O0OOO0 is None :#line:1790
        OO000OOOOO0O0OOO0 =await O0OOO0OOO0O0OO0OO .guild .create_role (name ='depressed',color =discord .Color .dark_gray ())#line:1791
        await O0OOO0OOO0O0OO0OO .send (f"Created '{OO000OOOOO0O0OOO0}' role.")#line:1792
    OOO0000OOOOOOO00O =str (O0OOO0OOO0O0OO0OO .author )#line:1794
    if OOO0000OOOOOOO00O =="kefayt_":#line:1795
        OOOOO00O0O00OO0O0 =discord .utils .get (O0OOO0OOO0O0OO0OO .guild .roles ,name ='depressed')#line:1796
        if OOOOO00O0O00OO0O0 is None :#line:1797
            OOOOO00O0O00OO0O0 =await O0OOO0OOO0O0OO0OO .guild .create_role (name ='depressed-king',color =discord .Color .dark_gray ())#line:1798
            await O0OOO0OOO0O0OO0OO .send (f"Created '{OO000OOOOO0O0OOO0}' role.")#line:1799
        await O0OOO0OOO0O0OO0OO .reply ("You can't make a depressed person depressed.")#line:1800
    else :#line:1802
        await O0OOO0OOO0O0OO0OO .author .add_roles (OO000OOOOO0O0OOO0 )#line:1803
        await O0OOO0OOO0O0OO0OO .reply (f"Role '{OO000OOOOO0O0OOO0}' added to you!")#line:1804
@bot .event #line:1808
async def on_command_error (O000OOO0OOOO000O0 ,O0O0O0OO0O0O000OO ):#line:1809
    if isinstance (O0O0O0OO0O0O000OO ,commands .CommandNotFound ):#line:1810
        await O000OOO0OOOO000O0 .reply ("That command does not exist.")#line:1811
    elif isinstance (O0O0O0OO0O0O000OO ,commands .MissingRequiredArgument ):#line:1813
        await O000OOO0OOOO000O0 .reply ("Missing required arguments.")#line:1814
    elif isinstance (O0O0O0OO0O0O000OO ,commands .BadArgument ):#line:1816
        await O000OOO0OOOO000O0 .reply ("Bad argument provided.")#line:1817
    elif isinstance (O0O0O0OO0O0O000OO ,commands .CommandOnCooldown ):#line:1819
        await O000OOO0OOOO000O0 .reply (f"This command is on cooldown. Try again in {round(O0O0O0OO0O0O000OO.retry_after)} seconds.")#line:1820
    elif isinstance (O0O0O0OO0O0O000OO ,commands .MissingPermissions ):#line:1822
        await O000OOO0OOOO000O0 .reply ("You don't have the necessary permissions to run this command.")#line:1823
    elif isinstance (O0O0O0OO0O0O000OO ,commands .BotMissingPermissions ):#line:1825
        await O000OOO0OOOO000O0 .reply ("The bot doesn't have the necessary permissions to execute this command.")#line:1826
    elif isinstance (O0O0O0OO0O0O000OO ,commands .DisabledCommand ):#line:1828
        await O000OOO0OOOO000O0 .reply ("This command is currently disabled.")#line:1829
    elif isinstance (O0O0O0OO0O0O000OO ,commands .NoPrivateMessage ):#line:1831
        await O000OOO0OOOO000O0 .reply ("This command cannot be used in private messages.")#line:1832
    elif isinstance (O0O0O0OO0O0O000OO ,commands .CheckFailure ):#line:1834
        await O000OOO0OOOO000O0 .reply ("You do not have permission to use this command.")#line:1835
    elif isinstance (O0O0O0OO0O0O000OO ,commands .CommandInvokeError ):#line:1837
        await O000OOO0OOOO000O0 .reply ("An error occurred while executing the command.")#line:1838
        OO0O0OO00O0OO0O0O =getattr (O0O0O0OO0O0O000OO ,"original",O0O0O0OO0O0O000OO )#line:1840
        print ('An error occurred during command execution:',file =sys .stderr )#line:1841
        traceback .print_exception (type (O0O0O0OO0O0O000OO ),O0O0O0OO0O0O000OO ,O0O0O0OO0O0O000OO .__traceback__ ,file =sys .stderr )#line:1842
    else :#line:1844
        myLogger .error (f'An error occurred during command execution: {O0O0O0OO0O0O000OO}')#line:1845
@bot .command (name ="search",help ="Search for available commands.")#line:1848
async def search_command (O0OO0000O0O0O0O0O ,OO00OOO00O0OO0O00 :str ):#line:1849
    OO00000O00O00OOO0 =[OO0OOOO0O0O0OOO0O .name for OO0OOOO0O0O0OOO0O in bot .commands ]#line:1850
    if OO00OOO00O0OO0O00 in OO00000O00O00OOO0 :#line:1851
        O000O0O0O00000OOO =bot .get_command (OO00OOO00O0OO0O00 )#line:1852
        if O000O0O0O00000OOO :#line:1853
            OOO00O00OO000O00O =O000O0O0O00000OOO .help if O000O0O0O00000OOO .help else "No help information available."#line:1854
            OOO00OOO0O0OO000O =discord .Embed (title =f"Command: {OO00OOO00O0OO0O00}",description =f"**Help:**\n{OOO00O00OO000O00O}",color =discord .Color .blue ())#line:1856
            await O0OO0000O0O0O0O0O .reply (embed =OOO00OOO0O0OO000O )#line:1857
        else :#line:1858
            await O0OO0000O0O0O0O0O .reply (f"The command **{OO00OOO00O0OO0O00}** is available.")#line:1859
    else :#line:1860
        await O0OO0000O0O0O0O0O .reply (f"The command **{OO00OOO00O0OO0O00}** is not available.")#line:1861
if __name__ =="__main__":#line:1864
    bot .run (TOKEN )#line:1865