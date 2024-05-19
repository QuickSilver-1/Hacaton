from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from media import *
from aiogram.types import WebAppInfo


main_reply_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Интенсив"), KeyboardButton(text="Женский клуб"), KeyboardButton(text="Личная работа")]],
    resize_keyboard=True
)

def give_start_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Узнать больше", callback_data="Узнать больше"
    )
    builder.button(
        text="Экстренная помощь", callback_data="Экстренная помощь"
    )

    builder.adjust(1)
    return builder.as_markup()

def give_service_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Узнать больше о раке груди", callback_data="Узнать больше о раке груди"
    )
    builder.button(
        text="Мнение врача", callback_data="Онколог"
    )
    builder.button(
        text="Лечение по ОМС бесплатно", callback_data="Лечение по ОМС бесплатно"
    )
    builder.button(
        text="Получить помощь Фонда", callback_data="Получить помощь Фонда"
    )
    builder.button(
        text="Школа пациента (F.A.Q)", callback_data="Школа пациента"
    )
    builder.button(
        text="Оставить отзыв о Фонде", callback_data="Оставить отзыв о Фонде"
    )
    builder.button(
        text="Помочь Фонду", callback_data="Помочь Фонду"
    )
    builder.button(
        text="Рассказать свою историю", callback_data="Поделиться своим опытом"
    )

    builder.adjust(1)
    return builder.as_markup()

def learn_more_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Вернуться в главное меню", callback_data="Узнать больше"
    )
    builder.button(
        text="Как сохранить здоровье груди", callback_data="Как сохранить здоровье груди"
    )
    builder.button(
        text="Как узнать свой риск", web_app=WebAppInfo(url="https://dalshefond.ru/check/")
    )
    builder.button(
        text="Как лечится рак груди", url="https://vmesteplus.ru/distance-programs/oncologist-course/"
    )

    builder.adjust(1)
    return builder.as_markup()

def give_staff_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Онколог", callback_data="Онколог"
    )
    builder.button(
        text="Лимфолог", callback_data="Лимфолог"
    )
    builder.button(
        text="Эндокринолог", callback_data="Эндокринолог"
    )
    builder.button(
        text="Диетолог", callback_data="Диетолог"
    )
    builder.button(
        text="Дерматолог", callback_data="Дерматолог"
    )
    builder.button(
        text="Сотрудник фонда", callback_data="Сотрудник фонда"
    )
    builder.button(
        text="Вернуться в главное меню", callback_data="Узнать больше"
    )

    builder.adjust(2)
    return builder.as_markup()

def answer_kb(id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Ответить", callback_data=f"Ответить{id}"
    )

    builder.adjust(1)
    return builder.as_markup()

def are_you_shure_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Да", callback_data="Да"
    )
    builder.button(
        text="Нет", callback_data="Нет"
    )

    builder.adjust(2)
    return builder.as_markup()

def have_acc_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Есть", callback_data="Есть"
    )
    builder.button(
        text="Нет", callback_data="Нету"
    )

    builder.adjust(2)
    return builder.as_markup()

def sign_in_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Войти", callback_data="Есть"
    )

    builder.adjust(1)
    return builder.as_markup()

def sign_up_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Зарегестрироваться", callback_data="Нету"
    )

    builder.adjust(1)
    return builder.as_markup()


def password_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Запомнил", callback_data="Запомнил"
    )

    builder.adjust(1)
    return builder.as_markup()

def skip_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Закончить", callback_data="Пропустить"
    )

    builder.adjust(1)
    return builder.as_markup()

def who_are_you_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Физ.лицо", callback_data="Физ.лицо"
    )
    builder.button(
        text="Юр.лицо", callback_data="Юр.лицо"
    )

    builder.adjust(2)
    return builder.as_markup()

def fiz_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Сделать пожертвование", web_app=WebAppInfo(url="https://dalshefond.ru/donate/")
    )
    builder.button(
        text="Получить ссылку для друга", callback_data="Получить ссылку для друга"
    )

    builder.adjust(1)
    return builder.as_markup()

def help_for_found_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Пособие для пациентов", callback_data="Пособие для пациентов"
    )
    builder.button(
        text="Консультация психолога", callback_data="Психолог"
    )
    builder.button(
        text="Консультация мед. юриста", callback_data="Мед.юрист"
    )
    builder.button(
        text="Бесплатное такси к месту лечения", web_app=WebAppInfo(url="https://vmesteplus.ru/support/how/targeted-assistance/")
    )
    builder.button(
        text="Связь с сотрудником Фонда", callback_data="Соединить с сотрудником Фонда"
    )
    builder.button(
        text="Вернуться в главное меню", callback_data="Узнать больше"
    )

    builder.adjust(1)
    return builder.as_markup()

def oms_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Как попасть к онкологу", callback_data="Как попасть к онкологу"
    )
    builder.button(
        text="Где пройти обследование", callback_data="Где пройти обследование"
    )
    builder.button(
        text="Вернуться на главную", callback_data="Узнать больше"
    )

    builder.adjust(1)
    return builder.as_markup()

def back_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Вернуться в главное меню", callback_data="Узнать больше"
    )

def visit_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Записаться к онкологу", callback_data="Онколог"
    )
    builder.button(
        text="В главное меню", callback_data="Узнать больше"
    )

    builder.adjust(1)
    return builder.as_markup()