import os
import time
import discord
from dotenv import load_dotenv
import random
import logging
import asyncio
import youtube_dl
from discord.ext import commands
import requests
import threading
import typing
import functools

##############
#logger setup#
##############

logger = logging.getLogger("discord")
#logger.setLevel(logging.INFO) # Do not allow DEBUG messages through
handler = logging.FileHandler(filename="C:\\Users\\Martin\\Desktop\\Projects\\Unnamed Bot\\bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("{asctime}: {levelname}: {name}: {message}", style="{"))
logger.addHandler(handler)

#############

class ydl_logger(object):
	def debug(self, msg):
		#print(msg)
		pass
	def warning(self, msg):
		print(msg)
	def error(self, msg):
		print(msg)

def ydl_hook(d):
	print(d['status'])
	if d['status'] == 'finished':
		print('Done downloading, now converting...')

##################
#logger setup end#
##################

#############
#queue setup#
#############
class track():
	url = ''
	#file_location = ''
	#is_downloaded = False
	#id = 0
	title = ''

#audiodir = 'C:\\Users\\Martin\\Desktop\\Projects\\Unnamed Bot\\Audio\\'
#current_id = 0
current_index = 0
queue = []
is_playing = False
is_villager = False
#is_in_play_loop = False
#dl_queue = []


#print(sound_files)
#print('\n')

#################
#queue setup end#
#################

###########
#ydl setup#
###########
#is_downloading = False

#queue_dl = []

ydl_opts = {
	'format': 'bestaudio/best',
	'noplaylist': 'True',
#	'download_archive': 'C:\\Users\\Martin\\Desktop\\Projects\\Unnamed Bot\\downloaded_songs.txt',
	#'outtmpl': 'C:\\Users\\Martin\\Desktop\\Projects\\Unnamed Bot\\Audio\\%(title)s.%(ext)s',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192'
		}],
	'logger': ydl_logger(),
	'progress_hooks': [ydl_hook]
	}

#with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#	ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])
###############
#ydl setup end#
###############

###############
#discord setup#
###############
vclient = None
main_ctx = None

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='-')

###################
#discord setup end#
###################


################
#discord events#
################
@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!\n')

@bot.event
async def on_error(event, *args, **kwargs):

	print(event)

	print('\nargs:\n')
	for i in args:
		print(i)

	print('\nkwargs:\n')
	for i in kwargs:
		print(i)

	print('\nkwargs values:\n')
	for i in kwargs.values:
		print(i)

@bot.event
async def on_command_error(ctx, exception):
	print(ctx)
	await ctx.send(exception)

##############
#bot commands#
##############

#test
@bot.command(name='test', help='prints a text message')
async def help(ctx):
	await ctx.send('text message')

#raise-exception
@bot.command(name='raise_exception')
async def raiseexception(ctx):
	raise discord.DiscordException

#join
@bot.command(name='join', help='joins to your voice channel')
async def connect(ctx):
	global vclient
	global main_ctx

	if ctx.author.voice == None:
		await ctx.send('You\'re not in any voice channel')
	else:
		channel = ctx.author.voice.channel
		main_ctx = ctx
		if vclient == None:
			vclient = await channel.connect()
		elif vclient.is_connected():
			await vclient.move_to(channel)
		else:
			vclient = await channel.connect()

	#with open('C:\\Users\\Martin\\Desktop\\Projects\\Unnamed Bot\\Rick Astley - Never Gonna Give You Up (Official Music Video)-dQw4w9WgXcQ.mp3') as f:
	#	await vclient.play(discord.FFmpegPCMAudio(f, pipe = True))
	#await queue_master()

@bot.command(name = 'VillagerMode')
async def villager(ctx):
	global is_villager
	if is_villager:
		is_villager = False
		await ctx.send('Villager mode deactivated')
	else:
		is_villager = True
		try:
			vclient.stop()
		except:
			pass
		await ctx.send('Villager mode activated')
		await villager()

@bot.command(name = 'play')
async def play(ctx, *arg):
	if vclient == None or not vclient.is_connected():
		await connect(ctx)
#	global is_in_play_loop
	query = ' '.join(arg)
	if query != '':
		msg = await queue_add(query, -1)
		await ctx.send(msg)
#	if not is_in_play_loop:
#		is_in_play_loop = True
	msg = await play_next()
	if msg != '' and msg != None:
		await ctx.send(msg)
	#await play(ctx)

@bot.command(name = 'skip')
async def skip(ctx):
	vclient.stop()

@bot.command(name = 'pause')
async def pause(ctx):
	vclient.pause()

@bot.command(name = 'resume')
async def resume(ctx):
	vclient.resume()

@bot.command(name = 'disconnect')
async def disconnect(ctx):
	global vclient
	global is_playing

	await vclient.disconnect()
	vclient = None
	is_playing = False


######################
#discord commands end#
######################

async def villager():
	dir = 'C:\\Users\\Martin\\Desktop\\Projects\\Unnamed Bot\\VillagerAudio\\'
	samples = [
		'Villager_accept1.oga',
		'Villager_accept2.ogg',
		'Villager_death.oga',
		'Villager_deny1.oga',
		'Villager_deny2.ogg',
		'Villager_hurt1.oga',
		'Villager_hurt2.ogg',
		'Villager_idle1.oga',
		'Villager_trade1.oga',
		'Villager_trade2.ogg',
		]
	with open(dir + samples[7]) as f:
		try:
			vclient.play(discord.FFmpegPCMAudio(f, pipe = True))
			await asyncio.sleep(5)
			vclient.play(discord.FFmpegPCMAudio(f, pipe = True))
		except Exception as e:
			print(e)

	random.shuffle(samples)
	counter = 0
	while True:
		try:
			await asyncio.sleep(300 + random.randrange(900))
			if not is_villager:
				break
			with open(dir + samples[counter]) as f:
				vclient.play(discord.FFmpegPCMAudio(f, pipe = True))
			counter += 1
			if counter == 10:
				counter = 0
		except Exception as e:
			print(e)

