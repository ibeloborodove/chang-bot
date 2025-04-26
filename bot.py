from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

TOKEN = "7731694868:AAGZvbAApn7hG7Xl-NnR1YMIfinKCTgtjvo"
ADMIN_ID = @ibeloborodove  # Твой Telegram ID

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Память для хранения всех сообщений
messages = []

# Состояния
class Form(StatesGroup):
    anonymity = State()
    restaurant = State()
    department = State()
    problem = State()

# Старт команды
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Анонимно", "Не анонимно")
    await message.answer("Привет! Хотите оставить сообщение анонимно?", reply_markup=markup)
    await Form.anonymity.set()

# Выбор анонимности
@dp.message_handler(state=Form.anonymity)
async def process_anonymity(message: types.Message, state: FSMContext):
    await state.update_data(anonymity=message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("БК", "Невский", "Некрасова")
    await message.answer("Выберите ресторан:", reply_markup=markup)
    await Form.restaurant.set()

# Выбор ресторана
@dp.message_handler(state=Form.restaurant)
async def process_restaurant(message: types.Message, state: FSMContext):
    await state.update_data(restaurant=message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Кухня", "Бар", "Зал")
    await message.answer("Выберите подразделение:", reply_markup=markup)
    await Form.department.set()

# Выбор подразделения
@dp.message_handler(state=Form.department)
async def process_department(message: types.Message, state: FSMContext):
    await state.update_data(department=message.text)
    await message.answer("Теперь опишите, что вас беспокоит:", reply_markup=types.ReplyKeyboardRemove())
    await Form.problem.set()

# Приём основного сообщения
@dp.message_handler(state=Form.problem)
async def process_problem(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    anonymity = user_data.get('anonymity')
    restaurant = user_data.get('restaurant')
    department = user_data.get('department')
    problem_text = message.text

    if anonymity == "Не анонимно":
        user_name = message.from_user.full_name
        user_id = message.from_user.id
    else:
        user_name = "-"
        user_id = "-"

    # Сохраняем всё вместе
    record = f"👤 Анонимно: {anonymity}\n🏢 Ресторан: {restaurant}\n🔧 Подразделение: {department}\n📝 Имя: {user_name}\n🆔 Telegram ID: {user_id}\n💬 Сообщение: {problem_text}\n{'-'*30}"
    messages.append(record)

    await message.answer("Спасибо! Ваше сообщение записано ✅")
    await state.finish()

# Команда для получения всех сообщений
@dp.message_handler(commands=['отчёт'])
async def report(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        if messages:
            report_text = "\n\n".join(messages)
            await message.answer(f"Все накопленные сообщения:\n\n{report_text}")
        else:
            await message.answer("Пока нет записей.")
    else:
        await message.answer("У вас нет доступа к этой команде.")

# Команда для очистки сообщений (если нужно)
@dp.message_handler(commands=['очистить'])
async def clear_messages(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        messages.clear()
        await message.answer("Все сообщения очищены.")
    else:
        await message.answer("У вас нет доступа к этой команде.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
