import asyncio
import random
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

from .botkey import key
from .generate import generate
from .document import Document
from .models import DocumentModel

"""
$ python3.5 skeletona_route.py <token>

It demonstrates:
- passing a routing table to `MessageLoop` to filter flavors.
- the use of custom keyboard and inline keyboard, and their various buttons.

Remember to `/setinline` and `/setinlinefeedback` to enable inline mode for your bot.

It works like this:

- First, you send it one of these 4 characters - `c`, `i`, `h`, `f` - and it replies accordingly:
    - `c` - a custom keyboard with various buttons
    - `i` - an inline keyboard with various buttons
    - `h` - hide custom keyboard
    - `f` - force reply
- Press various buttons to see their effects
- Within inline mode, what you get back depends on the **last character** of the query:
    - `a` - a list of articles
    - `p` - a list of photos
    - `b` - to see a button above the inline results to switch back to a private chat with the bot
"""
TOKEN = key
message_with_inline_keyboard = None

bot = telepot.aio.Bot(TOKEN)
answerer = telepot.aio.helper.Answerer(bot)


async def bind_photo_path_to_document(message_id, file_path):
    dm = await DocumentModel.findAll(where="message_id=%d"%message_id)
    dm.image += file_path
    dm.update()


async def add_photo(msg):
    if 'reply_to_message' in msg.keys():
            message_id = msg['reply_to_message']['message_id']
            photo_id = msg['photo'][-1]['file_id']
            photo_file = await bot.getFile(file_id=photo_id)
            file_path = photo_file['file_path']
            await bot.download_file(file_id=photo_id, dest=file_path)
            bind_photo_path_to_document(message_id=message_id)
    else:
        chat_id = msg['from']['id']
        await bot.sendMessage(chat_id, "请选定要绑定的课")   

    

async def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    message_id = msg['message_id']
    print('Chat:', content_type, chat_type, chat_id)

    if content_type=='photo':
        print(msg)
        # assert msg.reply_to_message
        photo = await add_photo(msg)
        print(photo)

    if content_type != 'text':
        return

    command = msg['text'].lower()

    if command == '/start':
        lrp = generate()
        print(lrp)
        markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='起课'), KeyboardButton(text='添加图片')]])
        await bot.sendMessage(chat_id, str(lrp), reply_markup=markup)        
    
    elif command == "起课":
        lrp = generate()
        await bot.sendMessage(chat_id, str(lrp))        

    elif command == 'c':
        markup = ReplyKeyboardMarkup(keyboard=[
                     ['Plain text', KeyboardButton(text='Text only')],
                     [dict(text='Phone', request_contact=True), KeyboardButton(text='Location', request_location=True)],
                 ])
        await bot.sendMessage(chat_id, 'Custom keyboard with various buttons', reply_markup=markup)
    elif command == 'i':
        markup = InlineKeyboardMarkup(inline_keyboard=[
                     [dict(text='Telegram URL', url='https://core.telegram.org/')],
                     [InlineKeyboardButton(text='Callback - show notification', callback_data='notification')],
                     [dict(text='Callback - show alert', callback_data='alert')],
                     [InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
                     [dict(text='Switch to using bot inline', switch_inline_query='initial query')],
                 ])

        # global message_with_inline_keyboard
        # message_with_inline_keyboard = await bot.sendMessage(chat_id, 'Inline keyboard with various buttons', reply_markup=markup)

    elif command == 'h':
        markup = ReplyKeyboardRemove()
        await bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)
    elif command == 'f':
        markup = ForceReply()
        await bot.sendMessage(chat_id, 'Force reply', reply_markup=markup)
    
    else:
        pass
        document = Document(command)
        await document.save_to_database(message_id=message_id)

        markup = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='添加图片', callback_data='add_image'), InlineKeyboardButton(text='修改时间', callback_data='edit_time')],
                 ])

        global message_with_inline_keyboard
        message_with_inline_keyboard = await bot.sendMessage(chat_id, str(document.get_text()), reply_markup=markup)


async def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)

    if data == 'notification':
        await bot.answerCallbackQuery(query_id, text='Notification at top of screen')
    elif data == 'alert':
        await bot.answerCallbackQuery(query_id, text='Alert!', show_alert=True)
    elif data == 'edit':
        global message_with_inline_keyboard

        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            await bot.editMessageText(msg_idf, 'NEW MESSAGE HERE!!!!!')
        else:
            await bot.answerCallbackQuery(query_id, text='No previous message to edit')
    elif data == 'add_image':
        await bot.answerCallbackQuery(query_id, text='请发送图片')

def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Computing for: %s' % query_string)

        articles = [InlineQueryResultArticle(
                        id='abcde', title='Telegram', input_message_content=InputTextMessageContent(message_text='Telegram is a messaging app')),
                    dict(type='article',
                        id='fghij', title='Google', input_message_content=dict(message_text='Google is a search engine'))]

        photo1_url = 'https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf'
        photo2_url = 'https://www.telegram.org/img/t_logo.png'
        photos = [InlineQueryResultPhoto(
                      id='12345', photo_url=photo1_url, thumb_url=photo1_url),
                  dict(type='photo',
                      id='67890', photo_url=photo2_url, thumb_url=photo2_url)]

        result_type = query_string[-1:].lower()

        if result_type == 'a':
            return articles
        elif result_type == 'p':
            return photos
        else:
            results = articles if random.randint(0,1) else photos
            if result_type == 'b':
                return dict(results=results, switch_pm_text='Back to Bot', switch_pm_parameter='Optional_start_parameter')
            else:
                return dict(results=results)

    answerer.answer(msg, compute)


def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)
