import tkinter as tk
from tkinter import scrolledtext, messagebox
import discord
import asyncio
import threading
import time
import urllib.request
import json
import socket
import sys
import os
import tempfile
from discord_webhook import DiscordWebhook, DiscordEmbed
import random

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

if not is_connected():
    messagebox.showinfo("IVAO GR ERROR", "Cannot establish an internet connection!")
    sys.exit()
    
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################

reqCode = random.randint(100000, 999999)
screenNum = random.randint(100, 999)

webhook = DiscordWebhook(url="link_of_verification_code_discord_webhook", username="Ivao.gr Verify Bot")
embed = DiscordEmbed(title=f"App number: {screenNum}", color="03b2f8")
embed.set_author(name="Panagiotis Giakoumakis", icon_url="https://cdn.discordapp.com/attachments/817501450208935946/1219006202105827408/327164182_1352097255564251_8657518921268393376_n.png?ex=6609bafe&is=65f745fe&hm=d19a062e3226ec905af81bcfe66a89d65d64be61f00dd2057692eb20f015d735&")
embed.set_timestamp()
embed.add_embed_field(name="Verification code: ", value=reqCode)
webhook.add_embed(embed)
response = webhook.execute()

temp_dir = tempfile.gettempdir()
file_path_ico = os.path.join(temp_dir, "logo.ico")
urllib.request.urlretrieve("link_of_logo.ico", file_path_ico)


CanOpen = False
def goMain(code):
    global CanOpen
    if code == str(reqCode):
        CanOpen = True
        login_page.destroy()
        print("Successfully loged in!")
    else:
        print("failed to log in")

login_page = tk.Tk()
login_page.title("Login")
login_page.iconbitmap(file_path_ico)
title_label = tk.Label(login_page, text=f"App id: {screenNum}")
title_label.pack()
title_entry = tk.Entry(login_page, width=50)
title_entry.pack()
submit_button = tk.Button(login_page, text="Submit", command=lambda: goMain(title_entry.get()))
submit_button.pack()

login_page.mainloop()


#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################

# TOKEN = 'MTIxNTM5Nzg4NTcxMDE3MjE5MA.GLP4nW.CTpWlamrg_Qv3z0ki_tNnNILSsHzgKPTP7ImZs'
# version = '1.2'
# excludeRole = 'DontSendDM'
# divisionChannel = 1215971486704341004
# eventsChannel = 1215971509412171876
# atcChannel = 1215971532673912963
# soChannel = 1215971555247657061


