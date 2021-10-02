import telebot
from func.take_base import take_base_clubs
from func.check_user import check_user_mail
from func.sorting import sorting
from func.take_info_clubs import take_info_clubs
from func.mail import mail_out
from func.geoloc import distance_calc
from settings import TOKEN
from func.keyboards import take_keyboard, Callback_data
import pymysql
from validate_email import validate_email

# запуск бота
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1111",
    database="botDB"
)
incorrect_input_text = "Упс, кажется ты ввел(а) что-то не так. Попробуй ещё раз"
already_registered_text = ", ты уже зарегистрирован(а) на Госуслугах Дети"
bot = telebot.TeleBot(TOKEN)

# проверка
def checkName(name):
    if len(name.split(' ')) == 3 and len(name.split(" ")[0]) > 1 and len(name.split(" ")[1]) > 1 and len(name.split(" ")[2]) > 1:
        return True
    return False


def checkDate(date):
    data = date.split(".")
    if len(data) != 3:
        return False
    if data[0].isdigit() and data[1].isdigit() and data[2].isdigit() and int(data[0]) in range(1, 32) and data[1] in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] and \
            int(data[2]) in range(2004, 2019):
        return True


# обработка callback от кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == Callback_data[6]:
        with connection.cursor() as cur:
            cur.execute('select * from clubs')
            dt = cur.fetchall()
        handle_show(call.message, dt)
    elif call.data == Callback_data[7]:
        handle_filter(call.message)
    elif call.data == Callback_data[8]:
        handle_show(call.message, sorting(1))
    elif call.data == Callback_data[9]:
        with connection.cursor() as cur:
            cur.execute('select * from users where tId = {}'.format(str(call.message.chat.id)))
            dt = cur.fetchall()
        handle_show(call.message, sorting([dt[0][11], dt[0][12]]))
    elif call.data == Callback_data[10]:
        handle_filter_types(call.message)
    elif call.data == Callback_data[0]:
        print('Отфильтровано по типу(спорт)')
    elif call.data == Callback_data[1]:
        print('Отфильтровано по типу(программирование)')
    elif call.data == Callback_data[2]:
        print('Отфильтровано по типу(рисование)')
    elif call.data == Callback_data[3]:
        print('Отфильтровано по типу(шахматы)')
    elif call.data == Callback_data[4]:
        print('Отфильтровано по типу(музыка)')
    elif call.data == Callback_data[13]:
        handle_sent_mail(call.message)
    elif call.data == Callback_data[14]:
        handle_menu(call.message)
    elif call.data == Callback_data[15]:
        handle_show_profile(call.message)
    elif call.data == Callback_data[16]:
        handle_edit_profile(call.message)


# функции
@bot.message_handler(commands=['menu'])

def handle_menu(message):
    tID = message.chat.id
    with connection.cursor() as cur:
        cur.execute('select kid_firstname, kid_lastname from users where tID = {}'.format(message.chat.id))
        name = cur.fetchall()
    if name:
        bot.send_message(message.chat.id, text=('Чем займёмся на этот раз, ' + str(name[0][1]) + '?'), reply_markup=take_keyboard('0'))
    else:
        bot.send_message(tID, "Ты ещё не зарегистрирован(а) в Госуслугах Дети, напиши /start")


# вывод мероприятий
@bot.message_handler(commands=['info'])
def handle_info(message, num):
    data = take_info_clubs(message.chat.id, int(num))
    info = data[0]
    bot.send_location(message.chat.id, data[1][1], data[1][0])
    bot.send_message(message.chat.id, info, reply_markup=take_keyboard('o1'))


def handle_show(message, data):
    bot.send_message(message.chat.id, text=take_base_clubs(data))
    bot.send_message(message.chat.id, text='Напиши номер кружка, чтобы получить подробную информацию и записаться')


# запись
@bot.message_handler(commands=['sent_mail'])
def handle_sent_mail(message):
    with connection.cursor() as cur:
        cur.execute('select parent_email, parent_lastname, parent_patronymic, kid_lastname, kid_firstname from users where tID = {}'.format(message.chat.id))
        mail_data = cur.fetchall()
    with connection.cursor() as cur:
        cur.execute('select ')
    print(mail_data)
    bot.send_message(message.chat.id, text='Информация о выбранном тобой кружке отправлена родителю. Удачи на занятиях!')
    mail_out(mail_data[0][0], mail_data[0][1], mail_data[0][2], mail_data[0][4], mail_data[0][3], "тестовое имя", "тестовая цена", "тестовая локация")
    handle_menu(message)


# фильтрация
@bot.message_handler(commands=['filter_types'])
def handle_filter_types(message):
    bot.send_message(message.chat.id, text='Выберите направление кружка', reply_markup=take_keyboard('f1'))


