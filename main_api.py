import telebot
import dbworker
import psycopg2
import config
import datetime
import os
import pytz
from telebot import types
from config import Token, admins


# DATABASE_URL = os.environ['postgresql://postgres:QtWLrg4wGHxhxOoLrz8P@containers-us-west-51.railway.app:5774/railway']

# con = psycopg2.connect(DATABASE_URL, sslmode='require')

con = psycopg2.connect(
  database="railway",
  user="postgres",
  password="QtWLrg4wGHxhxOoLrz8P",
  host="containers-us-west-51.railway.app",
  port="5774"
)

cur = con.cursor()
bot = telebot.TeleBot(Token)

cur.execute(f'''CREATE TABLE IF NOT EXISTS sale
                                         (Date TEXT,
                                         Name TEXT,
                                         Text TEXT,
                                         TextNames TEXT,
                                         SalePercent TEXT, 
                                         DateDelta TIMESTAMP,
                                         State TEXT);''')
con.commit()

cur.execute(f'''CREATE TABLE IF NOT EXISTS events
                                 (Id Text,
                                 Name TEXT,
                                 Text TEXT,
                                 ImgName TEXT, 
                                 Price TEXT);''')
con.commit()
cur.execute(f'''CREATE TABLE IF NOT EXISTS claims
                                 (Id TEXT,
                                 ChatId TEXT,
                                 Name TEXT,
                                 Date TEXT,
                                 State TEXT,
                                 NameUser TEXT, 
                                 Price INT,
                                 TextC TEXT);''')
con.commit()

claim_a = {}
claim_p = {}
new_event = {}
edit_event = {}
new_sale = {}

s_events = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in admins:
        cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                             (Name TEXT,
                                                             Date TEXT,
                                                             State TEXT,
                                                             NameUser TEXT, 
                                                             Price INT, 
                                                             AnswerAdmin TEXT);''')
        con.commit()
        buttons = [
            types.InlineKeyboardButton(text="Прайс", callback_data="ClbEvents-A"),
            types.InlineKeyboardButton(text="Все заявки", callback_data="ClbClaims-A"),
            types.InlineKeyboardButton(text="Скидки и акции", callback_data="ClbSale-A"),
            types.InlineKeyboardButton(text="Отправить сообщение", callback_data="ClbSendMChat-A"),
            types.InlineKeyboardButton(text="Бот", callback_data="ClbBot-A")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, 'Панель администратора. По кнопке "Бот" можно зайти в бота, как обычный пользователь...',
                             reply_markup=keyboard)
    else:
        cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                     (Name TEXT,
                                                     Date TEXT,
                                                     State TEXT,
                                                     NameUser TEXT, 
                                                     Price INT, 
                                                     AnswerAdmin TEXT);''')
        con.commit()
        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()
        EventsNames = ''
        for i in range(len(rows)):
            EventsNames += f'{rows[i][1]}\n'
        buttons = [
            types.InlineKeyboardButton(text="Прайс", callback_data="ClbEvents"),
            types.InlineKeyboardButton(text="Помощь", callback_data="ClbHelp"),
            types.InlineKeyboardButton(text="Мои заявки", callback_data="ClbClaims"),
            types.InlineKeyboardButton(text='Наш Instagram', url='https://www.instagram.com/gagra_sup/')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, f'<b>Приветствую! Я GAGRASUPbot</b>'
                                          f'и мне хочется предложить вам отличный способ активно и увлекательно провести свой досуг '
                                          f'- сапбординг. Это увлекательный вид активности, который понравится абсолютно любому - '
                                          f'от взрослых до детей, любителям экстрима и просто желающим приятно провести время на '
                                          f'море или на реке.'
                                          f'\n\n Мы предоставляем <b>качественные и надежные</b> сапборды от известных производителей, '
                                          f'таких как <b>Stormline</b>, <b>Bombitto</b> и другие бренды. '
                                          f'При этом, наш гид обязательно проведет инструктаж перед началом сплава, '
                                          f'а также предоставит спасательные жилеты и водонепроницаемые чехлы для '
                                          f'вашего телефона, чтобы обеспечить вашу безопасность.'
                                          f'\n\nМы предлагаем различные варианты для всех желающих - прокат сапбордов, '
                                          f'организованные прогулки и индивидуальные туры. Вам просто нужно нажать на '
                                          f'кнопку "Прайс" и выбрать наиболее подходящий вариант для себя. '
                                          f'При этом, если погода не будет благоприятной, мы всегда готовы '
                                          f'перенести ваши прогулки на более удобное время.'
                                          f'\n\nНе упускайте возможность открыть для себя новый увлекательный мир морских прогулок - '
                                          f'выберите сапбординг с GAGRASUPbot!', parse_mode='html', reply_markup=keyboard)


@bot.message_handler(commands=['price_list'])
def price_list(message):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                                 (Name TEXT,
                                                                 Date TEXT,
                                                                 State TEXT,
                                                                 NameUser TEXT, 
                                                                 Price INT, 
                                                                 AnswerAdmin TEXT);''')
    con.commit()
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    buttons = [types.InlineKeyboardButton(text=f"{rows[i][1]}", callback_data=f"ClbEvents{rows[i][0]}") for i in
               range(len(rows))]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text=f"Главное меню »", callback_data=f"ClbStart"))
    bot.send_message(chat_id=message.chat.id, text='<b>ПРОГУЛКИ. Выберите подходящий вариант:</b>', parse_mode='html',
                          reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                                     (Name TEXT,
                                                                     Date TEXT,
                                                                     State TEXT,
                                                                     NameUser TEXT, 
                                                                     Price INT, 
                                                                     AnswerAdmin TEXT);''')
    con.commit()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='WhatsApp', url='https://wa.me/+79407322932'),
                 types.InlineKeyboardButton(text='Telegram', url='tg://resolve?domain=danyaagrba'),
                 types.InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/gagra_sup/'),
                 types.InlineKeyboardButton(text=f"Главное меню »", callback_data=f"ClbStart"))
    bot.send_message(chat_id=message.chat.id, text='Вы можете написать нам:', reply_markup=keyboard)


