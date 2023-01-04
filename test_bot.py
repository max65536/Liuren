import time
import telepot
from telepot.loop import MessageLoop

from generate import generate

from botkey import key 
from IPython import embed

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    # embed()

    if content_type == 'text':
        bot.sendMessage(chat_id, str(generate()))
    #     bot.sendMessage(chat_id, "a\u3000a")
    #     bot.sendMessage(chat_id, "a a")


# TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(key)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.

while 1:
    time.sleep(10)
# embed()