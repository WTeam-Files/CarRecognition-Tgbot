import requests, telebot, flask, os
def infoo(path):
  url = 'https://carnet.ai/recognize-file'
  headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
      'Accept': '*/*',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate, br',
      'Origin': 'https://carnet.ai',
      'Connection': 'keep-alive',
      'Referer': 'https://carnet.ai/',
      'Cookie': '_ga_ZM4FBGFBK5=GS1.1.1682312433.1.1.1682312988.0.0.0; _ga=GA1.1.1403550793.1682312434; _gid=GA1.2.828671953.1682312434; __stripe_mid=45643645-fde1-4bfa-ab3b-3cd56a83028eec73bf; __stripe_sid=7d130e36-5efa-4faa-b98e-d4f5d32ad067cfd64f',
  }

  files = {'imageFile': ('x.jpg', open(path, 'rb'), 'image/*')}

  response = requests.post(url, headers=headers, files=files)
  return response.json()
# bot token here
bot = telebot.TeleBot("####", num_threads=20, skip_pending=True)

@bot.message_handler(commands=['start'])
def start(m):
  k = '''
👋🏻꒐ اهلا بك في  بوت معرفه نوع السياره!
⏺꒐ قم بأرسال صوره السيارة وسيقوم الذكاء الاصطناعي بتحديد نوع السياره ..
⎯ ⎯ ⎯ ⎯
  '''
  bot.reply_to(m, k)
@bot.message_handler(content_types=['photo'])
def getimg(m):
  fileid = m.photo[-1].file_id
  g = bot.get_file(fileid).file_path
  x = bot.download_file(g)
  with open("img.jpg", 'wb') as e:
    e.write(x)
  x = infoo('img.jpg')
  if x.get('error') !=None:
    bot.reply_to(m, x['error'])
  else:
    carname = x['car']['make']
    carmodel = x['car']['model']
    years = x['car']['years']
    angel = x['angle']['name']
    color = x['color']['name']
    info = f'''
تم التعرف على السيارة 🎉:
🤔 مصنع السيارة : {carname}
🕔 سنة اصدار السيارة: {years}
🟥🟦  لون السيارة: {color}
🚖 زاوية تصوير السيارة: {angel}
📳 اسم السياره (موديلها): {carmodel}
⎯ ⎯ ⎯ ⎯
    '''
    bot.reply_to(m, info)

bot.infinity_polling()
