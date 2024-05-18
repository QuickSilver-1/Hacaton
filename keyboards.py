from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from media import *
from aiogram.types import WebAppInfo
from psycopg2 import connect
from json import dumps


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
        text="Мнение врача", callback_data="Мнение врача"
    )
    builder.button(
        text="Лечение по ОМС бесплатно", callback_data="Лечение по ОМС бесплатно"
    )
    builder.button(
        text="Получить помощь Фонда", callback_data="Получить помощь Фонда"
    )
    builder.button(
        text="Психологическая поддержка", callback_data="Психологическая поддержка"
    )
    builder.button(
        text="Связь с Фондом", callback_data="Связь с Фондом"
    )

    builder.adjust(1)
    return builder.as_markup()

def found_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Оставить отзыв о работе Фонда", callback_data="Оставить отзыв о работе Фонда"
    )
    builder.button(
        text="Связь с сотрудником Фонда", callback_data="Связь с сотрудником Фонда"
    )
    builder.button(
        text="Помочь Фонду", callback_data="Помочь Фонду"
    )

    builder.adjust(1)
    return builder.as_markup()

def learn_more_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Хочу получить помощь Фонда", callback_data="Узнать больше"
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
    builder.button(
        text="Навигатор для пациента", callback_data="Навигатор для пациента"
    )
    builder.button(
        text="Соединить с сотрудником Фонда", callback_data="Соединить с сотрудником Фонда"
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
        text="Сотрудник фонда", callback_data="Онколог"
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

def sign_in_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Войти", callback_data="Есть"
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