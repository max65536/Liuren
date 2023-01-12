import asyncio
import logging
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from botkey import key
from bot_function import on_callback_query, on_chat_message, on_chosen_inline_result, on_inline_query, bot

import orm



async def init(loop):
    await orm.create_pool(loop=loop,host='localhost',port=3306,user='root',password='root',db='liuren')
    logging.info('server started at http://127.0.0.1:9012')


loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, {'chat': on_chat_message,
                                   'callback_query': on_callback_query,
                                   'inline_query': on_inline_query,
                                   'chosen_inline_result': on_chosen_inline_result}).run_forever())
loop.create_task(init(loop=loop))
print('Listening ...')

loop.run_forever()