@bot.message_handler(commands=['filter'])
def handle_filter(message):
    bot.send_message(message.chat.id, 'Доступные фильтры', reply_markup=take_keyboard('f2'))


def sorting(tag):
    with connection.cursor() as cur:
        cur.execute('select * from clubs')
        data = cur.fetchall()
    if tag == 1:
        data = sorted(data, key=lambda x: x[tag])
    else:
        data = sorted(data, key=lambda x: distance_calc(x[2], x[3], tag[0], tag[1]))
    return data


# регистрация и тест
@bot.message_handler(commands=['start'])
def handle_start(message):
    tID = message.chat.id
    with connection.cursor() as cursor:
        cursor.execute("select kid_firstname, kid_lastname from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
    if not data:
        with connection.cursor() as cursor:
            cursor.execute("insert into users (tID) VALUES (\"" + str(tID) + "\")")
            connection.commit()
        bot.send_message(tID, "Привет! Добро пожаловать в Госуслуги Дети! Здесь ты сможешь найти кружок или секцию по своим предпочтениям")
        bot.send_message(
            tID, "Чтобы я помог тебе, мне нужно узнать немного инфрормации о тебе")
        msg = bot.send_message(
            tID, "Напиши свою фамилию, имя и отчество через пробел")
        bot.register_next_step_handler(msg, input_name)
    else:
        bot.send_message(tID, str(data[0][1]) + ", ты уже зарегистрирован(а) на Госуслугах Дети.\nНапиши /menu")


def input_name(message):
    tID = message.chat.id
    data = message.text
    if not checkName(data):
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, input_name)
    else:
        with connection.cursor() as cursor:
            cursor.execute("update users set kid_firstname = \"" +
                           data.split(" ")[0] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set kid_lastname = \"" +
                           data.split(" ")[1] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set kid_patronymic = \"" +
                           data.split(" ")[2] + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()

        bot.send_message(
            tID, "Приятно познакомиться, " + data.split(" ")[1])
        msg = bot.send_message(
            tID, "Отправь мне свою дату рождения в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(msg, input_date_birth)


def input_date_birth(message):
    tID = message.chat.id
    data = message.text
    if checkDate(data):
        with connection.cursor() as cursor:
            cursor.execute("update users set birth_date = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "Записал дату рождения")
        msg = bot.send_message(
            tID, "Если у тебя есть сертификат ПФДО, отправь мне его номер. Если нет, отправь 0")
        bot.register_next_step_handler(msg, input_pfdo)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, input_date_birth)


def input_pfdo(message):
    tID = message.chat.id
    data = message.text
    if data == "0":
        bot.send_message(tID, "Понял, ставлю прочерк")
        with connection.cursor() as cursor:
            cursor.execute("update users set cert_number = \"" +
                           "0" + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(
            tID, "Теперь введи фамилию, имя и отчество одного из родителей")
        bot.register_next_step_handler(msg, input_parent_name)
    elif data.isdigit():
        with connection.cursor() as cursor:
            cursor.execute("update users set cert_number = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(
            tID, "Хорошо, что у тебя есть сертификат ПФДО, он позволит обучаться в большем количестве секций")
        msg = bot.send_message(
            tID, "Напиши фамилию, имя и отчество одного из родителей через пробел")
        bot.register_next_step_handler(msg, input_parent_name)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, input_pfdo)


def input_parent_name(message):
    tID = message.chat.id
    data = message.text
    if not checkName(data):
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, input_parent_name)
    else:
        with connection.cursor() as cursor:
            cursor.execute("update users set parent_firstname = \"" +
                           data.split(" ")[0] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set parent_lastname = \"" +
                           data.split(" ")[1] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set parent_patronymic = \"" +
                           data.split(" ")[2] + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(
            tID, "Отправь рабочую электронную почту родителя")
        bot.register_next_step_handler(msg, input_email)


def input_email(message):
    tID = message.chat.id
    data = message.text
    if validate_email(data, check_mx=True):
        with connection.cursor() as cursor:
                cursor.execute("update users set parent_email = \"" +
                               data + "\" where tID = \"" + str(tID) + "\"")
                connection.commit()
        msg = bot.send_message(
            tID, "Отправь мне местоположение своего дома, чтобы найти кружки поблизости")
        bot.register_next_step_handler(msg, get_location)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, input_email)

@bot.message_handler(content_types=["location"])
def get_location(message):
    # ДОБАВИТЬ В БАЗУ ДАННЫХ
    tID = message.chat.id
    data= str(message.location)
    posX = data[14:23]
    posY = data[37:45]
    with connection.cursor() as cursor:
            cursor.execute("update users set posX = \"" +
                           str(posX) + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set posY = \"" +
                           str(posY) + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
    bot.send_message(tID, "Уже подбираю тебе кружки около твоего дома...")
    with connection.cursor() as cursor:
        cursor.execute("select kid_firstname, kid_lastname from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
    bot.send_message(
        tID, "Ура! " + str(data[0][1]) + ", у тебя получилось зарегистрироваться!\nЧтобы начать искать кружки, мне нужно узнать, чем ты увлекаешься\nНапиши /quiz")

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    tID = message.chat.id
    with connection.cursor() as cursor:
        cursor.execute("select kid_firstname, kid_lastname, categories from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
    if data[0][2] != "":
        bot.send_message(tID, data[0][1] +", ты уже ответил(а) на вопросы, напиши /menu")
    elif not data[0][2]:
        bot.send_message(tID, "Давай узнаем о твоих увлечениях. Отвечай \"да\" или \"нет\"")
        msg = bot.send_message(tID, "Любишь заниматься спортом?")
        bot.register_next_step_handler(msg, pick_sport)
    else:
        bot.send_message(tID, "Ты ещё не зарегистрирован в ГосУслугах Дети, напиши /start")

def pick_sport(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = \"" +
                           "1" + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
            msg = bot.send_message(tID, "Как насчёт технологий IT?")
            bot.register_next_step_handler(msg, pick_it)
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Как насчёт технологий IT?")
        bot.register_next_step_handler(msg, pick_it)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_sport)

def pick_it(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = CONCAT(categories, \"" +
                           "2" + "\") where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(tID, "Увлекаешься рисованием?")
        bot.register_next_step_handler(msg, pick_painting)
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Увлекаешься рисованием?")
        bot.register_next_step_handler(msg, pick_painting)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_it)


def pick_painting(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = CONCAT(categories,\"" +
                           "3" + "\") where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(tID, "Увлекаешься шахматами?")
        bot.register_next_step_handler(msg, pick_chess)
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Увлекаешься шахматами?")
        bot.register_next_step_handler(msg, pick_chess)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_painting)

def pick_chess(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = CONCAT(categories,\"" +
                           "4" + "\") where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(tID, "Может любишь поиграть на музыкальных инструментах?")
        bot.register_next_step_handler(msg, pick_music)
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Может любишь поиграть на музыкальных инструментах?")
        bot.register_next_step_handler(msg, pick_music)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_chess)

def pick_music(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = CONCAT(categories,\"" +
                           "4" + "\") where tID = \"" + str(tID) + "\"")
        connection.commit()
        msg = bot.send_message(tID, "Отлично, я запомнил все твои увлечения! Начинай выбирать, просто напиши /menu")
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Отлично, я запомнил все твои увлечения! Начинай выбирать, просто напиши /menu")
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_music)


# профиль
@bot.message_handler(commands=['showprofile'])
def handle_show_profile(message):
    tID = message.chat.id

    with connection.cursor() as cursor:
        cursor.execute("select * from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
    if data:
        bot.send_message(tID, "Информация из профиля:")
        dict = {"1": ", Спорт", "2": ", Технологии IT", "3": ", Рисование", "4": ", Шахматы", "5": ", Музыка"}
        cat = ""
        for a in data[0][13]:
            cat = cat + dict[a]

        info_pro = "Твоё ФИО: " + str(data[0][0]) + " " + str(data[0][1]) + " " + data[0][2] + "\n" + \
        "Твоя дата рождения: " + data[0][10] + "\n" + \
        "Номер сертификата ПФДО: " + data[0][9] + "\n" + \
        "ФИО Родителя: " + str(data[0][3]) + " " + str(data[0][4]) + " " + data[0][5] + "\n" + \
        "Электронная почта: " + data[0][8] + "\n" + \
        "Твои интересы: " + cat[2:] + \
        "\nДля редактирования напиши /editprofile"
        bot.send_message(message.chat.id, text=info_pro)
    else:
        bot.send_message(tID, "Ты ещё не зарегистрирован(а) в Госуслугах Дети, напиши /start")


@bot.message_handler(commands=['editprofile'])
def handle_edit_profile(message):
    tID = message.chat.id
    with connection.cursor() as cursor:
        cursor.execute("select * from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
    if data:
        bot.send_message(tID, "Данные из профиля:")
        dict = {"1":", Спорт", "2":", Технологии IT","3":", Рисование","4":", Шахматы","5":", Музыка"}
        cat = ""
        for a in data[0][13]:
            cat = cat + dict[a]
        info = "1. Твоё ФИО: " + str(data[0][0]) + " " + str(data[0][1]) + " " + data[0][2] + "\n" + \
            "2. Твоя дата рождения: " + data[0][10] + "\n" + \
            "3. Номер сертификата ПФДО: " + data[0][9] + "\n" + \
            "4. ФИО Родителя: " + str(data[0][3]) + " " + str(data[0][4]) + " " + data[0][5] + "\n" + \
            "5. Электронная почта: " + data[0][8] + "\n" + \
            "6. Твои интересы: " + cat[2:]
        bot.send_message(tID, info)
        msg = bot.send_message(tID, "Выбери номер строки, которую хочешь изменить")
        bot.register_next_step_handler(msg, pick_line)
    else:
        bot.send_message(tID, "Ты ещё не зарегистрирован(а) в Госуслугах Дети, напиши /start")

def pick_line(message):
    tID = message.chat.id
    num = message.text
    if num.isdigit() and len(num) == 1 and int(num) in range(1,7):
        num = int(num)
        if num == 1:
            msg = bot.send_message(tID, "Введи свою фамилию, имя и отчество через пробел")
            bot.register_next_step_handler(msg, commit_kid_name)
        elif num == 2:
            msg = bot.send_message(tID, "Введи свою дату рождения в формате ДД.ММ.ГГГГ")
            bot.register_next_step_handler(msg, commit_birth_date)
        elif num == 3:
            msg = bot.send_message(tID, "Введи номер сертификата ПФДО, если его нет, введи 0")
            bot.register_next_step_handler(msg, commit_pfdo_num)

        elif num == 4:
            msg = bot.send_message(tID, "Введи фамилию, имя и отчество родителя через пробел")
            bot.register_next_step_handler(msg, commit_parent_name)

        elif num == 5:
            msg = bot.send_message(tID, "Введи действующую электронную почту родителя")
            bot.register_next_step_handler(msg, commit_parent_email)

        elif num == 6:
            msg = bot.send_message(tID, "Введи цифры направлений, которые тебе интересны, например, 124\n1. Спорт\n2. Технологии IT\n3. Рисование\n4. Шахматы\n5. Музыка")
            bot.register_next_step_handler(msg, commit_categories)
        else:
            msg = bot.send_message(tID, incorrect_input_text)
            bot.register_next_step_handler(msg, pick_line)

def commit_kid_name(message):
    tID = message.chat.id
    data = message.text
    if not checkName(data):
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_kid_name)
    else:
        with connection.cursor() as cursor:
            cursor.execute("update users set kid_firstname = \"" +
                           data.split(" ")[0] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set kid_lastname = \"" +
                           data.split(" ")[1] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set kid_patronymic = \"" +
                           data.split(" ")[2] + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()

        bot.send_message(
            tID, "Твоё ФИО успешно обновлено")

def commit_birth_date(message):
    tID = message.chat.id
    data = message.text
    if checkDate(data):
        with connection.cursor() as cursor:
            cursor.execute("update users set birth_date = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "Твоя дата рождения обновлена")
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_birth_date)

def commit_pfdo_num(message):
    tID = message.chat.id
    data = message.text
    if data == "0":
        with connection.cursor() as cursor:
            cursor.execute("update users set cert_number = \"" +
                           "0" + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "Твой номер сертификата ПФДО обновлён")
    elif data.isdigit():
        with connection.cursor() as cursor:
            cursor.execute("update users set cert_number = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "Твой номер сертификата ПФДО обновлён")
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_pfdo_num)

def commit_parent_name(message):
    tID = message.chat.id
    data = message.text
    if not checkName(data):
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_parent_name)
    else:
        with connection.cursor() as cursor:
            cursor.execute("update users set parent_firstname = \"" +
                           data.split(" ")[0] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set parent_lastname = \"" +
                           data.split(" ")[1] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set parent_patronymic = \"" +
                           data.split(" ")[2] + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "ФИО твоего родителя обновлено")

def commit_parent_email (message):
    tID = message.chat.id
    data = message.text
    with connection.cursor() as cursor:
            cursor.execute("update users set parent_email = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
    bot.send_message(tID, "Электронная почта твоего родителя обновлена")
    # ПРОВЕРКА ПОЧТЫ

def commit_categories(message):
    tID = message.chat.id
    data = message.text
    if not data.isdigit():
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_categories)
    else:
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = \"" +
                            data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit
        bot.send_message(tID, "Твой список интересов обновлён")


# контроль ввода
@bot.message_handler(func=lambda text:True)
def text_check(message):
    with connection.cursor() as cur:
        cur.execute('select * from clubs')
        db = cur.fetchall()
    try:
        if 0 < int(message.text) <= len(db):
            handle_info(message, int(message.text))
    except Exception as e:
        print(e)


bot.polling()