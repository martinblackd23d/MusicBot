# MusicBot
Discord bot to play music from YouTube

Uses [youtube-dl](https://github.com/ytdl-org/youtube-dl) and the [discord.py](https://discordpy.readthedocs.io/en/stable/) wrapper for the Discord API.

The bot:
- connects to a Discord server
- listens to commands in chat
- connects to voicechat to play audio
- streams audio from YouTube (while it's not utilized, I built functionality for downloading and caching songs)
- commands include: connecting to and disconnecting from voice channels, pausing and resuming songs, creating and editing a queue of songs to be played, playing songs from a URL or searching YouTube for them
- uses env file to store API credentials for added safety
- uses AsyncIO to handle commands asynchronously
- uses threading to simultaneously download and cache songs
- uses logging to create log file
