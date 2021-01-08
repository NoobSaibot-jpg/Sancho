from aiogram import types

Token = '1427303250:AAGFR66QcJN5O4XHFz4Gj45HO3UPpGvvkyY'

keyboard1 = types.ReplyKeyboardMarkup(True, True, False)
keyboard1.row('Показать последнюю новость')

keyboard = types.InlineKeyboardMarkup()
url_button = types.InlineKeyboardButton(text="Перейти на сайт", url='https://bank.gov.ua/WebSelling/Home/News')
keyboard.add(url_button)