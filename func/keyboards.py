from telebot import types
Callback_data = ['Sport', 'Programming', 'Drawing', 'Chess', 'Music', 'Apply',
                 'Show_activities', 'Filter', 'Cost', 'Most_close', 'Type',
                 'Yes', 'No', 'Write', 'Back', 'show_profile', 'edit_profile']


def take_keyboard(num):
    if num == 'r1':
        b1 = types.InlineKeyboardButton(text='Да', callback_data=Callback_data[11])
        b2 = types.InlineKeyboardButton(text='Нет', callback_data=Callback_data[12])
        keyboard = types.InlineKeyboardMarkup([[b1], [b2]])
    elif num == '0':
        b1 = types.InlineKeyboardButton(text='Посмотреть все секции и кружки', callback_data=Callback_data[6])
        b2 = types.InlineKeyboardButton(text='Включить поиск по фильтрам', callback_data=Callback_data[7])
        b3 = types.InlineKeyboardButton(text='Данные профиля', callback_data=Callback_data[15])
        keyboard = types.InlineKeyboardMarkup([[b1], [b2], [b3]])
    elif num == 'f1':
        b1 = types.InlineKeyboardButton(text='Спорт', callback_data=Callback_data[0])
        b2 = types.InlineKeyboardButton(text='Программирование', callback_data=Callback_data[1])
        b3 = types.InlineKeyboardButton(text='Рисование', callback_data=Callback_data[2])
        b4 = types.InlineKeyboardButton(text='Шахматы', callback_data=Callback_data[3])
        b5 = types.InlineKeyboardButton(text='Музыка', callback_data=Callback_data[4])
        b6 = types.InlineKeyboardButton(text='')
        keyboard = types.InlineKeyboardMarkup([[b1], [b2], [b3], [b4], [b5]])
    elif num == 'f2':
        b1 = types.InlineKeyboardButton(text='По стоимости', callback_data=Callback_data[8])
        b2 = types.InlineKeyboardButton(text='По расстоянию', callback_data=Callback_data[9])
        b3 = types.InlineKeyboardButton(text='По интересам', callback_data=Callback_data[10])
        keyboard = types.InlineKeyboardMarkup([[b1], [b2], [b3]])
    elif num == 'o1':
        b1 = types.InlineKeyboardButton(text='Записаться', callback_data=Callback_data[13])
        b2 = types.InlineKeyboardButton(text='Назад', callback_data=Callback_data[14])
        keyboard = types.InlineKeyboardMarkup([[b1], [b2]])
    elif num == 'r2':
        b1 = types.InlineKeyboardButton(text='Редактирование профиля', callback_data=Callback_data[16])
        b2 = types.InlineKeyboardButton(text='Назад', callback_data=Callback_data[14])
        keyboard = types.InlineKeyboardButton([[b1], [b2]])
    return keyboard
