import asyncio
import configparser
import sys
import os
import time
import socket
import discord
from discord.ext import commands
import threading
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep

x_pos = 0
z_pos = 0

config = configparser.ConfigParser()
config.read("settings.ini")

zombiepic = config["Pics"]["zombie"]
playermarker = config["Pics"]["player"]
animalpic = config["Pics"]["animal"]
chartpic = config["Pics"]["chart"]
structurespic = config["Pics"]["structures"]
barricadespic= config["Pics"]["barricades"]

ServerIP = config["Network"]["ServerIP"]
ServerCommandsPort = int(config["Network"]["ServerCommandsPort"])
ServerCommandsEnabled = True
ServerCommandsLogin = config["Network"]["ServerCommandsLogin"]
ServerCommandsPassword = config["Network"]["ServerCommandsPassword"]
ServerChatPort = int(config["ChatSettings"]["ServerChatPort"])
ServerChatPassword = config["ChatSettings"]["ServerChatPassword"]
ChatEnabled = True if config["ChatSettings"]["ChatEnabled"] == "true" else False
LogChannelID = int(config["ChatSettings"]["LogChannelID"])
ChatChannelID = int(config["ChatSettings"]["ChatChannelID"])

VIPCanGetZombiesOnMap = True if config["VIPPermissions"]["CanGetZombiesOnMap"] == "true" else False
VIPCanGetPlayersOnMap = True if config["VIPPermissions"]["CanGetPlayersOnMap"] == "true" else False
VIPCanGetAnimalsOnMap = True if config["VIPPermissions"]["CanGetAnimalsOnMap"] == "true" else False
VIPCanGetStructuresOnMap = True if config["VIPPermissions"]["CanGetStructuresOnMap"] == "true" else False

VIPCanKillAllAnimals = True if config["VIPPermissions"]["CanKillAllAnimals"] == "true" else False
VIPCanKillAllZombies = True if config["VIPPermissions"]["CanKillAllZombies"] == "true" else False
VIPCanResetAllNPC = True if config["VIPPermissions"]["CanResetAllNPC"] == "true" else False
VIPCanTeleportPlayers = True if config["VIPPermissions"]["CanTeleportPlayers"] == "true" else False
VIPCanTrackPlayerPosition = True if config["VIPPermissions"]["CanTrackPlayerPosition"] == "true" else False
VIPCanDumpAll = True if config["VIPPermissions"]["CanDumpAll"] == "true" else False

AdminRole = config["AdminSettings"]["AdminRole"]
VIPRole = config["AdminSettings"]["VIPRole"]

token = open('token.txt', 'r').readline()
client = commands.Bot( command_prefix = 'u_')

def ReConnectNetworkCommands():
    global untcommandssock
    untcommandssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    untcommandssock.settimeout(5)
    untcommandssock.connect((ServerIP, ServerCommandsPort))
    account = f"|{ServerCommandsLogin}|{ServerCommandsPassword}|"
    untcommandssock.send(account.encode('utf-8'))
    try:
        autlog = untcommandssock.recv(1024).decode('utf-8')
        print(f"RCON Authentification status: {autlog}")
    except:
    	print("Error with receiving server log ;(")
def ReConnectChat():
    global untchatsock
    untchatsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    untchatsock.connect((ServerIP, ServerChatPort))
    pkg = f"|{ServerChatPassword}|"
    untchatsock.send(pkg.encode('utf-8'))
    try:
        autlog = untchatsock.recv(1024).decode('utf-8')
        print(f"Network Chat Authentification status: {autlog}")
        loop = asyncio.get_event_loop()
        rxchatthr = threading.Thread(target=UntChatRX, args=(loop, ), name="ChatThread")
        rxchatthr.start()
    except:
    	print("Error with receiving server log ;(")