if CanOpen:
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "config.json")
    print(file_path)

    urllib.request.urlretrieve("link_of_config.json", file_path)

    with open(file_path) as f:
        config = json.load(f)

    TOKEN = config["TOKEN"]
    version = config["version"]
    excludeRole = config["excludeRole"]
    divisionChannel = config["divisionChannel"]
    eventsChannel = config["eventsChannel"]
    atcChannel = config["atcChannel"]
    soChannel = config["soChannel"]

    intents = discord.Intents.default()
    intents.members = True

    client = discord.Client(intents=intents)

    #############
    ##########
    #############
    async def send_message_to_channel(channel, message_content):
        if channel is None:
            console_preview.insert(tk.END, "Error: Channel is None\n")
            return

        try:
            await channel.send(content=message_content)
            console_preview.insert(tk.END, f"Sent message to channel: {channel.name}\n")
        except discord.Forbidden:
            console_preview.insert(tk.END, f"Couldn't send message to channel: {channel.name}: No permission\n")
        except discord.HTTPException as e:
            console_preview.insert(tk.END, f"Couldn't send message to channel: {channel.name}: {e}\n")

    async def send_embed_to_channel(channel, embed):
        if channel is None:
            console_preview.insert(tk.END, "Error: Channel is None\n")
            return

        try:
            await channel.send(content='||@everyone||', embed=embed)
            console_preview.insert(tk.END, f"Sent embed to channel: {channel.name}\n")
        except discord.Forbidden:
            console_preview.insert(tk.END, f"Couldn't send embed to channel: {channel.name}: No permission\n")
        except discord.HTTPException as e:
            console_preview.insert(tk.END, f"Couldn't send embed to channel: {channel.name}: {e}\n")

    #############
    ##########
    #############

    async def send_embedded_dm(embed, excluded_role_name):

        if sendtochannel_var.get():
            if selected_channel.get() == 'Division':
                target_channel = channelDivision
            elif selected_channel.get() == 'Events':
                target_channel =channelEvents
            elif selected_channel.get() == 'Atc':
                target_channel =channelAtc
            elif selected_channel.get() == 'SO Announcement':
                target_channel = channelSo

            await send_embed_to_channel(target_channel, embed)

        bot_user = client.user
        for guild in client.guilds:
            for member in guild.members:
                if member != bot_user and not member.bot:
                    excluded_role = discord.utils.get(guild.roles, name=excluded_role_name)
                    if excluded_role not in member.roles:
                        try:
                            await member.send(embed=embed)
                            console_preview.insert(tk.END, f"Sent an embedded message to {member.name}#{member.discriminator}\n")
                        except discord.Forbidden:
                            console_preview.insert(tk.END, f"Couldn't send an embedded message to {member.name}#{member.discriminator}: No permission\n")
                        except discord.HTTPException as e:
                            console_preview.insert(tk.END, f"Couldn't send an embedded message to {member.name}#{member.discriminator}: {e}\n")



    async def send_dm(message, excluded_role_name):

        if sendtochannel_var.get():
            if selected_channel.get() == 'Division':
                target_channel = channelDivision
            elif selected_channel.get() == 'Events':
                target_channel =channelEvents
            elif selected_channel.get() == 'Atc':
                target_channel =channelAtc
            elif selected_channel.get() == 'SO Announcement':
                target_channel = channelSo

            await send_message_to_channel(target_channel, message)

        for guild in client.guilds:
            for member in guild.members:
                if member != client.user and not member.bot:
                    excluded_role = discord.utils.get(guild.roles, name=excluded_role_name)
                    if excluded_role not in member.roles:
                        try:
                            await member.send(message)
                            console_preview.insert(tk.END, f"Sent a DM to {member.name}#{member.discriminator}\n")
                        except discord.Forbidden:
                            console_preview.insert(tk.END, f"Couldn't send a DM to {member.name}#{member.discriminator}: No permission\n")
                        except discord.HTTPException as e:
                            console_preview.insert(tk.END, f"Couldn't send a DM to {member.name}#{member.discriminator}: {e}\n")





    def clear_console():
        console_preview.delete(1.0, tk.END)


    root = tk.Tk()
    root.title("IVAO Discord mailer")

    print(file_path_ico)



    root.iconbitmap(file_path_ico)

    message_label = tk.Label(root, text="Enter Message:")
    message_label.pack()
    message_entry = tk.Entry(root, width=50)
    message_entry.pack()


    def send_message():
        console_preview.insert(tk.END, f"Please wait...\n")
        message = message_entry.get()
        client.loop.create_task(send_dm(message,excludeRole))


    send_button = tk.Button(root, text="Send DM", command=send_message)
    send_button.pack()

    sendtochannel_var = tk.BooleanVar()
    sendtochannel_check = tk.Checkbutton(root, text="Do you want to send the message or embed to announcement channel?", variable=sendtochannel_var)
    sendtochannel_check.pack(side=tk.TOP)

    ##############################

    # def show(): 
    #     label.config( text = selected_channel.get() ) 

    options = [ 
        "Division", 
        "Events", 
        "Atc", 
        "SO Announcement"
    ] 
    selected_channel = tk.StringVar() 
    selected_channel.set( "Division" ) 
    drop = tk.OptionMenu( root , selected_channel , *options ) 
    drop.pack(side=tk.TOP) 
    
    # Create button, it will change label text 
    # button = tk.Button( root , text = "click Me" , command = show ).pack() 
    
    # Create Label 
    # label = tk.Label( root , text = " " ) 
    # label.pack() 
    ############################

    clear_button = tk.Button(root, text="Clear Console", command=clear_console)
    clear_button.pack()


    console_preview = scrolledtext.ScrolledText(root, width=80, height=20)
    console_preview.pack()

    def on_ready():
        console_preview.insert(tk.END, f'Logged in as {client.user}, with version: {version}\n')
        console_preview.insert(tk.END, f'Made by panagiotisgiak3\n')
        console_preview.insert(tk.END, 'Ready to use :)')




    # selected_channel.get()
    # divisionChannel = 1215971486704341004
    # eventsChannel = 1215971509412171876
    # atcChannel = 1215971532673912963
    # soChannel = 1215971555247657061


    @client.event
    async def on_ready():
        console_preview.insert(tk.END, f'Logged in as {client.user}, with version: {version}\n')
        console_preview.insert(tk.END, f'Made by panagiotisgiak3\n')
        console_preview.insert(tk.END, f'Ready to use :)\n')


        # global target_channel
        # target_channel_id = announcementChannel
        # target_channel = client.get_channel(target_channel_id)

        # if target_channel is not None:
        #     console_preview.insert(tk.END, f"Target channel retrieved: {target_channel.name}\n")
        # else:
        #     console_preview.insert(tk.END, "Error: Target channel is None\n")

        global channelDivision
        global channelEvents
        global channelAtc
        global channelSo

        channelDivision = client.get_channel(divisionChannel)
        channelEvents = client.get_channel(eventsChannel)
        channelAtc = client.get_channel(atcChannel)
        channelSo = client.get_channel(soChannel)

        if channelDivision is not None:
            console_preview.insert(tk.END, f"Division channel retrieved: {channelDivision.name}\n")
        else:
            console_preview.insert(tk.END, "Error: Division channel is None\n")

        if channelEvents is not None:
            console_preview.insert(tk.END, f"Events channel retrieved: {channelEvents.name}\n")
        else:
            console_preview.insert(tk.END, "Error: Events channel is None\n")

        if channelAtc is not None:
            console_preview.insert(tk.END, f"Atc channel retrieved: {channelAtc.name}\n")
        else:
            console_preview.insert(tk.END, "Error: Atc channel is None\n")

        if channelSo is not None:
            console_preview.insert(tk.END, f"So channel retrieved: {channelSo.name}\n")
        else:
            console_preview.insert(tk.END, "Error: So channel is None\n")



    def run_bot():
        client.run(TOKEN)


    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    def open_embedded_popup():
        embedded_popup = tk.Toplevel(root)
        embedded_popup.title("Setup Embedded Message")
        embedded_popup.iconbitmap(file_path_ico)

        title_label = tk.Label(embedded_popup, text="Title:")
        title_label.pack()
        title_entry = tk.Entry(embedded_popup, width=50)
        title_entry.pack()

        description_label = tk.Label(embedded_popup, text="Description:")
        description_label.pack()
        description_entry = tk.Entry(embedded_popup, width=50)
        description_entry.pack()

        photo_label = tk.Label(embedded_popup, text="Photo URL:")
        photo_label.pack()
        photo_entry = tk.Entry(embedded_popup, width=50)
        photo_entry.pack()

        fields_frame = tk.Frame(embedded_popup)
        fields_frame.pack()

        fields = []

        def add_field():
            field_frame = tk.Frame(fields_frame)
            field_frame.pack()
            field_title_label = tk.Label(field_frame, text="Field Title:")
            field_title_label.pack(side=tk.LEFT)
            field_title_entry = tk.Entry(field_frame, width=20)
            field_title_entry.pack(side=tk.LEFT)
            field_value_label = tk.Label(field_frame, text="Field Value:")
            field_value_label.pack(side=tk.LEFT)
            field_value_entry = tk.Entry(field_frame, width=20)
            field_value_entry.pack(side=tk.LEFT)
            fields.append((field_title_entry, field_value_entry))

        add_field_button = tk.Button(embedded_popup, text="Add Field", command=add_field)
        add_field_button.pack()

        footer_frame = tk.Frame(embedded_popup)
        footer_frame.pack()

        footer_text = "IVAO GR 2024"
        footer_icon_url = "https://cdn.discordapp.com/attachments/992526898930401355/1215699904605986897/327164182_1352097255564251_8657518921268393376_n.png?ex=65fdb3c3&is=65eb3ec3&hm=5baeaf7b486b7d267a826485d609302619645e720c01b4ce0fd2aa8fc17e5605&"
        embed_color = 0x0749ce  # ivao blue color


        timestamp_var = tk.BooleanVar()
        timestamp_check = tk.Checkbutton(embedded_popup, text="Include Timestamp", variable=timestamp_var)
        timestamp_check.pack()

        def send_embedded_message():
            console_preview.insert(tk.END, f"Please wait...\n")
            embed = discord.Embed(title=title_entry.get(), description=description_entry.get(), color=embed_color)
            if photo_entry.get():
                embed.set_image(url=photo_entry.get())
            for field in fields:
                embed.add_field(name=field[0].get(), value=field[1].get(), inline=False)
            embed.set_footer(text=footer_text, icon_url=footer_icon_url)
            if timestamp_var.get():
                embed.timestamp = discord.utils.utcnow()
            client.loop.create_task(send_embedded_dm(embed,excludeRole))
            embedded_popup.destroy()

        send_button = tk.Button(embedded_popup, text="Send", command=send_embedded_message)
        send_button.pack()


    embedded_button = tk.Button(root, text="Setup Embedded Message", command=open_embedded_popup)
    embedded_button.pack()



    root.mainloop()