#############
#ydl manager#
#############

#unused
async def dl_manager():
	global is_downloading

	while True:
		if is_downloading:
			await asyncio.sleep(1)
		else:
			#print(queue)
			for t in queue:
				if t.is_downloaded:
					continue
				else:
					ydl_opts['outtmpl'] = audiodir + str(t.id) + '.%(ext)s'
					#print('before threading')
					t.is_downloaded = True
					t.file_location = audiodir + str(t.id) + '.mp3'
					print('Started downloading\nTitle: ' + t.title + '\nURL: ' + t.url + '\nID: ' + str(t.id) +'\n')
					try:
						th = threading.Thread(target = threaded_download, args = (t.url))
						th.start()
					except Exception as e:
						print(e)
					is_downloading = True
					print('after threading')
					break
			await asyncio.sleep(1)

#unused
def threaded_download(*args, **kwargs):
	global is_downloading

	url = ''
	for i in args:
		url += i
	#print(url)
	#print('entered threaded_download function')
	start = time.time()
	#with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	#	ydl.download([url])
	end = time.time()
	print('Finished downloading\nURL: ' + url + '\nTime taken: ' + str(end - start) + ' s\n')
	try:
		is_downloading = False
	except Exception as e:
		print('e')
	#else:
		#print('thread exited successfully')
	

#################
#ydl manager end#
#################

#######
#queue#
#######


def to_thread(func: typing.Callable) -> typing.Coroutine:
	@functools.wraps(func)
	async def wrapper(*args, **kwargs):
		#print(args)
		#print(kwargs)
		loop = asyncio.get_event_loop()
		wrapped = functools.partial(func, *args, **kwargs)
		return await loop.run_in_executor(None, wrapped)
	return wrapper


@to_thread
def video_info(keyword):
	#print('in_function')
	#print(keyword)
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try:
			requests.get(keyword)
			#video = ydl.extract_info(keyword, download = False)
		except:
			video = ydl.extract_info(f'ytsearch:{keyword}', download = False)['entries'][0]
			#print('video from search')
		else:
			video = ydl.extract_info(keyword, download = False)
			#print('video from URL')
	return video



async def queue_add(keyword, position):
	#global current_id
	#keywordl = [keyword]
	#print(keyword)
	video = await video_info(keyword = keyword)


	#if video['duration'] < 600:
	temp = track()
	temp.url = video['webpage_url']
	temp.title = video['title']
	#temp.id = current_id
	#current_id += 1
	queue.append(temp)
	return 'Queued: {0}'.format(temp.title)
	#else:
	#	return 'Currently videos longer than 10 minutes are not supported'

async def play_next():
	global current_index
	global is_playing
#	global is_in_play_loop

	if len(queue) == 0:
		return 'Queue is empty'
	if not vclient.is_connected():
		return 'Voice client is not connected'
	if vclient.is_playing():
		return ''
	if vclient.is_paused():
		vclient.resume()
		return 'Resumed playback'


	while True:
		if not is_playing and not is_villager:
			is_playing = True

			#if current_index >= len(queue):
			#	current_index = 0
			#temp_index = current_index
			#current_index += 1

			if len(queue) == 0:
				await asyncio.sleep(1)
				is_playing = False
				continue

			#with open(queue[current_index].file_location) as src:
			#	try:
			#		vclient.play(discord.FFmpegPCMAudio(src, pipe = True), after=play_next)
			#	except Exception as e:
			#		print(e)
			#		play_next('')
			FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

			#YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}

			#voice = get(client.voice_clients, guild=ctx.guild)


			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				tempvid = queue.pop()
				#info = ydl.extract_info(queue[temp_index].url, download=False)
				info = ydl.extract_info(tempvid.url, download=False)
				for i in info['formats']:
					if i['format_id'] == '251':
						I_URL = i['url']
				#I_URL = info['formats'][0]['url']
				#print('started probing')
				#print(await discord.FFmpegOpusAudio.probe(I_URL, method='fallback'))
				#source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
				try:
					source = discord.FFmpegPCMAudio(I_URL)
					vclient.play(source, after=play_next_callback)
				except Exception as e:
					print(e)
				if vclient.is_playing():
					#await main_ctx.send('Now playing: {0}'.format(queue[temp_index].title))
					await main_ctx.send('Now playing: {0}'.format(tempvid.title))
				#await play_next()
		await asyncio.sleep(1)

def play_next_callback(error):
	global is_playing

	if error != None:
		raise error
	is_playing = False

#unused
async def queue_master():
	global current_index

	while True:
		if len(queue) == 0:
			await asyncio.sleep(1)
		elif queue[current_index].is_downloaded:
			with open(queue[current_index].file_location) as src:
				vclient.play(src)
		current_index += 1
		if current_index >= len(queue):
			current_index = 0

###########
#queue end#
###########


######
#main#
######

#async def main():
#	fdlm = loop.create_task(dl_manager())
#	#fqm = loop.create_task(queue_master())
#	fbot = loop.create_task(bot.start(TOKEN))
#	await asyncio.wait([fdlm, fbot])

#loop = asyncio.get_event_loop()
#try:
#loop.run_until_complete(main())
#except KeyboardInterrupt:
#	print('keyboard interrupt registered')
#	loop.run_until_complete(bot.close())
#	print('keyboard interrupt successful')
	# cancel all tasks lingering
#finally:
#loop.close()
#client.run(TOKEN)
bot.run(TOKEN)