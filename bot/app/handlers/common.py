from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.services.api_client import APIClient
from app.states.poll_creation import PollCreation, PollPassing

router = Router()
api = APIClient()


@router.message(Command("start"))
async def start(message: Message):
    data = await api.create_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Привет! Твой user_id в системе: {data['id']}")


@router.message(Command("create_poll"))
async def create_poll_start(message: Message, state: FSMContext):
    await state.set_state(PollCreation.waiting_for_title)
    await message.answer("Введите название опроса")


@router.message(PollCreation.waiting_for_title)
async def create_poll_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(PollCreation.waiting_for_description)
    await message.answer("Введите описание опроса")


@router.message(PollCreation.waiting_for_description)
async def create_poll_description(message: Message, state: FSMContext):
    data = await state.get_data()
    user = await api.create_user(message.from_user.id, message.from_user.username)
    poll = await api.create_poll(owner_id=user["id"], title=data["title"], description=message.text)
    await state.clear()
    await message.answer(f"Опрос создан! ID: {poll['id']}")


@router.message(Command("my_polls"))
async def my_polls(message: Message):
    user = await api.create_user(message.from_user.id, message.from_user.username)
    polls = await api.user_polls(user["id"])
    if not polls:
        await message.answer("У вас пока нет опросов.")
        return
    text = "\n".join([f"#{p['id']} — {p['title']}" for p in polls])
    await message.answer(f"Ваши опросы:\n{text}")


@router.message(Command("take_poll"))
async def take_poll(message: Message, state: FSMContext):
    await state.set_state(PollPassing.waiting_for_poll_id)
    await message.answer("Введите ID опроса")


@router.message(PollPassing.waiting_for_poll_id)
async def take_poll_id(message: Message, state: FSMContext):
    poll_id = int(message.text)
    questions = await api.poll_questions(poll_id)
    if not questions:
        await message.answer("У опроса нет вопросов.")
        await state.clear()
        return

    await state.update_data(poll_id=poll_id, questions=questions, index=0)
    await state.set_state(PollPassing.answering_questions)
    await message.answer(questions[0]["text"])


@router.message(PollPassing.answering_questions)
async def answer_question(message: Message, state: FSMContext):
    data = await state.get_data()
    questions = data["questions"]
    index = data["index"]
    current = questions[index]

    user = await api.create_user(message.from_user.id, message.from_user.username)
    response = await api.submit_answer(user["id"], current["id"], message.text)
    if response.status_code not in (200, 201):
        await message.answer(f"Ошибка сохранения ответа: {response.text}")
        await state.clear()
        return

    index += 1
    if index >= len(questions):
        await message.answer("Спасибо! Опрос завершён.")
        await state.clear()
        return

    await state.update_data(index=index)
    await message.answer(questions[index]["text"])


@router.message(Command("results"))
async def results(message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Использование: /results <poll_id>")
        return
    poll_id = int(args[1])
    payload = await api.poll_results(poll_id)
    await message.answer(
        f"Участников: {payload['participants']}\n"
        f"Распределения: {payload['distributions']}\n"
        f"Средние шкал: {payload['scale_means']}"
    )


@router.message(F.text)
async def fallback(message: Message):
    await message.answer("Используйте команды: /start /create_poll /my_polls /take_poll /results")
