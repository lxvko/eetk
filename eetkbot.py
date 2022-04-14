from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from collect_data_weekly import collect_data_weekly
from collect_data_daily import collect_data_daily
from collect_kitties import collect_kitty
import asyncio
import glob
import os


# Вводим токен нашего бота
bot = Bot(token='', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


# 760196701 Это я)) @lxvko

# Обработчик команды /start
@dp.message_handler(commands='start')
async def start(message: types.Message):
    # Создание кнопок для выбора курсов
    start_buttons = ['Первый курс', 'Второй курс', 'Третий курс', 'Четвертый курс']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for start_button in start_buttons:
        keyboard.add(start_button)

    # Отправка сообщения пользователю
    await message.answer('Выбери нужный курс', reply_markup=keyboard)


# Обработчик команды "Вернуться к выбору курсов"
@dp.message_handler(Text(equals='Вернуться к выбору курсов'))
async def comeback(message: types.Message):
    # Создание кнопок для выбора курсов
    start_buttons = ['Первый курс', 'Второй курс', 'Третий курс', 'Четвертый курс']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for start_button in start_buttons:
        keyboard.add(start_button)

    # Отправка сообщения пользователю
    await message.answer('Выбери нужный курс', reply_markup=keyboard)


# Обработчик команды "/join"
@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    # Бот берет id пользователя, написавшего команду
    current_user_id = message.from_user.id
    # Подгружает базу данных пользователей рассылки из файла
    with open('user_id.txt') as file:
        user_id = [line.strip() for line in file]

    # Если такой пользователь уже есть в базе данных
    if str(current_user_id) in user_id:
        await message.answer('Ты уже подписан на рассылку!')
    # Если нет в базе данных
    else:
        await message.answer('Теперь ты подписан на рассылку 😊\nЕсли захочешь отписаться, то напиши /leave')
        user_id.append(current_user_id)

    # Сохраняет базу данных пользователей, подписавшихся на рассылку
    with open("user_id.txt", "w") as file:
        for user in user_id:
            print(user, file=file)


# Обработчик команды "/leave"
@dp.message_handler(commands=['leave'])
async def leave(message: types.Message):
    # Бот берет id пользователя, написавшего команду
    current_user_id = message.from_user.id
    # Подгружает базу данных пользователей рассылки из файла
    with open('user_id.txt') as file:
        user_id = [line.strip() for line in file]

    # Пробует удалить пользователя из базы данных
    try:
        user_id.remove(str(current_user_id))
        await message.answer('Ты отписался от рассылки 🥺')
    except ValueError:
        await message.answer('Но ведь тебя и так нет в рассылке!')

    # Сохраняет базу данных
    with open("user_id.txt", "w") as file:
        for user in user_id:
            print(user, file=file)


# Обработчик секретной команды "/spisok"
@dp.message_handler(commands=['spisok'])
async def spisok(message: types.Message):
    # Открываем базу данных пользователей и выводим их в чат с пользователем
    with open('user_id.txt') as file:
        user_id = [line.strip() for line in file]

    await message.answer(f'{len(user_id)}')


# Обработчик секретной команды "/preload"
@dp.message_handler(commands=['preload'])
async def spisok(message: types.Message):
    await message.answer('Загрузка. Подожди, пожалуйста 🙃')

    # Удаляем все файлы из папки pdfs
    for file in glob.glob('pdfs/*'):
        os.remove(file)

    # Скачиваем актуальные файлы изменений
    collect_data_daily()
    course = 1
    # Скачиваем актуальные файлы расписания для всех курсов
    for course in range(1, 5):
        await asyncio.sleep(2)
        try:
            collect_data_weekly(course)
            await message.answer(f'{course} курс успешно загружен 🙃')
        except:
            await message.answer(f'Ой, что-то сломалось с {course} курсом :(')


# Тут просто копипаст с минимальными изменениями для каждого курса, 
@dp.message_handler(Text(equals='Первый курс'))
async def first_course_is_selected(message: types.Message):
    first_course = ['Расписание первого курса', 'Изменения']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*first_course)
    keyboard.add('Вернуться к выбору курсов')
    await message.answer('Теперь сделай запрос', reply_markup=keyboard)


@dp.message_handler(Text(equals='Второй курс'))
async def second_course_is_selected(message: types.Message):
    second_course = ['Расписание второго курса', 'Изменения']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*second_course)
    keyboard.add('Вернуться к выбору курсов')
    await message.answer('Теперь сделай запрос', reply_markup=keyboard)


@dp.message_handler(Text(equals='Третий курс'))
async def third_course_is_selected(message: types.Message):
    third_course = ['Расписание третьего курса', 'Изменения']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*third_course)
    keyboard.add('Вернуться к выбору курсов')
    await message.answer('Теперь сделай запрос', reply_markup=keyboard)