def send_recv_server(pkg):
    try:
        pkg = f"|{pkg}|".encode('utf-8')
        untcommandssock.send(pkg)
        data = untcommandssock.recv(1024).decode('utf-8')
        return data
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
def send_recv_server_args(pkg, args):
    try:
        pkg = f"|{pkg}|{args}|".encode('utf-8')
        untcommandssock.send(pkg)
        data = untcommandssock.recv(1024).decode('utf-8')
        return data
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
def create_pix_from_coords(x,z):
    img1 = Image.open(chartpic)
    img2 = Image.open(playermarker).convert("RGBA")
    pix_x = 1016 + int(x)
    pix_z = 1016 - int(z)
    if(pix_x > 2020 and pix_z > 2020):
        pix_x = 2020
        pix_z = 2020
    elif(pix_x > 2020):
        pix_x = 2020
    elif(pix_z > 2020):
        pix_z = 2020
    img1.paste(img2, (pix_x,pix_z), img2)
    img1.save('Cache/playerposition.png')

@client.event
async def on_ready():
	print(f'{client.user.name} BOT connected!')

@client.command( pass_context = True)
async def info(ctx):
	await ctx.send('Unturned 2.2.5 Bot')
	
@client.command( pass_context = True)
async def author(ctx):
	await ctx.send('Made by NeoLight')

@client.command(pass_context = True)
async def ban(ctx, *args):
    try:
        role_names = [role.name for role in ctx.message.author.roles]
        if (AdminRole not in role_names):
            await ctx.send("You don't have permissions to use this command")
            return
        pkg = f"|ban|{args[0]}|{args[1]}|".encode('utf-8')
        untcommandssock.send(pkg)
        await ctx.send(untcommandssock.recv(1024).decode('utf-8'))
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
@client.command(pass_context = True)
async def kick(ctx, *args):
    try:
        role_names = [role.name for role in ctx.message.author.roles]
        if (AdminRole not in role_names):
            await ctx.send("You don't have permissions to use this command")
            return
        pkg = f"|kick|{args[0]}|{args[1]}|".encode('utf-8')
        untcommandssock.send(pkg)
        await ctx.send(untcommandssock.recv(1024).decode('utf-8'))
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
@client.command(pass_context = True)
async def getIP(ctx,arg):
    try:
	    role_names = [role.name for role in ctx.message.author.roles]
	    if (AdminRole not in role_names):
		    await ctx.send("You don't have permissions to use this command")
		    return
	    pIP = send_recv_server_args('getuserip', arg)
	    await ctx.send(f"{arg} IP is: {pIP}")
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()

@client.command(pass_context = True)
async def getstructurescount(ctx):
	structures_count = send_recv_server('getstructures')
	await ctx.send(structures_count)

@client.command(pass_context = True)
async def getzombiecount(ctx):
	getzombiecount_count = send_recv_server('getzombiecount')
	await ctx.send(getzombiecount_count)

@client.command(pass_context = True)
async def getanimalcount(ctx):
	getanimals_count = send_recv_server('getanimals')
	await ctx.send(getanimals_count)

@client.command(pass_context = True)
async def killallanimals(ctx):
	role_names = [role.name for role in ctx.message.author.roles]
	if (AdminRole not in role_names) and (VIPRole not in role_names):
		await ctx.send("You don't have permissions to use this command")
		return
	if (not VIPCanKillAllAnimals and AdminRole not in role_names):
		await ctx.send("You don't have permissions to use this command")
		return
	killallanimals_quest = send_recv_server('killallanimals')
	await ctx.send(killallanimals_quest)

@client.command(pass_context = True)
async def playerslist(ctx):
	players_list = send_recv_server('playerslist').replace(',','\n')
	await ctx.send("Server Players: " + '\n' + "```" + "\n" + players_list + '\n' + "```")

@client.command(pass_context = True)
async def respawnallnpc(ctx):
	role_names = [role.name for role in ctx.message.author.roles]
	if (AdminRole not in role_names) and (VIPRole not in role_names):
		await ctx.send("You don't have permissions to use this command")
		return
	if (not VIPCanResetAllNPC and AdminRole not in role_names):
		await ctx.send("You don't have permissions to use this command")
		return
	respawnallnpc_quest = send_recv_server('respawnnpc')
	await ctx.send(respawnallnpc_quest)

