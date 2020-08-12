from requests import get
from telegram.ext import Updater , CommandHandler, MessageHandler, Filters
import logging
import random
import os
from bs4 import BeautifulSoup
TOKEN = os.environ.get("TOKEN")
PORT = os.environ.get("PORT",5000)
def start(update,context):
    message = "Hi!! {} , To get random verse of Srimadbhagavad Gita send /verse.To get a specific verse send /verse <verse no.> <chapter no.> .\n \nadd 'hi' or 'en' or both with command to get translation and 'hic' and 'enc' for commentaries also.\nExamples : /verse 1 4 (verse 1 from chapter 2)\n ,/verse 1 (random verse from chapter 1)\n ,/verse (random verse)\nBot developed by @TheShubhendra \nContent credit : www.gitasupersite.iitk.ac.in".format(update.message.from_user.first_name)  
    context.bot.send_message(update.message.chat_id,message)

def verse(update,context):
  text = update.message.text
  print(text)
  text=text.split()
  hi=en=hic=enc=0
  if "hi" in text:
   text.remove("hi")
   hi =  1
  if "en" in text:
   en = 1
   text.remove("en")
  if "hic" in text:
   hic = 1
   text.remove("hic")
  if "enc" in text:
   enc = 1
   text.remove("enc")
  if len(text)==1:
    v = random.randint(1,48)
    c = random.randint(1,18)
  elif len(text) == 2:
    v = random.randint(1,48)
    c = int(text[1])
  else:
    v = int(text[1])
    c = int(text[2])
  
  url = "https://www.gitasupersite.iitk.ac.in/srimad?language=dv&field_chapter_value={}&field_nsutra_value={}&htrskd={}&etsiva={}&hcchi={}&ecsiva={}".format(c,v,hi,en,hic,enc)
  soup = BeautifulSoup(get(url).text)
  con = soup.select("font")
  for i in range(1,(1+hi+en+hic+enc)*2,2):
    context.bot.send_message(update.message.chat_id,con[i].getText())
def main():  
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  updater = Updater(TOKEN,use_context=True)
  dispatcher = updater.dispatcher

  handler = CommandHandler('verse',verse)
  start_handler = CommandHandler('start',start)
  dispatcher.add_handler(handler)
  dispatcher.add_handler(start_handler)

  updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
  updater.bot.setWebhook("https://shrimad-bhagwat-gita-bot.herokuapp.com/" + TOKEN)
#  updater.start_polling()
  updater.idle()
if __name__ == '__main__':
  main()
