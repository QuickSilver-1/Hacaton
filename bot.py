from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import *
from media import *
from config import config_1
from psycopg2 import connect
from psycopg2 import connect
from re import match

class Form(StatesGroup):
    fio = State()
    age = State()
    problem = State()
    number = State()

class Admin(StatesGroup):
    answer_msg = State()

class Register(StatesGroup):
    fio = State()
    email = State()
    number = State()
    username = State()
    password = State()

class Sign_in(StatesGroup):
    email = State()
    password = State()

dp = Dispatcher()
bot = Bot(token=config_1.TOKEN)

@dp.message(F.photo)
async def photo_handler(message: Message) -> None:
    photo_data = message.photo[-1]
    await message.answer(f'{photo_data}')

@dp.message(F.video)
async def photo_handler(message: Message) -> None:
    photo_data = message.video
    await message.answer(f'{photo_data}')

@dp.message(F.document)
async def photo_handler(message: Message) -> None:
    photo_data = message.document

    await message.answer(f'{photo_data}')

@dp.message(F.voice)
async def photo_handler(message: Message) -> None:
    photo_data = message.voice.file_id

    await message.answer(f'{photo_data}')

@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT COUNT(*) FROM "person" WHERE tg_id = {message.from_user.id}''')
    if len(cursor.fetchall()) != 0:
        await message.answer_photo(photo=start_photo, caption=start_text, reply_markup=give_start_kb())
    else:
        await message.answer(text="Для доступа к боту нужно иметь аккаунта на сайте Фонда. Он у вас есть?", reply_markup=have_acc_kb())

@dp.callback_query(F.data == "Нету")
async def register(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.fio)
    await state.update_data(username=callback.message.from_user.username, tg_id=callback.message.from_user.id)
    await callback.message.answer(text="Тогда нужно пройти небольшую регистрацию. Введите ФИО в формате 'Иванов Иван Иванович'")

@dp.callback_query(F.data == "Есть")
async def sign_in(callback: CallbackQuery, state: FSMContext):
    await

@dp.message(Register.fio)
async def reg_fio(message: Message, state: FSMContext) -> None:
    try:
        last_name, first_name, second_name = message.text.split()
    except:
        await message.answer(text="Неправильный формат данных, попробуйте снова")
        return None
    await state.update_data(first_name=first_name, last_name=last_name, second_name=second_name)
    await state.set_state(Register.email)
    await message.answer(text="Введите свою почту")

@dp.message(Register.email)
async def reg_email(message: Message, state: FSMContext) -> None:
    if match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', message.text) is None:
        await message.answer(text="Неправильный формат данных, попробуйте снова")
    else:
        connection = connect(config_1.POSTGRES_URL)
        cursor = connection.cursor()
        cursor.execute(f'''SELECT COUNT(*) FROM "person" WHERE email = {message.text}''')
        if cursor.fetchall()[0] > 0:
            await message.answer(text="Пользователь с такой почтой уже есть", reply_markup=sign_in_kb())
        else:
            await state.update_data(email=message.text)
            await state.set_state(Register.number)
            await message.answer(text="Введите номер своего телефона")

@dp.message(Register.number)
async def reg_number(message: Message, state: FSMContext) -> None:
    if match("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message.text):
        await message.answer(text="Неправильный формат данных, попробуйте снова")
    else:
        await state.update_data(number=message.text)
        await state.set_state(Register.username)
        await message.answer(text="Придумайте себе имя пользователя\nОно должно состоять из символов латинского алфавита, цифр, а также символов: _ $ ^ #\nДлина от 3 до 15 символов")

@dp.message(Register.username)
async def reg_username(message: Message, state: FSMContext) -> None:
    if match("^[a-zA-Z0-9_$^#]+$", message.text) is None or len(message.text) < 3 or len(message.text) > 15:
        await message.answer(text="Неправильный формат данных, попробуйте снова")
    else:
        await state.update_data(username=message.text)
        await state.set_state(Register.password)
        await message.answer(text="Придумайте себе имя пароль\nОно должно состоять из символов латинского алфавита, цифр, а также символов: _ $ ^ #\nДлина от 3 до 15 символов")

@dp.message(Register.password)
async def reg_password(message: Message, state: FSMContext) -> None:
    if match("^[a-zA-Z0-9_$^#]+$", message.text) is None or len(message.text) < 3 or len(message.text) > 15:
        await message.answer(text="Неправильный формат данных, попробуйте снова")
    else:
        await state.update_data(password=message.text)
        await message.answer(text="Запомните пароль. Далнейший вход в систему будет осуществлять через него", reply_markup=password_kb())

@dp.callback_query(F.data == "Запомнил")
async def reg_final(callback: CallbackQuery, state: FSMContext):
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO "person" (username_tg, )''')