@client.command(pass_context = True)
async def killallzombies(ctx):
	role_names = [role.name for role in ctx.message.author.roles]
	if (AdminRole not in role_names) and (VIPRole not in role_names):
		await ctx.send("You don't have permissions to use this command")
		return
	if (not VIPCanKillAllZombies and AdminRole not in role_names):
		await ctx.send("You don't have permissions to use this command")
		return
	killallzombies_quest = send_recv_server('killallzombies')
	await ctx.send(killallzombies_quest)

@client.command(pass_context = True)
async def tp(ctx,*args):
    role_names = [role.name for role in ctx.message.author.roles]
    if (AdminRole not in role_names) and (VIPRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    if (not VIPCanTeleportPlayers and AdminRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    try:
        pkg = f"|tp|{args[0]}|{args[1]}|{args[2]}|{args[3]}|".encode('utf-8')
        untcommandssock.send(pkg)
        server_msg = untcommandssock.recv(1024).decode('utf-8')
        await ctx.send(server_msg)
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
@client.command(pass_context = True)
async def gps(ctx,arg):
    role_names = [role.name for role in ctx.message.author.roles]
    if (AdminRole not in role_names) and (VIPRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    if (not VIPCanTrackPlayerPosition and AdminRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    try:
        pkg = f"|pchart|{arg}|".encode('utf-8')
        untcommandssock.send(pkg)
        server_msg = untcommandssock.recv(1024).decode('utf-8')
        new_serverc = server_msg.split('|')
        p_x = new_serverc[1]
        p_z = new_serverc[2]
        create_pix_from_coords(p_x,p_z)
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
    await ctx.send(f"{arg} Location on Map")
    await ctx.send(file=discord.File("Cache/playerposition.png"))

@client.command(pass_context = True)
async def zombiesdump(ctx):
    role_names = [role.name for role in ctx.message.author.roles]
    if (AdminRole not in role_names) and (VIPRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    if (not VIPCanGetZombiesOnMap and AdminRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    try:
        untcommandssock.send('|zombiedump|'.encode('utf-8'))
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
        return
    raw_dump = untcommandssock.recv(10000).decode('utf-8')
    zombie_columns = raw_dump.split('/')
    img1 = Image.open(chartpic)
    img2 = Image.open(zombiepic).convert("RGBA")
    for zombie_column in zombie_columns:
        x_z = zombie_column.split('|')
        if(x_z[0] == '' or x_z[1] == ''):
            break
        x = int(x_z[0])
        z = int(x_z[1])
        pix_x = 1016 + int(x)
        pix_z = 1016 - int(z)
        if(pix_x > 2020 and pix_z > 2020):
            pix_x = 2020
            pix_z = 2020
        elif(pix_x > 2020):
            pix_x = 2020
        elif(pix_z > 2020):
            pix_z = 2020
        img1.paste(img2, (pix_x, pix_z), img2)
    img1.save('Cache/zombies.png')
    await ctx.send(file=discord.File('Cache/zombies.png'))
    os.remove('Cache/zombies.png')
@client.command(pass_context=True)
async def announce(ctx, *_args):
	role_names = [role.name for role in ctx.message.author.roles]
	if (AdminRole not in role_names):
		await ctx.send("You don't have permissions to use this command")
		return
	args = ""
	for arg in _args:
		args+=f"{arg} "
	await ctx.send(send_recv_server_args("announce", args))
@client.command(pass_context=True)
async def gettime(ctx):
	await ctx.send(send_recv_server("gettime"))
@client.command(pass_context = True)
async def animalsdump(ctx):
    role_names = [role.name for role in ctx.message.author.roles]
    if (AdminRole not in role_names) and (VIPRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    if (not VIPCanGetAnimalsOnMap and AdminRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    try:
        untcommandssock.send('|animaldump|'.encode('utf-8'))
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
        return
    raw_dump = untcommandssock.recv(10000).decode('utf-8')
    animal_columns = raw_dump.split('/')
    img1 = Image.open(chartpic)
    img2 = Image.open(animalpic).convert("RGBA")
    for animal_column in animal_columns:
        x_z = animal_column.split('|')
        if(x_z[0] == '' or x_z[1] == ''):
            break
        x = int(x_z[0])
        z = int(x_z[1])
        pix_x = 1016 + int(x)
        pix_z = 1016 - int(z)
        if(pix_x > 2020 and pix_z > 2020):
            pix_x = 2020
            pix_z = 2020
        elif(pix_x > 2020):
            pix_x = 2020
        elif(pix_z > 2020):
            pix_z = 2020
        pix_x -= 45
        pix_z -= 31
        img1.paste(img2, (pix_x, pix_z), img2)
    img1.save('Cache/animals.png')
    await ctx.send(file=discord.File('Cache/animals.png'))
    os.remove('Cache/animals.png')

@client.command(pass_context = True)
async def structuresdump(ctx):
    role_names = [role.name for role in ctx.message.author.roles]
    if (AdminRole not in role_names) and (VIPRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    if (not VIPCanGetStructuresOnMap and AdminRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    try:
        untcommandssock.send('|structuresdump|'.encode('utf-8'))
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
        return
    raw_dump = untcommandssock.recv(10000).decode('utf-8')
    animal_columns = raw_dump.split('/')
    img1 = Image.open(chartpic)
    img2 = Image.open(structurespic).convert("RGBA")
    for animal_column in animal_columns:
        x_z = animal_column.split('|')
        if(x_z[0] == '' or x_z[1] == ''):
            break
        x = int(x_z[0])
        z = int(x_z[1])
        pix_x = 1016 + int(x)
        pix_z = 1016 - int(z)
        if(pix_x > 2020 and pix_z > 2020):
            pix_x = 2020
            pix_z = 2020
        elif(pix_x > 2020):
            pix_x = 2020
        elif(pix_z > 2020):
            pix_z = 2020
        pix_x -= 45
        pix_z -= 31
        img1.paste(img2, (pix_x, pix_z), img2)
    img1.save('Cache/structures.png')
    await ctx.send(file=discord.File('Cache/structures.png'))
    os.remove('Cache/structures.png')
@client.command(pass_context = True)
async def playersdump(ctx):
    role_names = [role.name for role in ctx.message.author.roles]
    if (AdminRole not in role_names) and (VIPRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    if (not VIPCanGetPlayersOnMap and AdminRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    try:
        untcommandssock.send('|playersdump|'.encode('utf-8'))
    except:
        print("Error with commands connection")
        ReConnectNetworkCommands()
        return
    raw_dump = untcommandssock.recv(10000).decode('utf-8')
    animal_columns = raw_dump.split('/')
    img1 = Image.open(chartpic)
    for animal_column in animal_columns:
        try:
            x_z = animal_column.split('|')
            if(x_z[0] == '' or x_z[1] == '' or x_z[2] == '' or x_z[3] == ''):
                break
            x = int(x_z[0])
            z = int(x_z[1])
            face = str(x_z[2])
            name = str(x_z[3])
            img2 = Image.open(f"Resources/Faces/{face}.png").convert("RGBA")
            pix_x = 1016 + int(x)
            pix_z = 1016 - int(z)
            if(pix_x > 2020 and pix_z > 2020):
                pix_x = 2020
                pix_z = 2020
            elif(pix_x > 2020):
                pix_x = 2020
            elif(pix_z > 2020):
                pix_z = 2020
            pix_x -= 45
            pix_z -= 31
            img1.paste(img2, (pix_x, pix_z), img2)
            d = ImageDraw.Draw(img1)
            fnt = ImageFont.truetype("Resources/Fonts/ARLRDBD.TTF", 25)
            d.text((pix_x-17,pix_z+46), name, font=fnt,fill=(255,255,255,255))
        except:
            pass
    img1.save('Cache/playerspositions.png')
    await ctx.send(file=discord.File('Cache/playerspositions.png'))
    os.remove('Cache/playerspositions.png')
@client.command(pass_context = True)
async def dumpall(ctx):
    role_names = [role.name for role in ctx.message.author.roles]
    if (AdminRole not in role_names) and (VIPRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    if (not VIPCanDumpAll and AdminRole not in role_names):
        await ctx.send("You don't have permissions to use this command")
        return
    try:
        untcommandssock.send('|playersdump|'.encode('utf-8'))
    except:
    	ReConnectNetworkCommands()
    	return
    try:
        players_dump = untcommandssock.recv(10000).decode('utf-8')
    except:
    	pass
    try:
        untcommandssock.send('|structuresdump|'.encode('utf-8'))
    except:
    	pass
    try:
        structures_dump = untcommandssock.recv(10000).decode('utf-8')
    except:
    	pass
    try:
        untcommandssock.send('|animaldump|'.encode('utf-8'))
    except:
    	pass
    try:
        animals_dump = untcommandssock.recv(10000).decode('utf-8')
    except:
    	pass
    try:
        untcommandssock.send('|zombiedump|'.encode('utf-8'))
    except:
    	pass
    try:
        zombies_dump = untcommandssock.recv(10000).decode('utf-8')
    except:
    	pass
    try:
        animal_columns = animals_dump.split('/')
    except:
    	pass
    try:
        player_columns = players_dump.split('/')
    except:
    	pass
    try:
        zombie_columns = zombies_dump.split('/')
    except:
    	pass
    try:
        structure_columns = structures_dump.split('/')
    except:
    	pass
    img1 = Image.open(chartpic)
    for structure_column in structure_columns:
        try:
            x_z = structure_column.split('|')
            if(x_z[0] == '' or x_z[1] == ''):
                break
            x = int(x_z[0])
            z = int(x_z[1])
            img2 = Image.open(structurespic).convert("RGBA")
            pix_x = 1016 + int(x)
            pix_z = 1016 - int(z)
            if(pix_x > 2020 and pix_z > 2020):
                pix_x = 2020
                pix_z = 2020
            elif(pix_x > 2020):
                pix_x = 2020
            elif(pix_z > 2020):
                pix_z = 2020
            pix_x -= 45
            pix_z -= 31
            img1.paste(img2, (pix_x, pix_z), img2)
        except:
            pass
    try:
        for animal_column in animal_columns:
            try:
                x_z = animal_column.split('|')
                if(x_z[0] == '' or x_z[1] == ''):
                    break
                x = int(x_z[0])
                z = int(x_z[1])
                img2 = Image.open(animalpic).convert("RGBA")
                pix_x = 1016 + int(x)
                pix_z = 1016 - int(z)
                if(pix_x > 2020 and pix_z > 2020):
                    pix_x = 2020
                    pix_z = 2020
                elif(pix_x > 2020):
                    pix_x = 2020
                elif(pix_z > 2020):
                    pix_z = 2020
                pix_x -= 45
                pix_z -= 31
                img1.paste(img2, (pix_x, pix_z), img2)
            except:
                pass
    except:
    	pass
    try:
        for zombie_column in zombie_columns:
            try:
                x_z = zombie_column.split('|')
                if(x_z[0] == '' or x_z[1] == ''):
                    break
                x = int(x_z[0])
                z = int(x_z[1])
                img2 = Image.open(zombiepic).convert("RGBA")
                pix_x = 1016 + int(x)
                pix_z = 1016 - int(z)
                if(pix_x > 2020 and pix_z > 2020):
                    pix_x = 2020
                    pix_z = 2020
                elif(pix_x > 2020):
                    pix_x = 2020
                elif(pix_z > 2020):
                    pix_z = 2020
                pix_x -= 45
                pix_z -= 31
                img1.paste(img2, (pix_x, pix_z), img2)
            except:
                pass
    except:
    	pass
    for player_column in player_columns:
        try:
            x_z = player_column.split('|')
            if(x_z[0] == '' or x_z[1] == '' or x_z[2] == '' or x_z[3] == ''):
                break
            x = int(x_z[0])
            z = int(x_z[1])
            face = str(x_z[2])
            name = str(x_z[3])
            img2 = Image.open(f"Resources/Faces/{face}.png").convert("RGBA")
            pix_x = 1016 + int(x)
            pix_z = 1016 - int(z)
            if(pix_x > 2020 and pix_z > 2020):
                pix_x = 2020
                pix_z = 2020
            elif(pix_x > 2020):
                pix_x = 2020
            elif(pix_z > 2020):
                pix_z = 2020
            pix_x -= 45
            pix_z -= 31
            img1.paste(img2, (pix_x, pix_z), img2)
            d = ImageDraw.Draw(img1)
            fnt = ImageFont.truetype("Resources/Fonts/ARLRDBD.TTF", 25)
            d.text((pix_x-17,pix_z+46), name, font=fnt,fill=(255,255,255,255))
        except:
            pass
    img1.save('Cache/alldump.png')
    await ctx.send(file=discord.File('Cache/alldump.png'))
    os.remove('Cache/alldump.png')
def ThreadedChatRX():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(UntChatRX())

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.channel.id != ChatChannelID or message.author == client.user:
        return
    global untchatsock
    if untchatsock is None:
    	return
    txpkg = f"|{message.author.name}|{message.content}|".encode('utf-8')
    try:
        untchatsock.send(txpkg)
    except:
        print("Error with chat connection")
        ReConnectChat()

async def sendmsgRX(_rxpkg):
	nchannel = client.get_channel(ChatChannelID)
	logchannel = client.get_channel(LogChannelID)
	rxmassiv = _rxpkg.decode('utf-8').split('|')
	if rxmassiv[1] == '1':
		await nchannel.send(f"[{rxmassiv[2]}] Connected !")
		await logchannel.send(f"[{rxmassiv[2]}] Connected !  ({rxmassiv[3]})")
	elif rxmassiv[1] == '2':
		await nchannel.send(f"[{rxmassiv[2]}] Disconnected ")
		await logchannel.send(f"[{rxmassiv[2]}] Disconnected ! ({rxmassiv[3]})")
	else:
		await nchannel.send(f"[{rxmassiv[2]}]: {rxmassiv[3]}")

def InfoSender(info):
	print(f"Server Info: {info}")
def UntChatRX(_loop):
	while True:
		global untchatsock
		try:
			_rxpkg = untchatsock.recv(1024)
			if _rxpkg.decode('utf-8').split('|')[1] == "info":
				InfoSender(_rxpkg.decode('utf-8').split('|')[2])
				continue
			send_fut = asyncio.run_coroutine_threadsafe(sendmsgRX(_rxpkg), _loop)
			send_fut.result()
		except:
			print("Error With Chat Connection")
			time.sleep(1)
			ReConnectChat()
if ChatEnabled:
    untchatsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    untchatsock.connect((ServerIP, ServerChatPort))
    pkg = f"|{ServerChatPassword}|"
    untchatsock.send(pkg.encode('utf-8'))
    try:
        autlog = untchatsock.recv(1024).decode('utf-8')
        print(f"Network Chat Authentification status: {autlog}")
    except:
    	print("Error with receiving Chat server log ;(")
    loop = asyncio.get_event_loop()
    rxchatthr = threading.Thread(target=UntChatRX, args=(loop, ), name="ChatThread")
    rxchatthr.start()
if ServerCommandsEnabled:
    untcommandssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    untcommandssock.settimeout(5)
    untcommandssock.connect((ServerIP, ServerCommandsPort))
    account=f"|{ServerCommandsLogin}|{ServerCommandsPassword}|"
    untcommandssock.send(account.encode('utf-8'))
    try:
        autlog = untcommandssock.recv(1024).decode('utf-8')
        print(f"Network RCON Authentification status: {autlog}")
    except:
    	print("Error with receiving Chat server log ;(")
client.run(token)
