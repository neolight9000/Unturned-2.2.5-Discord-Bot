# Unturned-2.2.5-Discord-Bot
The first discord bot working with the UnturnedNetworkAPI plugin. Allows you to administer the server through Discord.

# References
`Pillow` - `pip install Pillow`

`configparser` - `pip install configparser`

`discord` - `pip install discord.py`


# Commands
`ban` - Ban a player on the server, `only admins can use this command.` example:
`u_ban` `PlayerName` `Reason`

`kick` - Kick a player from the server, `only admins can use this command.` example:
`u_kick` `PlayerName` `Reason`

`getIP` - Get the player's IP on the server, `only admins can use this command.` example:
`u_getIP` `PlayerName`


`getstructurescount` - Get the number of structures on the server, example:
`u_getstructurescount`

`getzombiecount` - Get the number of zombies on the server, example:
`u_getzombiecount`

`getanimalcount` - Get the number of animals on the server, example:
`u_getanimalcount`

`killallanimals` - Kill all animals on the server, example:
`u_killallanimals`

`killallzombies` - Kill all zombies on the server, example:
`u_killallzombies`

`playerslist` - Get the list of player names on the server, example:
`u_playerslist`

`respawnallnpc` - Respawn all NPC on the server, example:
`u_respawnallnpc`

`tp` - Teleport player to your x y z location, example:
`u_tp` `playername` `x` `y` `z`

`gps` - Get the player's location on image, example:
`u_gps` `PlayerName`

`zombiesdump` - Get the location of all zombies on the server, example:
`u_zombiesdump`

`animalsdump` - Get the location of all animals on the server, example:
`u_animalsdump`

`structuresdump` - Get the location of all structures on the server, example:
`u_structuresdump`

`playersdump` - Get the location of all players on the server, example:
`u_playersdump`

`announce` - Announce message on the server, example:
`u_announce` `Message`

`gettime` - Get time on the server, example:
`u_gettime`

`dumpall` - Get the location of players+zombies+animals+structures on the server, example:
`u_dumpall`

# [Pics] Configurations
`zombie` - Zombie image path

`animal` - Animal image path

`player` - Player image path

`chart` - Chart image path

`structures` - Structures image path

`barricades` - Barricades image path

# [Network] Configurations
`ServerIP` - Unturned Server IP

`ServerCommandsPort` - Unturned RCON Port

`ServerCommandsLogin` - Unturned RCON Login

`ServerCommandsPassword` - Unturned RCON Password

# [AdminSettings] Configurations
`AdminRole` - Discord Unturned Admin Role Name

`VIPRole` - Discord Unturned VIP Role Name

# [ChatSettings] Configurations
`ChatEnabled` - true/false enable/disable chat

`ServerChatPort` - Unturned Server Chat Port

`LogChannelID` - Unturned Log Channel ID

`ChatChannelID` - Unturned Chat Channel ID

`ServerChatPassword` - Unturned Chat Password