@bot.message_handler(commands=['my_claims'])
def my_claims(message):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                                     (Name TEXT,
                                                                     Date TEXT,
                                                                     State TEXT,
                                                                     NameUser TEXT, 
                                                                     Price INT, 
                                                                     AnswerAdmin TEXT);''')
    con.commit()
    cur.execute(f"SELECT * FROM p{message.chat.id}")
    rows = cur.fetchall()
    buttons = [types.InlineKeyboardButton(text=f"{rows[i][0]} ({'.'.join(rows[i][1].split()[0].split('-')[::-1])})",
                                          callback_data=f"ClbEvents{rows[i][1].split()[0]}_{rows[i][1].split()[1]}")
               for i in
               range(len(rows))]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text=f"Главное меню »", callback_data=f"ClbStart"))
    bot.send_message(chat_id=message.chat.id, text='Выберите название прогулки:', reply_markup=keyboard)


@bot.message_handler(commands=['db_config'])
def db_config(message):
    if message.chat.id in admins:
        cur.execute("""SELECT table_name FROM information_schema.tables
                   WHERE table_schema = 'public'""")
        buttons = [types.InlineKeyboardButton(text=f"{table[0]}", callback_data=f"db_config_{table[0]}") for table in
                   cur.fetchall()]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        bot.send_message(chat_id=message.chat.id, text='Все таблицы бота:', reply_markup=keyboard)


@bot.message_handler(commands=['work_day'])
def work_day(message):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS work 
                                                    (Date TEXT,
                                                    Time TEXT,
                                                    NameEvent TEXT,
                                                    Quantity TEXT,
                                                    Price TEXT,
                                                    PayMethod TEXT,
                                                    BookingTime TEXT,
                                                    WorkerName TEXT);''')
    con.commit()



# Добавление заявки пользователя ----- Добавление заявки пользователя ----- Добавление заявки пользователя ----- Добавление заявки пользователя
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.SendClaim.value)
def user_age(message):
    tz = pytz.timezone('Europe/Moscow')
    dt = datetime.datetime.now(tz)
    date = dt.replace(tzinfo=None)
    user_name = message.chat.username
    cur.execute(f'''INSERT INTO p{message.chat.id} (Name, Date, State, NameUser, Price, AnswerAdmin) VALUES 
                                                                           ('{claim_p[message.chat.id, 'name_event']}', 
                                                                           '{date}', 
                                                                           'На рассмотрении', 
                                                                           '{user_name}', 
                                                                           '{claim_p[message.chat.id, 'price_event']}',
                                                                           ' ');''')
    con.commit()
    cur.execute(f"SELECT * FROM p{message.chat.id}")
    rowssss = cur.fetchall()
    claim_id = f'{message.chat.id}_{len(rowssss)}'
    ttt = message.text
    cur.execute(f'''INSERT INTO claims (Id, ChatId, Name, Date, State, NameUser, Price, TextC) VALUES 
                                                                                       ('{claim_id}',
                                                                                       '{message.chat.id}',
                                                                                       '{claim_p[message.chat.id, 'name_event']}', 
                                                                                       '{date}', 
                                                                                       'На рассмотрении', 
                                                                                       '{user_name}', 
                                                                                       '{claim_p[message.chat.id, 'price_event']}',
                                                                                       '{ttt}');''')
    con.commit()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
    keya = types.InlineKeyboardMarkup(row_width=1)
    keya.add(types.InlineKeyboardButton(text=f"Написать", callback_data=f"ClbSendMessage"))
    bot.send_message(message.chat.id,
                     'Заявка успешно создана. Ожидайте! В ближайшее время с вами свяжется администратор!',
                     reply_markup=key)
    claim_a['admin_claim_id'] = claim_id
    claim_a['admin_chat_id'] = message.chat.id
    claim_a['admin_chat_date'] = date
    for o in admins:
        bot.send_message(int(o), f'Новая заявка!!!'
                                 f'\n\nПрогулка: {claim_p[message.chat.id, "name_event"]}'
                                 f'\nДата: {date}'
                                 f'\nИмя пользователя: {user_name}'
                                 f'\nЦена: {claim_p[message.chat.id, "price_event"]}'
                                 f'\n\nКомментарий: {ttt}', reply_markup=keya)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


# Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.WFMesT.value)
def user_age(message):
    text = message.text
    cur.execute(f'''SELECT ChatId FROM claims WHERE Id = '{claim_a['admin_claim_id']}';''')
    rows = cur.fetchone()
    bot.send_message(int(rows[0]), text)
    cur.execute(
        f'''UPDATE p{claim_a['admin_chat_id']} SET AnswerAdmin = '{text}' WHERE Date = '{claim_a['admin_chat_date']}';''')
    con.commit()
    dbworker.set_state(message.chat.id, config.States.S_START.value)


# Новое мероприятие_название ----- Новое мероприятие_название ----- Новое мероприятие_название ----- Новое мероприятие_название ----- Новое мероприятие_название
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewEventName.value)
def user_age(message):
    new_event[message.chat.id, 'name'] = message.text
    bot.send_message(message.chat.id, 'Напишите описание мероприятия. Вы можете использовать специальные теги.'
                                      '\n\nВиды тегов:'
                                      '\n<b>Жирный</b>'
                                      '\n<em>Курсив</em>'
                                      '\n<ins>С подчеркиванием</ins>'
                                      '\n<del>Зачеркнутый</del>'
                                      '\n<code>Моноширинный (вообще это кодовый для программистов)</code>'
                                      '\n<a href="какая нибудь ссылка">Слово в котором будет ссылка</a>'
                                      '\n\nНапишите в чат описание мероприятия:')
    dbworker.set_state(message.chat.id, config.States.NewEventText.value)


# Новое мероприятие_описание ----- Новое мероприятие_описание ----- Новое мероприятие_описание ----- Новое мероприятие_описание ----- Новое мероприятие_описание
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewEventText.value)
def user_age(message):
    new_event[message.chat.id, 'text'] = message.text
    bot.send_message(message.chat.id, 'Какая цена одного билета на данное мероприятие? (Кол-во: 1 шт)')
    dbworker.set_state(message.chat.id, config.States.NewEventPrice.value)


