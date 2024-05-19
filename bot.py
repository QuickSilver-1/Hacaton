from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder
from keyboards import *
from media import *
from config import config_1
from psycopg2 import connect
from re import match

class Form(StatesGroup):
    fio = State()
    age = State()
    problem = State()
    number = State()
    media = State()

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

class Review(StatesGroup):
    fio = State()
    age = State()
    city = State()
    review = State()
    mark = State()

class Location(StatesGroup):
    region = State()

class Faq(StatesGroup):
    num = State()

class Story(StatesGroup):
    msg = State()

dp = Dispatcher()
bot = Bot(token=config_1.TOKEN)

@dp.message(CommandStart())
async def cmd_start(message: Message, reg = False) -> None:
    if reg == True:
        await message.answer_photo(photo=start_photo, caption=start_text, reply_markup=give_start_kb())
    else:
        await message.answer(text="Для доступа к боту нужно иметь аккаунта на сайте Фонда. Он у вас есть?", reply_markup=have_acc_kb())

@dp.callback_query(F.data == "Нету")
async def register(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.fio)
    await state.update_data(username=callback.message.from_user.username, tg_id=callback.message.from_user.id)
    await callback.message.answer(text="Вам нужно пройти небольшую регистрацию. Введите ФИО в формате 'Иванов Иван Иванович'")

@dp.callback_query(F.data == "Есть")
async def sign_in(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Sign_in.email)
    await callback.message.answer(text="Введите свой email")

