from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from config import Token
import config
from pars import News
from sqlighter import SQLighter
import asyncio
import aioschedule


bot = Bot(token=Token)
dp = Dispatcher(bot)
news = News('check.txt')
db = SQLighter('db.db')

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЧтобы получать новости подпишитесь на рассылку!\n/subscribe\n/help - помощь, для Санька, а то хер разберется)", reply_markup=config.keyboard1)

@dp.message_handler(commands=['help'])
async def help_comand(message: types.Message):
    await message.reply('Выберите команду \n\n /subscribe - подписаться на рассылку \n /unsubscribe - отписаться от рассылки \n /start - перезапустить бота')


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, True)
	
	await message.answer("Вы успешно подписались на рассылку!\nКак будет новость я маякну!")

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")


@dp.message_handler()
async def echo_message(msg: types.Message):
    if msg.text == 'Показать последнюю новость':
        await msg.reply(news.check_last(), reply_markup=config.keyboard2)

@dp.callback_query_handler()
async def see_more(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query_id= callback_query.id)
	await bot.send_message(callback_query.from_user.id, news.full_news())
    		


db = SQLighter('db.db')

async def scheduled():
		subscriptions = db.get_subscriptions()
		a = news.check_point()
		b = news.read_check()
		if a!=b:
			for s in subscriptions:
				await bot.send_message(s[1], text=news.check_news1(), reply_markup=config.keyboard2)
				news.write_check_point()
				print(f'Send to {s[1]} done!')


async def scheduler1():
    aioschedule.every(1).minutes.do(scheduled)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(x):
    asyncio.create_task(scheduler1())



# запускаем лонг поллинг
if __name__ == '__main__':
	executor.start_polling(dp, on_startup=on_startup)