@dp.message_handler(Text(equals='Четвертый курс'))
async def fourth_course_is_selected(message: types.Message):
    fourth_course = ['Расписание четвертого курса', 'Изменения']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*fourth_course)
    keyboard.add('Вернуться к выбору курсов')
    await message.answer('Теперь сделай запрос', reply_markup=keyboard)


# Копипаст с минимальными изменениями для каждого курса
@dp.message_handler(Text(equals='Расписание первого курса'))
async def get_data_weekly_first(message: types.Message):
    await message.answer('Загрузка. Подожди, пожалуйста 🙃')

    # Сохраняем pdf-файлы для первого курса
    collect_data_weekly(1)
    # Открываем названия файлов и ссылки
    with open('texts/schedules.txt') as file:
        schedule = [line.strip() for line in file]
    with open('texts/schedules_names.txt') as file:
        schedule_name = [line.strip() for line in file]

    # Отправляем файлы пользователю
    for i in range(len(schedule)):
        part = schedule[i].rpartition('/')[-1]
        await message.answer_document(
            open(f'pdfs/{part}.pdf', 'rb'),
            caption=f'{schedule_name[i]}')
        await asyncio.sleep(0.5)


@dp.message_handler(Text(equals='Расписание второго курса'))
async def get_data_weekly_second(message: types.Message):
    await message.answer('Загрузка. Подожди, пожалуйста 🙃')

    collect_data_weekly(2)
    with open('texts/schedules.txt') as file:
        schedule = [line.strip() for line in file]
    with open('texts/schedules_names.txt') as file:
        schedule_name = [line.strip() for line in file]

    for i in range(len(schedule)):
        part = schedule[i].rpartition('/')[-1]
        await message.answer_document(
            open(f'pdfs/{part}.pdf', 'rb'),
            caption=f'{schedule_name[i]}')
        await asyncio.sleep(0.5)


@dp.message_handler(Text(equals='Расписание третьего курса'))
async def get_data_weekly_third(message: types.Message):
    await message.answer('Загрузка. Подожди, пожалуйста 🙃')

    collect_data_weekly(3)
    with open('texts/schedules.txt') as file:
        schedule = [line.strip() for line in file]
    with open('texts/schedules_names.txt') as file:
        schedule_name = [line.strip() for line in file]

    for i in range(len(schedule)):
        part = schedule[i].rpartition('/')[-1]
        await message.answer_document(
            open(f'pdfs/{part}.pdf', 'rb'),
            caption=f'{schedule_name[i]}')
        await asyncio.sleep(0.5)


@dp.message_handler(Text(equals='Расписание четвертого курса'))
async def get_data_weekly_fourth(message: types.Message):
    await message.answer('Загрузка. Подожди, пожалуйста 🙃')

    collect_data_weekly(4)
    with open('texts/schedules.txt') as file:
        schedule = [line.strip() for line in file]
    with open('texts/schedules_names.txt') as file:
        schedule_name = [line.strip() for line in file]

    for i in range(len(schedule)):
        part = schedule[i].rpartition('/')[-1]
        await message.answer_document(
            open(f'pdfs/{part}.pdf', 'rb'),
            caption=f'{schedule_name[i]}')
        await asyncio.sleep(0.5)


# Обработчик команды "Изменения"
@dp.message_handler(Text(equals='Изменения'))
async def get_data_daily(message: types.Message):
    await message.answer('Загрузка. Подожди, пожалуйста 🙃')

    # Сохраняем pdf-файлы изменений
    collect_data_daily()
    # Подгружаем имена файлов, ссылки и форматы файлов
    with open('texts/changes.txt') as file:
        changes = [line.strip() for line in file]
    with open('texts/changes_names.txt') as file:
        changes_names = [line.strip() for line in file]
    with open('texts/temp_formats.txt') as file:
        temp_formats = [line.strip() for line in file]

    counter = -1
    for change in changes:
        counter += 1
        await asyncio.sleep(0.5)
        # Отправляем файлы пользователю с интервалом пол секунды
        if 'cloud.mail.ru' in change:
            part = changes[counter].rpartition('/')[-1]
            if temp_formats[counter] == 'pdf':
                await message.answer_document(
                    open(f'pdfs/{part}.pdf', 'rb'),
                    caption=f'{changes_names[counter]}')
            elif temp_formats[counter] == 'jpg':
                await message.answer_document(
                    open(f'pdfs/{part}.jpg', 'rb'),
                    caption=f'{changes_names[counter]}')
            elif temp_formats[counter] == 'png':
                await message.answer_document(
                    open(f'pdfs/{part}.png', 'rb'),
                    caption=f'{changes_names[counter]}')
        else:
            await message.answer_document(
                open(f'pdfs/{changes_names[counter]}.pdf', 'rb'),
                caption=f'{changes_names[counter]}')


# Обработчик секретной команды "Милый котик"
@dp.message_handler(Text(equals='Милый котик'))
async def get_kitty(message: types.Message):
    # Сохраняем котика
    collect_kitty()
    # Отправляем котика
    await message.answer_photo(open('cats/kitty.jpg', 'rb'))


# Запускаем бота
def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