@dp.message(Sign_in.email)
async def sign_in_email(message: Message, state: FSMContext):
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT COUNT(*) FROM "person" WHERE email = '{message.text}';''')
    if cursor.fetchone()[0] == 0:
        await message.answer(text="Нет такого пользователя. Попробуйте снова или зарегистрируйтесь", reply_markup=sign_up_kb())
    else:
        await state.set_state(Sign_in.password)
        await state.update_data(email=message.text)
        await message.answer(text="Введите пароль")

@dp.message(Sign_in.password)
async def sign_in_password(message: Message, state: FSMContext):
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    data = await state.get_data()
    email = data.get("email")
    cursor.execute(f'''SELECT password FROM "person" WHERE email = '{email}';''')
    password = config_1.crypt.decrypt(cursor.fetchone()[0].encode())
    if password.decode() == message.text:
        await state.clear()
        await cmd_start(message=message, reg=True)
    else:
        await message.answer(text="Неверный пароль")

@dp.message(Register.fio)
async def reg_fio(message: Message, state: FSMContext) -> None:
    try:
        last_name, first_name, second_name = message.text.split()
    except:
        await message.answer(text="Неправильный формат данных, попробуйте снова")
        return None
    await state.update_data(first_name=first_name, last_name=last_name, second_name=second_name, username_tg=message.from_user.username, tg_id=message.from_user.id)
    await state.set_state(Register.email)
    await message.answer(text="Введите свою почту")

@dp.message(Register.email)
async def reg_email(message: Message, state: FSMContext) -> None:
    if match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', message.text) is None:
        await message.answer(text="Неправильный формат данных, попробуйте снова")
    else:
        connection = connect(config_1.POSTGRES_URL)
        cursor = connection.cursor()
        cursor.execute(f'''SELECT COUNT(*) FROM "person" WHERE email = '{message.text}';''')
        if cursor.fetchone()[0] > 0:
            await message.answer(text="Пользователь с такой почтой уже есть", reply_markup=sign_in_kb())
        else:
            await state.update_data(email=message.text)
            await state.set_state(Register.number)
            await message.answer(text="Введите номер своего телефона")

@dp.message(Register.number)
async def reg_number(message: Message, state: FSMContext) -> None:
    if match("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message.text) is None:
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
        await message.answer(text="Придумайте себе пароль\nОно должно состоять из символов латинского алфавита, цифр, а также символов: _ $ ^ #\nДлина от 3 до 30 символов")

@dp.message(Register.password)
async def reg_password(message: Message, state: FSMContext) -> None:
    if match("^[a-zA-Z0-9_$^#]+$", message.text) is None or len(message.text) < 3 or len(message.text) > 30:
        await message.answer(text="Неправильный формат данных, попробуйте снова")
    else:
        await state.update_data(password=message.text)
        await message.answer(text="Запомните пароль. Далнейший вход в систему будет осуществлять через него", reply_markup=password_kb())

@dp.callback_query(F.data == "Запомнил")
async def reg_final(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username_tg = data.get("username_tg")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    second_name = data.get("second_name")
    email  = data.get("email")
    tg_id = data.get("tg_id")
    number = data.get("number")
    username = data.get("username")
    password = data.get("password")
    password = config_1.crypt.encrypt(password)
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute(f'''INSERT INTO "person" (username_tg, first_name, last_name, second_name, email, number, tg_id, username, password)
                   VALUES ('{username_tg}', '{first_name}', '{last_name}', '{second_name}', '{email}', '{number}', '{tg_id}', '{username}', '{password.decode()}');''')
    connection.commit()
    await callback.message.answer(text="Регистрация успешно выполнена")
    await state.clear()
    await cmd_start(message=callback.message, reg=True)

@dp.callback_query(F.data == "Узнать больше")
async def learn_more(callback: CallbackQuery) -> None:
    await callback.message.answer_photo(photo=picture_photo, reply_markup=give_service_kb())

@dp.callback_query(F.data == "Экстренная помощь")
async def fast_help(callback: CallbackQuery) -> None:
    await callback.message.answer(text=help_txt)

@dp.callback_query(F.data == "Узнать больше о раке груди")
async def learn_more_cancer(callback: CallbackQuery) -> None:
    await callback.message.answer(text=learn_more_text, reply_markup=learn_more_kb())

@dp.callback_query(F.data == "Как сохранить здоровье груди")
async def check_list(callback: CallbackQuery) -> None:
    await callback.message.answer_document(text=checklist_text, document=checklist_file)

@dp.callback_query(F.data == "Соединить с сотрудником Фонда")
async def connect_with_staff(callback: CallbackQuery) -> None:
    await callback.message.answer(text=staff_text, reply_markup=give_staff_kb())

@dp.callback_query(F.data == "Онколог")
async def register_oncolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Онколога")
    await state.set_state(Form.age)
    await callback.message.answer(text="1/3 | Напишите свой возраст")

@dp.callback_query(F.data == "Лимфолог")
async def register_limfolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Лимфолога")
    await state.set_state(Form.age)
    await callback.message.answer(text="1/3 | Напишите свой возраст")

@dp.callback_query(F.data == "Эндокринолог")
async def register_endocrinolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Эндокринолога")
    await state.set_state(Form.age)
    await callback.message.answer(text="1/3 | Напишите свой возраст")

@dp.callback_query(F.data == "Психолог")
async def register_endocrinolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Психолога")
    await state.set_state(Form.age)
    await callback.message.answer(text="1/3 | Напишите свой возраст")

@dp.callback_query(F.data == "Мед.юрист")
async def register_endocrinolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Мед.юриста")
    await state.set_state(Form.age)
    await callback.message.answer(text="1/3 | Напишите свой возраст")

@dp.callback_query(F.data == "Диетолог")
async def register_dietolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Диетолога")
    await state.set_state(Form.age)
    await callback.message.answer(text="1/3 | Напишите свой возраст")

@dp.callback_query(F.data == "Дерматолог")
async def register_dermotolog(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Дерматолога")
    await state.set_state(Form.age)
    await callback.message.answer(text="1/3 | Напишите свой возраст")

@dp.callback_query(F.data == "Сотрудник фонда")
async def sign_up(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor="Сотрудника фонда")
    await state.set_state(Form.age)
    await callback.message.answer(text="1/3 | Напишите свой возраст")

@dp.message(Form.age)
async def register_age(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await state.set_state(Form.problem)
    await message.answer(text="2/3 | Опишите свою проблему в паре предложений")

@dp.message(Form.problem)
async def registe_file(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if data.get("doctor") in ["Психолога", "Мед.юриста", "Сотрудника фонда"]:
        await message.answer(text="3/3 | Заявка сформирована. Нажми завершить", reply_markup=skip_kb())
    else:
        await state.set_state(Form.media)    
        await message.answer(text="3/3 | Загрузите по одному документы в формате pdf имеющиеся у вас: выписной эпикриз, описание ИГХ, описание УЗИ и Маммографии", reply_markup=skip_kb())
    
    await state.update_data(media='')
    await state.update_data(problem=message.text)
 


@dp.message(Form.media)
async def set_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=data.get("msg"))
    except Exception:
        pass
    await state.update_data(media=data.get("media") + "///" + message.document.file_id)
    
    msg = await message.answer(text="Закончите или есть еще файлы?", reply_markup=skip_kb())
    await state.update_data(msg=msg.message_id)

@dp.callback_query(F.data == "Пропустить")
async def send_sign_call(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    username = callback.from_user.username
    doctor = data.get("doctor")
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT first_name, last_name, second_name FROM "person" WHERE tg_id = '{callback.from_user.id}';''')
    print()
    fio = ' '.join(list(cursor.fetchone()))
    age = data.get("age")
    problem = data.get("problem")
    cursor.execute(f'''SELECT number FROM "person" WHERE tg_id = '{callback.from_user.id}';''')
    number = cursor.fetchone()[0]
    chat_id = "-4218092750"
    media = MediaGroupBuilder()
    if data.get("media") != "":
        for i in data.get("media").split('///')[1:]:
            media.add_document(media=i)
    await bot.send_message(chat_id=chat_id,
                           text=f"Пользователь: @{username}\nОставил заявку на консультацию у {doctor}\nФИО: {fio}\nНомер телефона: {number} \nВозраст: {age}\nПроблема: {problem}",
                           reply_markup=answer_kb(callback.from_user.id))
    if data.get("media") != "":
        await bot.send_message(chat_id=chat_id, text="Приложенные файлы")
        await bot.send_media_group(chat_id=chat_id, media=media.build())
    await callback.message.answer(text="Спасибо за обращение! Вам скоро напишут", reply_markup=back_kb())
    await state.clear()

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
async def im_shure(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await bot.send_message(chat_id=data.get("id"), text=data.get("answer"))
    await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=data.get("msg_del"))
    await callback.message.answer(text="Сообщение отправлено")
    await state.clear()