# Новое мероприятие_цена ----- Новое мероприятие_цена ----- Новое мероприятие_цена ----- Новое мероприятие_цена ----- Новое мероприятие_цена
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewEventPrice.value)
def user_age(message):
    new_event[message.chat.id, 'price'] = message.text
    tz = pytz.timezone('Europe/Moscow')
    dt = datetime.datetime.now(tz)
    date = dt.replace(tzinfo=None)
    cur.execute(f'''INSERT INTO events (Id, Name, Text, ImgName, Price) VALUES 
                                                            ('{date}',
                                                            '{new_event[message.chat.id, "name"]}',
                                                            '{new_event[message.chat.id, "text"]}',
                                                            ' ',
                                                            '{new_event[message.chat.id, "price"]}');''')
    con.commit()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
    bot.send_message(message.chat.id, f'Мероприятие успешно создано!!!'
                         f'\n\nНазвание кнопки: {new_event[message.chat.id, "name"]}'
                         f'\nОписание: {new_event[message.chat.id, "text"]}'
                         f'\nЦена: {new_event[message.chat.id, "price"]}₽', reply_markup=key)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


# Редактирование мероприятия ----- Редактирование мероприятия ----- Редактирование мероприятия ----- Редактирование мероприятия ----- Редактирование мероприятия
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.EditNameEvent.value)
def edit_name_event(message):
    id = edit_event[message.chat.id, 'Id']
    cur.execute(f'''UPDATE events SET Name = '{message.text}' WHERE Id = '{id}';''')
    con.commit()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
    bot.send_message(message.chat.id, 'Мероприятие обновлено!', reply_markup=key)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.EditTextEvent.value)
def edit_text_event(message):
    id = edit_event[message.chat.id, 'Id']
    cur.execute(f'''UPDATE events SET Text = '{message.text}' WHERE Id = '{id}';''')
    con.commit()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
    bot.send_message(message.chat.id, 'Мероприятие обновлено!', reply_markup=key)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.EditPriceEvent.value)
def edit_price_event(message):
    id = edit_event[message.chat.id, 'Id']
    cur.execute(f'''UPDATE events SET Price = '{message.text}' WHERE Id = '{id}';''')
    con.commit()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
    bot.send_message(message.chat.id, 'Мероприятие обновлено!', reply_markup=key)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(content_types=['photo'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.SendMChatPhoto_1.value)
def send_m_chat_photo_1(message):
    img = bot.get_file(message.photo[-1].file_id)
    path = bot.download_file(img.file_path)
    with open('photo.jpg', 'wb') as file:
        file.write(path)
    file.close()
    bot.send_message(message.chat.id, f'Фотография сохранена. Напишите сообщение. Вы можете использовать специальные теги.'
                                   f'\n\nВиды тегов:'
                                   f'\n<b>Жирный</b>'
                                   f'\n<em>Курсив</em>'
                                   f'\n<ins>С подчеркиванием</ins>'
                                   f'\n<del>Зачеркнутый</del>'
                                   f'\n<code>Моноширинный (вообще это кодовый для программистов)</code>'
                                   f'\n<a href="какая нибудь ссылка">Слово в котором будет ссылка</a>'
                                   f'\n\nНапишите в чат сообщение для пользователей:')
    dbworker.set_state(message.chat.id, config.States.SendMChatPhoto_2.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.SendMChatPhoto_2.value)
def send_m_chat_photo_2(message):
    cur.execute("""SELECT table_name FROM information_schema.tables
                           WHERE table_schema = 'public'""")
    ids = []
    for table_name in cur.fetchall():
        if 'p' in table_name[0]:
            ids.append(int(table_name[0].strip('p')))
    text = message.text
    for i in ids:
        img = open('photo.jpg', 'rb')
        bot.send_photo(i, img, text, parse_mode='html')
        img.close()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
    bot.send_message(message.chat.id, 'Сообщение отправлено!', reply_markup=key)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(content_types=['video'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.SendMChatVideo_1.value)
def send_m_chat_video_1(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('video.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, f'Фотография сохранена. Напишите сообщение. Вы можете использовать специальные теги.'
                                   f'\n\nВиды тегов:'
                                   f'\n<b>Жирный</b>'
                                   f'\n<em>Курсив</em>'
                                   f'\n<ins>С подчеркиванием</ins>'
                                   f'\n<del>Зачеркнутый</del>'
                                   f'\n<code>Моноширинный (вообще это кодовый для программистов)</code>'
                                   f'\n<a href="какая нибудь ссылка">Слово в котором будет ссылка</a>'
                                   f'\n\nНапишите в чат сообщение для пользователей:')
    dbworker.set_state(message.chat.id, config.States.SendMChatVideo_2.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.SendMChatVideo_2.value)
def send_m_chat_video_2(message):
    cur.execute("""SELECT table_name FROM information_schema.tables
                           WHERE table_schema = 'public'""")
    ids = []
    for table_name in cur.fetchall():
        if 'p' in table_name[0]:
            ids.append(int(table_name[0].strip('p')))
    text = message.text
    for i in ids:
        img = open('video.mp4', 'rb')
        bot.send_video(i, img, None, text, timeout=1000, parse_mode='html', supports_streaming=True)
        img.close()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
    bot.send_message(message.chat.id, 'Сообщение отправлено!', reply_markup=key)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.SendMChatNoPhoto.value)
def send_m_chat_no_photo(message):
    cur.execute("""SELECT table_name FROM information_schema.tables
                               WHERE table_schema = 'public'""")
    ids = []
    for table_name in cur.fetchall():
        if 'p' in table_name[0]:
            ids.append(int(table_name[0].strip('p')))
    text = message.text
    for i in ids:
        bot.send_message(i, text, parse_mode='html')
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
    bot.send_message(message.chat.id, 'Сообщение отправлено!', reply_markup=key)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewSaleName.value)
def send_m_chat_no_photo(message):
    new_sale[message.chat.id, "name"] = message.text
    bot.send_message(message.chat.id, 'Отлично! Теперь напишите текст для уведомления пользвателей...')
    dbworker.set_state(message.chat.id, config.States.NewSaleText.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewSaleText.value)
def send_m_chat_no_photo(message):
    new_sale[message.chat.id, "text"] = message.text
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    text = ''
    for i in range(len(rows)):
        s_events[f"{i + 1}"] = rows[i][1]
        text += f'{i + 1}. {rows[i][1]}\n'
    bot.send_message(message.chat.id, f'Сохранено! Теперь выберите на какие мероприятия распространяется скидка'
                                      f'\n\nМероприятия:'
                                      f'\n{text}'
                                      f'\n\nНапишите в чат через запятую номера мероприятий (точка в конце не ставится), '
                                      f'на которые РАСПРОСТРАНЯЕТСЯ скидка.'
                                      f'\n\nПример: 1, 2, 5, 8')
    dbworker.set_state(message.chat.id, config.States.NewSaleTextNames.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewSaleTextNames.value)
def send_m_chat_no_photo(message):
    NumbersNames = (message.text).split(', ')
    ListNames = [s_events[f'{num}'] for num in NumbersNames]
    new_sale[message.chat.id, "text_names"] = " ".join(ListNames)
    bot.send_message(message.chat.id, f'Список мероприятий на которые распространяется скидка:'
                                      f'\n{", ".join(ListNames)}'
                                      f'\n\nНапишите какая будет скидка.'
                                      f'\n\nПример: 0.1 (пишите скидку в десятичной дроби, через точку. Например 10% - 0.1 и т.д.)')
    dbworker.set_state(message.chat.id, config.States.NewSalePercent.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewSalePercent.value)
def send_m_chat_no_photo(message):
    s_events = {}
    new_sale[message.chat.id, "sale_percent"] = message.text
    bot.send_message(message.chat.id, f'Отлично! Теперь напишите через сколько часов закончится действие скидки.'
                                      f'\n\nПример: 12 (указывается число - кол-во часов)')
    dbworker.set_state(message.chat.id, config.States.NewSaleDateDelta.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewSaleDateDelta.value)
def send_m_chat_no_photo(message):
    new_sale[message.chat.id, "date_delta"] = message.text
    # Date, datetime.datetime.now()
    # Name, new_sale[message.chat.id, "name"]
    # Text, new_sale[message.chat.id, "text"]
    # TextNames, new_sale[message.chat.id, "text_names"]
    # SalePercent, new_sale[message.chat.id, "sale_percent"]
    # DateDelta, new_sale[message.chat.id, "date_delta"]
    # State, 'True'
    tz = pytz.timezone('Europe/Moscow')
    dt = datetime.datetime.now(tz)
    date = dt.replace(tzinfo=None)
    cur.execute(f'''INSERT INTO sale (Date, Name, Text, TextNames, SalePercent, DateDelta, State) VALUES 
                                                                ('{date}',
                                                                '{new_sale[message.chat.id, "name"]}',
                                                                '{new_sale[message.chat.id, "text"]}',
                                                                '{new_sale[message.chat.id, "text_names"]}',
                                                                '{new_sale[message.chat.id, "sale_percent"]}',
                                                                '{date + datetime.timedelta(hours=int(new_sale[message.chat.id, "date_delta"]))}',
                                                                'True');''')
    con.commit()
    cur.execute("SELECT * FROM sale")
    rows = cur.fetchall()
    bot.send_message(message.chat.id, f'Скидка сохранена и применена. Вот текущие значения:'
                                      f'\n\n<ins>Дата создания:</ins> \n{rows[-1][0]}'
                                      f'\n\n<ins>Название:</ins> \n{rows[-1][1]}'
                                      f'\n\n<ins>Описание:</ins> \n{rows[-1][2]}'
                                      f'\n\n<ins>Мероприятия, на которые распространяется скидка:</ins> \n{rows[-1][3]}'
                                      f'\n\n<ins>Скидка:</ins> \n{int(float(rows[-1][4]) * 100)}%'
                                      f'\n\n<ins>Дата окончания скидки:</ins> \n{rows[-1][5]}'
                                      f'\n\n<ins>Статус:</ins> \n{rows[-1][6]}', parse_mode='html')
    dbworker.set_state(message.chat.id, config.States.S_START.value)

    cur.execute("""SELECT table_name FROM information_schema.tables
                               WHERE table_schema = 'public'""")
    ids = []
    for table_name in cur.fetchall():
        if 'p' in table_name[0]:
            ids.append(int(table_name[0].strip('p')))
    for i in ids:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='Прайс »', callback_data="ClbEvents"))
        bot.send_message(i, f'{rows[-1][1]}'
                               f'\n{rows[-1][2]}'
                               f'\n\n<code>Скидка действует до {".".join(str(rows[-1][5]).split()[0].split("-")[::-1])} '
                               f'{":".join(str(rows[-1][5]).split()[1].split(":")[0:2])}</code>', parse_mode='html', reply_markup=keyboard)