@dp.callback_query(F.data == "Узнать больше")
async def learn_more(callback: CallbackQuery) -> None:
    await callback.message.answer(text="Мы можем предложить следующую помощь", reply_markup=give_service_kb())

@dp.callback_query(F.data == "Экстренная помощь")
async def fast_help(callback: CallbackQuery) -> None:
    await callback.message.answer(text=help_txt)

@dp.callback_query(F.data == "Узнать больше о раке груди")
async def learn_more_cancer(callback: CallbackQuery) -> None:
    await callback.message.answer(text=checklist_text, reply_markup=learn_more_kb())

@dp.callback_query(F.data == "Связь с Фондом")
async def connect_with_found(callback: CallbackQuery) -> None:
    await callback.message.answer(text=found_text, reply_markup=found_kb())

@dp.callback_query(F.data == "Как сохранить здоровье груди")
async def check_list(callback: CallbackQuery) -> None:
    await callback.message.answer_document(text=checklist_text, document=checklist_file)

@dp.callback_query(F.data == "Соединить с сотрудником Фонда")
async def connect_with_staff(callback: CallbackQuery) -> None:
    await callback.message.answer(text=staff_text, reply_markup=give_staff_kb())

@dp.callback_query(F.data == "Онколог")
async def register_oncolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Онкологу")
    await state.set_state(Form.fio)
    await callback.message.answer(text="1/4 | Напишите своё ФИО")

@dp.callback_query(F.data == "Лимфолог")
async def register_limfolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Лимфологу")
    await state.set_state(Form.fio)
    await callback.message.answer(text="1/4 | Напишите своё ФИО")

@dp.callback_query(F.data == "Эндокринолог")
async def register_endocrinolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Эндокринологу")
    await state.set_state(Form.fio)
    await callback.message.answer(text="1/4 | Напишите своё ФИО")

@dp.callback_query(F.data == "Диетолог")
async def register_dietolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Диетологу")
    await state.set_state(Form.fio)
    await callback.message.answer(text="1/4 | Напишите своё ФИО")

@dp.callback_query(F.data == "Дерматолог")
async def register_dermotolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Дерматологу")
    await state.set_state(Form.fio)
    await callback.message.answer(text="1/4 | Напишите своё ФИО")

@dp.callback_query(F.data == "Сотрудник фонда")
async def sign_up(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Сотруднику фонда")
    await state.set_state(Form.fio)
    await callback.message.answer(text="1/4 | Напишите своё ФИО")

@dp.message(Form.fio)
async def register_fio(message: Message, state: FSMContext) -> None:
    await state.update_data(fio=message.text)
    await state.set_state(Form.age)
    await message.answer(text="2/4 | Напишите свой возраст")

@dp.message(Form.age)
async def register_age(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await state.set_state(Form.problem)
    await message.answer(text="3/4 | Опишите свою проблему в паре предложений")

@dp.message(Form.problem)
async def register_age(message: Message, state: FSMContext) -> None:
    await state.update_data(problem=message.text)
    await state.set_state(Form.number)
    await message.answer(text="4/4 | Напишите свой номер")

@dp.message(Form.number)
async def send_sign_call(message: Message, state: FSMContext) -> None:
    username = message.from_user.username
    data = await state.get_data()
    doctor = data.get("doctor")
    fio = data.get("fio")
    age = data.get("age")
    problem = data.get("problem")
    number = message.text
    chat_id = "-4218092750"
    await bot.send_message(chat_id,
                           text=f"Пользователь: @{username} \nОставил заявку на консультацию у {doctor}\nФИО: {fio}\nНомер телефона {number} \nВозраст: {age}\nПроблема: {problem}",
                           reply_markup=answer_kb(message.from_user.id))
    await message.answer("Спасибо за обращение! Вами скоро напишут")

@dp.callback_query(F.data.startswith("Ответить"))
async def answer_to_user(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admin.answer_msg)
    await state.update_data(id=callback.data[8:])
    await callback.message.answer(text="Напишите ответ ниже")

@dp.message(Admin.answer_msg)
async def are_you_shure(message: Message, state: FSMContext) -> None:
    await state.update_data(answer=message.text)
    msg_for_delete = await message.answer(text="Вы уверены, что хотите отправить это сообщение?", reply_markup=are_you_shure_kb())
    await state.update_data(msg_del=msg_for_delete.message_id)

@dp.callback_query(F.data == "Да")
async def im_shure(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_id=data.get("id"), text=data.get("answer"))
    await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=data.get("msg_del"))
    await callback.message.answer(text="Сообщение отправлено")

@dp.callback_query(F.data == "Нет")
async def im_shure(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=data.get("msg_del"))
    await callback.message.answer(text="Сообщение не отправлено")