@dp.callback_query(F.data == "Нет")
async def im_shure(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=data.get("msg_del"))
    await callback.message.answer(text="Сообщение не отправлено")
    await state.clear()

@dp.callback_query(F.data == "Оставить отзыв о Фонде")
async def review(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Review.age)
    await callback.message.answer(text=review_text)

@dp.message(Review.age)
async def review_city(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Review.city)
    await message.answer(text="Напишите ваш город")

@dp.message(Review.city)
async def review_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Review.mark)
    await message.answer(text="Дайте оценку по 10-балльной шкале")
    
@dp.message(Review.mark)
async def review_city(message: Message, state: FSMContext):
    try:
        if int(message.text) >= 0 and int(message.text) <= 10:
            await state.update_data(mark=message.text)
            await state.set_state(Review.review)
            await message.answer(text="Напишите отзыв")
        else:
            message.answer(text="Можно ввести оценку от 0 до 10 включительно. Попробуйте снова")
    except:
        message.answer(text="Неверный формат данных. Попробуйте снова")

@dp.message(Review.review)
async def review_review(message: Message, state: FSMContext):
    data = await state.get_data()
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT first_name, last_name, second_name FROM "person" WHERE tg_id = '{message.from_user.id}';''')
    first_name, last_name, second_name = cursor.fetchone()
    age = data.get("age")
    city = data.get("city")
    mark = data.get("mark")

    cursor.execute(f'''INSERT INTO "review" (tg_id, first_name, last_name, second_nam, age, city, mark, text) VALUES ('{message.from_user.id}', '{first_name}', '{last_name}', '{second_name}', '{age}', '{city}', '{mark}', '{message.text}');''')
    connection.commit()
    await state.clear()
    await message.answer(text="Спасибо за Ваш отзыв", reply_markup=back_kb())

@dp.callback_query(F.data == "Помочь Фонду")
async def help_for_found(callback: CallbackQuery):
    await callback.message.answer(text="Как вы хотите помочь?", reply_markup=who_are_you_kb())

@dp.callback_query(F.data == "Физ.лицо")
async def help_for_found(callback: CallbackQuery):
    await callback.message.answer(text="Как вы хотите помочь?", reply_markup=fiz_kb())

@dp.callback_query(F.data == "Юр.лицо")
async def help_for_found(callback: CallbackQuery):
    await callback.message.answer(text="Для помощи от юридических лиц, пожалуйста, позвоните на номер - 8 (495) 5426717 или напишите на почту - moldovanova@dalshefond.ru", reply_markup=give_service_kb())
  
@dp.callback_query(F.data == "Получить ссылку для друга")
async def get_link(callback: CallbackQuery):
    await callback.message.answer(text="https://dalshefond.ru/donate/", reply_markup=give_service_kb())

@dp.callback_query(F.data == "Получить помощь Фонда")
async def help(callback: CallbackQuery):
    await callback.message.answer(text="Мы можем предоставить следующую помощь", reply_markup=help_for_found_kb())

@dp.callback_query(F.data == "Пособие для пациентов")
async def giude_pcient(callback: CallbackQuery):
    await callback.message.answer_document(document=posobie_file, reply_markup=back_kb())

@dp.callback_query(F.data == "Лечение по ОМС бесплатно")
async def oms_free(callback: CallbackQuery):
    await callback.message.answer(text="Вся информация по ОМС", reply_markup=oms_kb())
 
@dp.callback_query(F.data == "Как попасть к онкологу")
async def how_to_visit(callback: CallbackQuery):
    await callback.message.answer(text=oms_text, reply_markup=visit_kb())

@dp.callback_query(F.data == "Где пройти обследование")
async def where_clinic(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Location.region)
    await callback.message.answer(text="Напишите название вашего региона")

@dp.message(Location.region)
async def clinic_region(message: Message, state: FSMContext):
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM "clinic" WHERE region = '{message.text}';''')
    region = cursor.fetchone()
    if region is None:
        await message.answer(text="Регион не найдет. Попробуйте перефразировать\nПримеры: Москва, Оренбургская область, республика Башкортостан")
    else:
        await message.answer(text=f'{region[0]} - {region[1]}\n{region[2]}', reply_markup=back_kb())
        await state.clear()

