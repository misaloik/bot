from __future__ import unicode_literals
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram import types
import yt_dlp
import os
import time
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = Bot(token=os.environ.get("TOKEN")) #ваш токен
dp = Dispatcher(bot)

class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
	def __init__(self):
		super(FilenameCollectorPP, self).__init__(None)
		self.filenames = []

	def run(self, information):
		self.filenames.append(information["filepath"])
		return [], information



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	await message.reply("Вітаю!\n /mp4 для завантаження відео за посиланням\n /mp3 для завантаження аудіо за посиланням \n /vid для завантаження відео по назві \n /sea для пошуку аудіo по назві відео")



@dp.message_handler(commands=['sea'])
async def search(message: types.Message):
  arg = message.get_args()
  await message.reply('зачекайте...')
  YDL_OPTIONS = {'format': 'bestaudio/best',
    'noplaylist':'True',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192'
    }],
  }
  with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
    try:
      get(arg) 
    except:
      filename_collector = FilenameCollectorPP()
      ydl.add_post_processor(filename_collector)
      video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
      await message.reply_document(open(filename_collector.filenames[0], 'rb'))
      await message.reply(f'Успішно відправлено!')
      time.sleep(5)
      os.remove(filename_collector.filenames[0])
      
    else:
      video = ydl.extract_info(arg, download=True)
    
    return filename_collector.filenames[0]


@dp.message_handler(commands=['mp3'])
async def youtube(message: types.Message): 
    arguments = message.get_args()
    await message.reply("Зачекайте...")
    ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
	    filename_collector = FilenameCollectorPP()
	    ydl.add_post_processor(filename_collector)
	    ydl.download([arguments])
		
		
	    await message.reply_document(open(filename_collector.filenames[0], 'rb'))
	    await message.reply(f'Файл відправлено!\nДякую за користування бота')
	    time.sleep(5)
	    os.remove(filename_collector.filenames[0])
	    return filename_collector.filenames[0]
@dp.message_handler(commands=['mp4'])
async def search(message: types.Message):
  arg = message.get_args()
  await message.reply('зачекайте...')
  ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
      get(arg) 
    except:
      filename_collector = FilenameCollectorPP()
      ydl.add_post_processor(filename_collector)
      video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
      await message.reply_document(open(filename_collector.filenames[0], 'rb'))
      await message.reply(f'Успішно відправлено!')
      time.sleep(5)
      os.remove(filename_collector.filenames[0])
      
    else:
      video = ydl.extract_info(arg, download=True)
    
    return filename_collector.filenames[0]

@dp.message_handler(commands=['vid'])
async def search_video(message: types.Message):
  arg = message.get_args()
  await message.reply('зачекайте...')
  YDL_OPTIONS = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }

  with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
    try:
      get(arg) 
    except:
      filename_collector = FilenameCollectorPP()
      ydl.add_post_processor(filename_collector)
      video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
      await message.reply_document(open(filename_collector.filenames[0], 'rb'))
      await message.reply(f'Успішно відправлено!')
      time.sleep(5)
      os.remove(filename_collector.filenames[0])
      
    else:
      video = ydl.extract_info(arg, download=True)
    
    return filename_collector.filenames[0]


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)