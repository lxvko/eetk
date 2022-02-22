from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import (MessageCantBeDeleted, MessageToDeleteNotFound)
from contextlib import suppress
from collect_data_weekly import collect_data_weekly
from collect_data_daily import collect_data_daily
from collect_kitties import collect_kitty
import time
import asyncio

bot = Bot(token='5085326595:AAFI3xs2njh8QS_Ymz_Mc0m8kvNSw0i8LRc', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


# 5068878742:AAEB6rC4kEmngswkQS6n31fAVR3szf7NshE

# 760196701 author

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Расписание', 'Изменения', 'Милый котик']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите нужный запрос', reply_markup=keyboard)


@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    current_user_id = message.from_user.id
    with open('user_id.txt') as file:
        user_id = [line.strip() for line in file]

    if str(current_user_id) in user_id:
        await message.answer('Ты уже подписан на рассылку!')
    else:
        await message.answer('Теперь ты подписан на рассылку 😊\nЕсли захочешь отписаться, то напиши /leave')
        user_id.append(current_user_id)

    with open("user_id.txt", "w") as file:
        for user in user_id:
            print(user, file=file)


@dp.message_handler(commands=['leave'])
async def leave(message: types.Message):
    current_user_id = message.from_user.id
    with open('user_id.txt') as file:
        user_id = [line.strip() for line in file]

    try:
        user_id.remove(str(current_user_id))
        await message.answer('Ты отписался от рассылки 🥺')
    except ValueError:
        await message.answer('Но ведь тебя и так нет в рассылке!')

    with open("user_id.txt", "w") as file:
        for user in user_id:
            print(user, file=file)


@dp.message_handler(commands=['spisok'])
async def spisok(message: types.Message):
    with open('user_id.txt') as file:
        user_id = [line.strip() for line in file]

    for i in range(len(user_id)):
        await message.answer(f'{user_id[i]}')


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(Text(equals='Расписание'))
async def get_data_weekly(message: types.Message):
    msg = await message.answer('Загрузка. Подожди, пожалуйста 🙃')
    asyncio.create_task(delete_message(msg, 2))

    collect_data_weekly()
    with open('texts/schedules.txt') as file:
        schedule = [line.strip() for line in file]
    with open('texts/schedules_names.txt') as file:
        schedule_name = [line.strip() for line in file]

    for i in range(len(schedule)):
        part = schedule[i].rpartition('/')[-1]
        await message.answer_document(
            open(f'pdfs/{part}.pdf', 'rb'),
            caption=f'{schedule_name[i]}')


@dp.message_handler(Text(equals='Изменения'))
async def get_data_daily(message: types.Message):
    msg = await message.answer('Загрузка. Подожди, пожалуйста 🙃')
    asyncio.create_task(delete_message(msg, 2))

    collect_data_daily()
    with open('texts/changes.txt') as file:
        changes = [line.strip() for line in file]
    with open('texts/changes_names.txt') as file:
        changes_names = [line.strip() for line in file]

    counter = -1
    for change in changes:
        counter += 1
        if 'cloud.mail.ru' in change:
            part = changes[counter].rpartition('/')[-1]
            try:
                await message.answer_document(
                    open(f'pdfs/{part}.pdf', 'rb'),
                    caption=f'{changes_names[counter]}')
                await message.answer_photo(
                    open(f'pdfs/{part}.jpg', 'rb'),
                    caption=f'{changes_names[counter]}')
            except:
                pass
        else:
            await message.answer_document(
                open(f'pdfs/{changes_names[counter]}.pdf', 'rb'),
                caption=f'{changes_names[counter]}')


@dp.message_handler(Text(equals='Милый котик'))
async def get_kitty(message: types.Message):
    collect_kitty()
    await message.answer_photo(
        open('cats/kitty.jpg', 'rb'))


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