# Callback ----- Callback ----- Callback ----- Callback ----- Callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS p{call.message.chat.id}
                                                                 (Name TEXT,
                                                                 Date TEXT,
                                                                 State TEXT,
                                                                 NameUser TEXT, 
                                                                 Price INT, 
                                                                 AnswerAdmin TEXT);''')
    con.commit()


    # Старт callback ----- Старт callback ----- Старт callback ----- Старт callback ----- Старт callback
    if call.data == 'ClbStart':
        if call.message.chat.id in admins:
            buttons = [
                types.InlineKeyboardButton(text="Прайс", callback_data="ClbEvents-A"),
                types.InlineKeyboardButton(text="Все заявки", callback_data="ClbClaims-A"),
                types.InlineKeyboardButton(text="Скидки и акции", callback_data="ClbSale-A"),
                types.InlineKeyboardButton(text="Отправить сообщение", callback_data="ClbSendMChat-A"),
                types.InlineKeyboardButton(text="Бот", callback_data="ClbBot-A")
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Панель администратора. По кнопке "Бот" можно зайти в бота, как обычный пользователь...',
                reply_markup=keyboard)
            dbworker.set_state(call.message.chat.id, config.States.S_START.value)
        else:
            cur.execute("SELECT * FROM events")
            rows = cur.fetchall()
            EventsNames = ''
            for i in range(len(rows)):
                EventsNames += f'{rows[i][1]}\n'
            buttons = [
                types.InlineKeyboardButton(text="Прайс", callback_data="ClbEvents"),
                types.InlineKeyboardButton(text="Помощь", callback_data="ClbHelp"),
                types.InlineKeyboardButton(text="Мои заявки", callback_data="ClbClaims"),
                types.InlineKeyboardButton(text='Наш Instagram', url='https://www.instagram.com/gagra_sup/')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f' <b>Приветствую! Я GAGRASUPbot</b>'
                                          f'и мне хочется предложить вам отличный способ активно и увлекательно провести свой досуг '
                                          f'- сапбординг. Это увлекательный вид активности, который понравится абсолютно любому - '
                                          f'от взрослых до детей, любителям экстрима и просто желающим приятно провести время на '
                                          f'море или на реке.'
                                          f'\n\n Мы предоставляем <b>качественные и надежные</b> сапборды от известных производителей, '
                                          f'таких как <b>Stormline</b>, <b>Bombitto</b> и другие бренды. '
                                          f'При этом, наш гид обязательно проведет инструктаж перед началом сплава, '
                                          f'а также предоставит спасательные жилеты и водонепроницаемые чехлы для '
                                          f'вашего телефона, чтобы обеспечить вашу безопасность.'
                                          f'\n\nМы предлагаем различные варианты для всех желающих - прокат сапбордов, '
                                          f'организованные прогулки и индивидуальные туры. Вам просто нужно нажать на '
                                          f'кнопку "Прайс" и выбрать наиболее подходящий вариант для себя. '
                                          f'При этом, если погода не будет благоприятной, мы всегда готовы '
                                          f'перенести ваши прогулки на более удобное время.'
                                          f'\n\nНе упускайте возможность открыть для себя новый увлекательный мир морских прогулок - '
                                          f'выберите сапбординг с GAGRASUPbot!', parse_mode='html', reply_markup=keyboard)
            dbworker.set_state(call.message.chat.id, config.States.S_START.value)


    # Прайс / мероприятия  ----- Прайс / мероприятия  ----- Прайс / мероприятия  ----- Прайс / мероприятия  ----- Прайс / мероприятия
    if call.data == 'ClbEvents':
        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][1]}", callback_data=f"ClbEvents{rows[i][0]}") for i in
                   range(len(rows))]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        if call.message.chat.id in admins:
            keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbBot-A"))
        else:
            keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbStart"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='<b>ПРОГУЛКИ. Выберите подходящий вариант:</b>', parse_mode='html', reply_markup=keyboard)


    cur.execute("SELECT * FROM events")
    rows_events = cur.fetchall()
    for i in range(len(rows_events)):

        # Прайс / мероприятия вывод ----- Прайс / мероприятия вывод ----- Прайс / мероприятия вывод ----- Прайс / мероприятия вывод
        if call.data == f"ClbEvents{rows_events[i][0]}":
            key = types.InlineKeyboardMarkup(row_width=1)
            cur.execute("SELECT * FROM sale")
            sale_rows = cur.fetchall()
            num = [0]
            tz = pytz.timezone('Europe/Moscow')
            dt = datetime.datetime.now(tz)
            date = dt.replace(tzinfo=None)
            for i_s in range(len(sale_rows)):
                if sale_rows[i_s][6] == 'True':
                    if date <= sale_rows[i_s][5]:
                        if rows_events[i][1] in sale_rows[i_s][3]:
                            num.append(float(sale_rows[i_s][4]))
                    else:
                        cur.execute(f'''UPDATE sale SET State = 'False' WHERE Date = '{sale_rows[i_s][0]}';''')
                        con.commit()
            text = ''
            if max(num) == 0:
                text = f'{rows_events[i][4]}₽'
            else:
                cur.execute(f"SELECT * FROM sale WHERE SalePercent = '{max(num)}' AND State = 'True'")
                sale_rows_1 = cur.fetchall()
                text = f'<del>{rows_events[i][4]}₽</del> {int(int(rows_events[i][4]) - (int(rows_events[i][4]) * max(num)))}₽' \
                       f'\n\n<code>Скидка {int(max(num) * 100)}% действует до {".".join(str(sale_rows_1[0][5]).split()[0].split("-")[::-1])} {":".join(str(sale_rows_1[0][5]).split()[1].split(":")[0:2])}</code>'

            key.add(types.InlineKeyboardButton(text=f"Подать заявку", callback_data=f"ClbEventsSend{rows_events[i][0]}"),
                    types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'{rows_events[i][2]}'
                                       f'\n\n<b>Цена: {text}</b>', parse_mode='html', reply_markup=key)


        # Подать заявку ----- Подать заявку ----- Подать заявку ----- Подать заявку ----- Подать заявку
        if call.data == f"ClbEventsSend{rows_events[i][0]}":
            cur.execute(f"SELECT * FROM p{call.message.chat.id}")
            row_sel = cur.fetchall()
            k = 1
            tz = pytz.timezone('Europe/Moscow')
            dt = datetime.datetime.now(tz)
            date = dt.replace(tzinfo=None)
            for p in range(len(row_sel)):
                if (row_sel[p][1].split()[0] == f'{date}'.split()[0]) and (
                        rows_events[i][1] == row_sel[p][0]):
                    k = 0
            if k:
                # Date, datetime.datetime.now()
                # Name, new_sale[message.chat.id, "name"]
                # Text, new_sale[message.chat.id, "text"]
                # TextNames, new_sale[message.chat.id, "text_names"]
                # SalePercent, new_sale[message.chat.id, "sale_percent"]
                # DateDelta, new_sale[message.chat.id, "date_delta"]
                # State, 'True'
                dbworker.set_state(call.message.chat.id, config.States.SendClaim.value)
                cur.execute("SELECT * FROM sale")
                sale_rows = cur.fetchall()
                num = [0]
                tz = pytz.timezone('Europe/Moscow')
                dt = datetime.datetime.now(tz)
                date = dt.replace(tzinfo=None)
                for i_s in range(len(sale_rows)):
                    if sale_rows[i_s][6] == 'True':
                        if date <= sale_rows[i_s][5]:
                            if rows_events[i][1] in sale_rows[i_s][3]:
                                num.append(float(sale_rows[i_s][4]))
                        else:
                            cur.execute(f'''UPDATE sale SET State = 'False' WHERE Date = '{sale_rows[i_s][0]}';''')
                            con.commit()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Напишите сообщение к заявке и укажите в нем контактные данные (номер телефона/ссылка на телеграм/ссылка на страницу вк)...')
                claim_p[call.message.chat.id, 'name_event'] = rows_events[i][1]
                claim_p[call.message.chat.id, 'price_event'] = int(int(rows_events[i][4]) - (int(rows_events[i][4]) * max(num)))

            else:
                keyss = types.InlineKeyboardMarkup(row_width=1)
                keyss.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Заявка повторно быть подана не может! Второй раз подать заявку вы сможете только завтра!',
                                      reply_markup=keyss)


        # Прайс / мероприятия админ вывод ----- Прайс / мероприятия админ вывод ----- Прайс / мероприятия админ вывод ----- Прайс / мероприятия админ вывод
        if call.data == f"ClbEvents{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}-A":
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"Редактировать название", callback_data=f"ClbEditNameEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}"),
                    types.InlineKeyboardButton(text=f"Редактировать текст", callback_data=f"ClbEditTextEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}"),
                    types.InlineKeyboardButton(text=f"Редактировать цену", callback_data=f"ClbEditPriceEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}"),
                    types.InlineKeyboardButton(text=f"Удалить", callback_data=f"ClbDelEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}_1"),
                    types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'{rows_events[i][2]}'
                                         f'\n\n<b>Цена: {rows_events[i][4]}₽</b>', parse_mode='html', reply_markup=key)


        # Редактирование мероприятия ----- Редактирование мероприятия ----- Редактирование мероприятия ----- Редактирование мероприятия
        if call.data == f"ClbEditNameEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}":
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}-A"))
            edit_event[call.message.chat.id, 'Id'] = rows_events[i][0]
            dbworker.set_state(call.message.chat.id, config.States.EditNameEvent.value)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Напишите в чат новое название:', reply_markup=key)


        if call.data == f"ClbEditTextEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}":
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}-A"))
            edit_event[call.message.chat.id, 'Id'] = rows_events[i][0]
            dbworker.set_state(call.message.chat.id, config.States.EditTextEvent.value)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Напишите новый текст и не забывайте писать правильные теги открывая и закрывая их.'
                                       '\n\nВиды тегов:'
                                       '\n<b>Жирный</b>'
                                       '\n<em>Курсив</em>'
                                       '\n<ins>С подчеркиванием</ins>'
                                       '\n<del>Зачеркнутый</del>'
                                       '\n<code>Моноширинный (вообще это кодовый для программистов)</code>'
                                       '\n<a href="какая нибудь ссылка">Слово в котором будет ссылка</a>'
                                       '\n\nНапишите в чат новый текст:', reply_markup=key)


        if call.data == f"ClbEditPriceEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}":
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}-A"))
            edit_event[call.message.chat.id, 'Id'] = rows_events[i][0]
            dbworker.set_state(call.message.chat.id, config.States.EditPriceEvent.value)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Напишите новую цену:', reply_markup=key)


        # Удалить мероприятие ----- Удалить мероприятие ----- Удалить мероприятие ----- Удалить мероприятие ----- Удалить мероприятие
        if call.data == f"ClbDelEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}_1":
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"Да", callback_data=f"ClbDelEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}_2"),
                    types.InlineKeyboardButton(text=f"Нет", callback_data=f"ClbEvents{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}-A"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Вы точно хотите удалить мероприятие?', reply_markup=key)


        if call.data == f"ClbDelEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}_2":
            cur.execute(f'''DELETE FROM events WHERE Id = '{rows_events[i][0]}';''')
            con.commit()
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Мероприятие удалено!', reply_markup=key)


    # Все заявки для пользователя ----- Все заявки для пользователя ----- Все заявки для пользователя ----- Все заявки для пользователя ----- Все заявки для пользователя
    if call.data == 'ClbClaims':
        cur.execute(f"SELECT * FROM p{call.message.chat.id}")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][0]} ({'.'.join(rows[i][1].split()[0].split('-')[::-1])})",
                                              callback_data=f"ClbEvents{rows[i][1].split()[0]}_{rows[i][1].split()[1]}")
                   for i in range(len(rows))]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению у вас пока нет заявок((( ' \
                   '\n\n<code>Чтобы подать заявку нажмите «Прайс» и выберите прогулку</code>'
            keyboard.add(types.InlineKeyboardButton(text=f"Прайс", callback_data=f"ClbEvents"))

        if call.message.chat.id in admins:
            keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbBot-A"))
        else:
            keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbStart"))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, parse_mode='html', reply_markup=keyboard)


    # Все заявки для пользователя вывод ----- Все заявки для пользователя вывод ----- Все заявки для пользователя вывод ----- Все заявки для пользователя вывод ----- Все заявки для пользователя вывод
    cur.execute(f"SELECT * FROM p{call.message.chat.id}")
    rows_claims_user = cur.fetchall()
    for i in range(len(rows_claims_user)):
        if call.data == f"ClbEvents{rows_claims_user[i][1].split()[0]}_{rows_claims_user[i][1].split()[1]}":
            keydpl = types.InlineKeyboardMarkup(row_width=1)
            keydpl.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'<b>{rows_claims_user[i][0]}</b>'
                                       f'\nДата: {".".join(rows_claims_user[i][1].split()[0].split("-")[::-1])}'
                                       f'\nВремя: {":".join(rows_claims_user[i][1].split()[1].split(":")[0:2])}'
                                       f'\n\nСтатус: {rows_claims_user[i][2]}'
                                       f'\nЦена: {rows_claims_user[i][4]}'
                                       f'\n\nСообщение от администратора: {rows_claims_user[i][5]}', parse_mode='html', reply_markup=keydpl)


    # Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора
    if call.data == 'ClbSendMessage':
        dbworker.set_state(call.message.chat.id, config.States.WFMesT.value)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Напишите сообщение...')


    # Прайс / мероприятия админ ----- Прайс / мероприятия админ ----- Прайс / мероприятия админ ----- Прайс / мероприятия админ ----- Прайс / мероприятия админ
    if call.data == 'ClbEvents-A':
        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][1]}",
                                              callback_data=f"ClbEvents{rows[i][0].split()[0]}_{rows[i][0].split()[1]}-A")
                   for i in
                   range(len(rows))]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"Создать мероприятие", callback_data=f"ClbNewEvent-A"),
                     types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению мероприятий пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.S_START.value)


    # Новое мероприятие ----- Новое мероприятие ----- Новое мероприятие ----- Новое мероприятие ----- Новое мероприятие
    if call.data == 'ClbNewEvent-A':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Напишите название мероприятия...', reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.NewEventName.value)


    # Виды заявок ----- Виды заявок ----- Виды заявок ----- Виды заявок ----- Виды заявок
    if call.data == 'ClbClaims-A':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text=f"На рассмотрении", callback_data=f"ClbClaimsTrue_0-A"),
                     types.InlineKeyboardButton(text=f"Одобренные", callback_data=f"ClbClaimsTrue_2-A"),
                     types.InlineKeyboardButton(text=f"Выполненные", callback_data=f"ClbClaimsFalse_1-A"),
                     types.InlineKeyboardButton(text=f"Отклоненные", callback_data=f"ClbClaimsTrue_3-A"),
                     types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите тип заявок:', reply_markup=keyboard)


    # Виды заявок вывод ----- Виды заявок вывод ----- Виды заявок вывод ----- Виды заявок вывод ----- Виды заявок вывод
    if call.data == 'ClbClaimsTrue_0-A':
        cur.execute("SELECT * FROM claims")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({'.'.join(rows[i][3].split()[0].split('-')[::-1])})", callback_data=f"ClbClaimTrue{'_'.join(rows[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows[i][3].split()[1].split(':')[0:2])}-A") for i in
                range(len(rows)) if rows[i][4] == 'На рассмотрении']
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению новых заявок пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)


    if call.data == 'ClbClaimsTrue_2-A':
        cur.execute("SELECT * FROM claims")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({'.'.join(rows[i][3].split()[0].split('-')[::-1])})", callback_data=f"ClbClaimTrue{'_'.join(rows[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows[i][3].split()[1].split(':')[0:2])}-A") for i in
                range(len(rows)) if rows[i][4] == 'Одобрена']
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению новых заявок пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)


    if call.data == 'ClbClaimsTrue_3-A':
        cur.execute("SELECT * FROM claims")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({'.'.join(rows[i][3].split()[0].split('-')[::-1])})", callback_data=f"ClbClaimTrue{'_'.join(rows[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows[i][3].split()[1].split(':')[0:2])}-A") for i in
                range(len(rows)) if rows[i][4] == 'Отклонена']
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению новых заявок пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)


    if call.data == 'ClbClaimsFalse_1-A':
        cur.execute("SELECT * FROM claims")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({'.'.join(rows[i][3].split()[0].split('-')[::-1])})", callback_data=f"ClbClaimTrue{'_'.join(rows[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows[i][3].split()[1].split(':')[0:2])}-A") for i in
                range(len(rows)) if rows[i][4] == 'Выполнена']
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению новых заявок пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)


    # Вывод заявки ----- Вывод заявки ----- Вывод заявки ----- Вывод заявки ----- Вывод заявки
    cur.execute("SELECT * FROM claims")
    rows_claims = cur.fetchall()
    for i in range(len(rows_claims)):
        if call.data == f"ClbClaimTrue{'_'.join(rows_claims[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows_claims[i][3].split()[1].split(':')[0:2])}-A":
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"Поставить статус - Выполнена",
                                                callback_data=f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_1-A"),
                     types.InlineKeyboardButton(text=f"Поставить статус - Одобрена",
                                                callback_data=f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_2-A"),
                     types.InlineKeyboardButton(text=f"Поставить статус - Отклонена",
                                               callback_data=f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_3-A"),
                     types.InlineKeyboardButton(text=f"Написать сообщение к заявке", callback_data=f"ClbSendMessage"),
                     types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
            claim_a['admin_claim_id'] = rows_claims[i][0]
            cur.execute(f"SELECT * FROM p{rows_claims[i][1]} WHERE Date = '{rows_claims[i][3]}'")
            r = cur.fetchall()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'ChatId - {rows_claims[i][1]}'
                                         f'\n\nНазвание мероприятия: {rows_claims[i][2]}'
                                         f'\nДата: {".".join(rows_claims[i][3].split()[0].split("-")[::-1])} в {":".join(rows_claims[i][3].split()[1].split(":")[0:2])}'
                                         f'\nСтатус: {rows_claims[i][4]}'
                                         f'\nИмя пользователя: @{rows_claims[i][5]}'
                                         f'\n\nЦена: {rows_claims[i][6]}'
                                         f'\n\nСообщение администратора: {r[0][5]}'
                                         f'\n\nКомментарий пользователя: {rows_claims[i][7]}', reply_markup=keyb)


        # Статусы заявок ----- Статусы заявок ----- Статусы заявок ----- Статусы заявок ----- Статусы заявок
        if call.data == f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_1-A":
            cur.execute(f'''UPDATE claims SET State = 'Выполнена' WHERE Id = '{rows_claims[i][0]}';''')
            con.commit()
            cur.execute(f'''UPDATE p{rows_claims[i][1]} SET State = 'Выполнена' WHERE Date = '{rows_claims[i][3]}';''')
            con.commit()
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
            bot.send_message(rows_claims[i][1], f'Ваша заявка "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} выполнена!')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Успешно! Статус заявки "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} изменен на "Выполнена"', reply_markup=keyb)


        if call.data == f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_2-A":
            cur.execute(f'''UPDATE claims SET State = 'Одобрена' WHERE Id = '{rows_claims[i][0]}';''')
            con.commit()
            cur.execute(f'''UPDATE p{rows_claims[i][1]} SET State = 'Одобрена' WHERE Date = '{rows_claims[i][3]}';''')
            con.commit()
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
            bot.send_message(rows_claims[i][1], f'Ваша заявка "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} одобрена!')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Успешно! Статус заявки "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} изменен на "Одобрена"', reply_markup=keyb)


        if call.data == f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_3-A":
            cur.execute(f'''UPDATE claims SET State = 'Отклонена' WHERE Id = '{rows_claims[i][0]}';''')
            con.commit()
            cur.execute(f'''UPDATE p{rows_claims[i][1]} SET State = 'Отклонена' WHERE Date = '{rows_claims[i][3]}';''')
            con.commit()
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
            bot.send_message(rows_claims[i][1], f'Ваша заявка "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} отклонена!')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Успешно! Статус заявки "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} изменен на "Отклонена"', reply_markup=keyb)


    # Помощь ----- Помощь ----- Помощь ----- Помощь ----- Помощь
    if call.data == "ClbHelp":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='WhatsApp', url='https://wa.me/+79407322932'),
                     types.InlineKeyboardButton(text='Telegram', url='tg://resolve?domain=danyaagrba'),
                     types.InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/gagra_sup/'))
        if call.message.chat.id in admins:
            keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbBot-A"))
        else:
            keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbStart"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы можете написать нам:', reply_markup=keyboard)


    # Скидки и акции админ ----- Скидки и акции админ ----- Скидки и акции админ ----- Скидки и акции админ ----- Скидки и акции админ
    if call.data == "ClbSale-A":
        cur.execute(f'''CREATE TABLE IF NOT EXISTS sale
                                                 (Date TEXT,
                                                 Name TEXT,
                                                 Text TEXT,
                                                 TextNames TEXT,
                                                 SalePercent TEXT, 
                                                 DateDelta TIMESTAMP,
                                                 State TEXT);''')
        con.commit()
        s_events = {}
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbStart"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Напишите название для скидки:', reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.NewSaleName.value)


    # Отправить сообщение админ ----- Отправить сообщение админ ----- Отправить сообщение админ ----- Отправить сообщение админ
    if call.data == "ClbSendMChat-A":
        cur.execute("""SELECT table_name FROM information_schema.tables
                               WHERE table_schema = 'public'""")

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='Текст с фото', callback_data="ClbSendMChatPhoto-A"),
                     types.InlineKeyboardButton(text='Текст с видео', callback_data="ClbSendMChatVideo-A"),
                     types.InlineKeyboardButton(text='Только текст', callback_data="ClbSendMChatNoPhoto-A"),
                     types.InlineKeyboardButton(text='« Назад', callback_data="ClbStart"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите тип:', reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.S_START.value)


    if call.data == "ClbSendMChatPhoto-A":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbSendMChat-A"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Отправьте фотографию в формате png или jpg...',reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.SendMChatPhoto_1.value)


    if call.data == "ClbSendMChatVideo-A":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbSendMChat-A"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Отправьте видео в формате png или jpg...',reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.SendMChatVideo_1.value)


    if call.data == "ClbSendMChatNoPhoto-A":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='« Назад', callback_data="ClbSendMChat-A"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Вы можете использовать специальные теги.'
                                   f'\n\nВиды тегов:'
                                   f'\n<b>Жирный</b>'
                                   f'\n<em>Курсив</em>'
                                   f'\n<ins>С подчеркиванием</ins>'
                                   f'\n<del>Зачеркнутый</del>'
                                   f'\n<code>Моноширинный (вообще это кодовый для программистов)</code>'
                                   f'\n<a href="какая нибудь ссылка">Слово в котором будет ссылка</a>'
                                   f'\n\nНапишите в чат сообщение для пользователей:', reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.SendMChatNoPhoto.value)


    # Бот для админа ----- Бот для админа ----- Бот для админа ----- Бот для админа ----- Бот для админа
    if call.data == "ClbBot-A":
        buttons = [
            types.InlineKeyboardButton(text="Прайс", callback_data="ClbEvents"),
            types.InlineKeyboardButton(text="Помощь", callback_data="ClbHelp"),
            types.InlineKeyboardButton(text="Мои заявки", callback_data="ClbClaims"),
            types.InlineKeyboardButton(text='Наш Instagram', url='https://www.instagram.com/gagra_sup/'),
            types.InlineKeyboardButton(text='« Назад', callback_data="ClbStart"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f' 👋🏻 <b>Приветствую! Я GAGRASUPbot.</b>'
                                   f' Откройте для себя новый увлекательный мир морских прогулок. '
                                   f'Ознакомьтесь с нашим предложением и выберите для себя самое лучшее'
                                   f'\n\n <b>Сапбординг</b> <em>— именно тот вид активности, который '
                                   f'понравится абсолютно всем, это по-настоящему универсальный вид '
                                   f'активного отдыха, который по душе и взрослым, и детям. Многие хотят '
                                   f'просто кататься по морю, по реке, встречать рассветы и загорать. '
                                   f'\nНикакого экстрима.</em>'
                                   f'\n\nИНСТРУКТАЖ И БЕЗОПАСНОСТЬ'
                                   f'\n У нас только качественные и брендовые сапборды Stormline, Bombitto и другие.'
                                   f'\n\n Гид проводит обязательный инструктаж перед сплавом, выдает спасательные '
                                   f'жилеты, водонепроницаемые чехлы для телефонов. '
                                   f'\n\n <em>*При неблагоприятных климатических условиях возможен перенос прогулки</em>'
                                   f'\n\n<b>ПРОКАТ • ПРОГУЛКИ • ИНДИВИДУАЛЬНЫЕ ТУРЫ</b>'
                                   f'\n\n<code>нажмите «Прайс» и выберите прогулку</code>', parse_mode='html',
                              reply_markup=keyboard)

    if call.data == f'db_config_clb':
        if call.message.chat.id in admins:
            buttons = [types.InlineKeyboardButton(text=f"{table[0]}", callback_data=f"db_config_{table[0]}") for table in cur.fetchall()]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Все таблицы базы данных:', reply_markup=keyboard)


    cur.execute("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema = 'public'""")
    for table_name in cur.fetchall():
        if call.data == f'db_config_{table_name[0]}':
            if call.message.chat.id in admins:
                cur.execute(f"""SELECT * FROM {table_name[0]}""")
                key = types.InlineKeyboardMarkup(row_width=1)
                key.add(types.InlineKeyboardButton(text="Да", callback_data=f"db_config_{table_name[0]}_del"),
                        types.InlineKeyboardButton(text="Нет", callback_data="db_config_clb"))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f'Зачения:'
                                           f'\n\n{[(i[0], i[1]) for i in cur.fetchall()]}'
                                           f'\n\nХотите очистить таблицу?', reply_markup=key)

        if call.data == f'db_config_{table_name[0]}_del':
            if call.message.chat.id in admins:
                cur.execute(f''' DELETE FROM {table_name[0]} ''')
                key = types.InlineKeyboardMarkup(row_width=1)
                key.add(types.InlineKeyboardButton(text="« Назад", callback_data="db_config_clb"))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Выполнено!', reply_markup=key)


bot.polling(none_stop = True, interval = 0)