@dp.callback_query(F.data == "Школа пациента")
async def faq(callback: CallbackQuery):
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute('''SELECT question FROM "faq";''')
    await callback.message.answer(text="Часто задаваемые вопросы:\n" + "\n".join([f'{count+1}) ' + i[0] for count, i in enumerate(cursor.fetchall())]))
    await callback.message.answer(text="Нажмите на /question")

@dp.message(Command('question'))
async def answer(message: Message, state: FSMContext):
    await state.set_state(Faq.num)
    await message.answer(text="Введите номер вопроса")
    
@dp.message(Faq.num)
async def answer_question(message: Message, state: FSMContext):
    connection = connect(config_1.POSTGRES_URL)
    cursor = connection.cursor()
    num = message.text
    try:
        cursor.execute(f'''SELECT question, answer FROM "faq" WHERE faq_id = '{num}';''')
        question, answer = cursor.fetchone()
        await message.answer(text=f"Вопрос: {question}\n\nОтвет: {answer}")
        await state.clear()
    except:
        await message.answer(text="Неверный номер вопроса. Попробуйте снова")
    
@dp.callback_query(F.data == 'Поделиться своим опытом')
async def experience(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Напишите немного о своей истории, скоро с вами свяжутся и узнают поподробнее")
    await state.set_state(Story.msg)

@dp.message(Story.msg)
async def experience2(message: Message, state: FSMContext):
    await bot.send_message(chat_id='-4218092750', text=f'Пользователь @{message.from_user.username} хочет поделиться своей историей\nОписание: {message.text}')
    await message.answer(text="Спасибо, скоро с вами свяжутся", reply_markup=back_kb())
    await state.clear()
    