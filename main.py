import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from buttons import main_menu, lab_menu, subject_menu
import os
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)
load_dotenv()
users = []
admin_chat_id = os.getenv("ADMIN_ID")
# Initialize bot and dispatcher
bot = Bot(token=os.getenv("BOT_KEY_API"))
dp = Dispatcher(bot, storage=MemoryStorage())

# Define states
class QuestionnaireStates(StatesGroup):
    subject = State()
    task = State()


# Define commands
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in users:
        users.append(user_id)
    await message.answer("Hello, I'm a mythi help bot.", reply_markup=main_menu)


# Handle General Information button
@dp.message_handler(text="General Information")
async def general_information(message: types.Message):
    await message.answer("Hello, I'm a mythi help bot.", reply_markup=main_menu)


# Handle Questionnaire button
@dp.message_handler(text="Questionnaire")
async def questionnaire(message: types.Message):
    await message.answer("What item do you need?", reply_markup=subject_menu)

    # Set state to subject
    await QuestionnaireStates.subject.set()


# Handle subject selection
@dp.message_handler(state=QuestionnaireStates.subject)
async def handle_subject(message: types.Message, state: FSMContext):
    # Save subject selection to state
    await state.update_data(subject=message.text)

    if message.text == "Informatics":
        await message.answer("What kind of laboratory work?", reply_markup=lab_menu)

        # Set state to task
        await QuestionnaireStates.task.set()

    elif message.text == "Mathematics":
        await message.answer("What kind of help do you need?")
        # Set state to task
        await QuestionnaireStates.task.set()


# Handle task selection
@dp.message_handler(state=QuestionnaireStates.task)
async def handle_task(message: types.Message, state: FSMContext):
    # Save task selection to state
    await state.update_data(task=message.text)

    # Get subject and task from state
    data = await state.get_data()

    # Send answers to admin
    await bot.send_message(admin_chat_id, f"Subject: {data['subject']}\nTask: {data['task']}\nId: {message.from_user.id}",
                           parse_mode=ParseMode.HTML)

    # Reset state and send main menu
    await state.reset_state()
    await message.answer("Thank you for completing the questionnaire!", reply_markup=main_menu)


# Обработчик команды /all
@dp.message_handler(commands=['all'])
async def cmd_all(message: types.Message):
    # Проверяем, является ли отправитель сообщения админом
    is_admin = message.from_user.id == int(admin_chat_id)
    if not is_admin:
        await message.answer("Вы не являетесь админом!")
        return
    # Отправляем сообщение всем пользователям
    for user_id in users:
        await bot.send_message(chat_id=user_id, text=message.text[4:])
print("here")

@dp.message_handler(commands=['write'])
async def cmd_write(message: types.Message):
    # Получаем текст сообщения
    msg = message.text[6:]
    arr_msg = msg.split(" ")
    print(arr_msg)
    try:
        await bot.send_message(arr_msg[1], arr_msg[2], parse_mode=ParseMode.HTML)
        await message.reply("Сообщение успешно отправлено!")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

# Start polling
if __name__ == '__main__':
    logging.info("Starting bot polling")
    executor.start_polling(dp)
