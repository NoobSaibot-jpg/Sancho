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

db = SQLighter('db.db')
news = News('check.txt')


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
async def last_message(msg: types.Message):
    if msg.text == 'Показать последнюю новость':
        await msg.reply(news.check_last() , reply_markup=config.keyboard)


db = SQLighter('db.db')

async def scheduled(wait_for):
	subscriptions = db.get_subscriptions()
	while True:
		await asyncio.sleep(wait_for)
		new_news = news.read_check()
		old_news = news.check_point()
		text = news.check_news1()
		if new_news != old_news:
				for s in subscriptions:
					await bot.send_message(s[1], text=text, reply_markup=config.keyboard)
				news.write_check_point()
		else:
    			continue

# loop = asyncio.get_event_loop()
# loop.create_task(scheduled(10))


if __name__ == '__main__':
    dp.loop.run_until_complete(scheduled(10))
    executor.start_polling(dp)