import json

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.main import main_keyboard, question_type_keyboard, yes_no_keyboard
from app.services.api_client import APIClient
from app.states.poll_creation import PollCreation, PollPassing

router = Router()
api = APIClient()

QUESTION_TYPES = {"single_choice", "multi_choice", "scale_1_5", "open_text"}

HELP_TEXT = (
    "Доступные команды:\n"
    "/start — регистрация и главное меню\n"
    "/help — показать это сообщение\n"
    "/create_poll — создать опрос (с добавлением вопросов в чате)\n"
    "/my_polls — мои опросы\n"
    "/take_poll — пройти опрос по ID\n"
    "/results <poll_id> — аналитика по опросу"
)


@router.message(Command("start"))
async def start(message: Message):
    data = await api.create_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"Привет! Ты зарегистрирован. user_id: {data['id']}\n\n{HELP_TEXT}",
        reply_markup=main_keyboard,
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(HELP_TEXT, reply_markup=main_keyboard)


@router.message(Command("create_poll"))
async def create_poll_start(message: Message, state: FSMContext):
    await state.clear()
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

    await state.update_data(poll_id=poll["id"], question_order=1)
    await state.set_state(PollCreation.waiting_for_add_question)
    await message.answer(
        f"Опрос создан! ID: {poll['id']}\nДобавить первый вопрос?",
        reply_markup=yes_no_keyboard,
    )


@router.message(PollCreation.waiting_for_add_question)
async def poll_add_question_decision(message: Message, state: FSMContext):
    answer = (message.text or "").strip().lower()
    if answer in {"да", "yes", "y"}:
        await state.set_state(PollCreation.waiting_for_question_text)
        await message.answer("Введите текст вопроса")
        return

    if answer in {"нет", "no", "n"}:
        await state.clear()
        await message.answer("Готово. Опрос сохранён.", reply_markup=main_keyboard)
        return

    await message.answer("Пожалуйста, выберите: Да или Нет.", reply_markup=yes_no_keyboard)


@router.message(PollCreation.waiting_for_question_text)
async def poll_question_text(message: Message, state: FSMContext):
    await state.update_data(question_text=message.text)
    await state.set_state(PollCreation.waiting_for_question_type)
    await message.answer(
        "Выберите тип вопроса:\n"
        "- single_choice\n- multi_choice\n- scale_1_5\n- open_text",
        reply_markup=question_type_keyboard,
    )


@router.message(PollCreation.waiting_for_question_type)
async def poll_question_type(message: Message, state: FSMContext):
    q_type = (message.text or "").strip()
    if q_type not in QUESTION_TYPES:
        await message.answer("Неверный тип. Выберите кнопку из меню типа вопроса.", reply_markup=question_type_keyboard)
        return

    await state.update_data(question_type=q_type)

    if q_type in {"single_choice", "multi_choice"}:
        await state.set_state(PollCreation.waiting_for_question_options)
        await message.answer("Введите варианты через запятую. Пример: красный, синий, зелёный")
        return

    await create_question_and_ask_more(message, state, options_json=None)


@router.message(PollCreation.waiting_for_question_options)
async def poll_question_options(message: Message, state: FSMContext):
    options = [item.strip() for item in (message.text or "").split(",") if item.strip()]
    if len(options) < 2:
        await message.answer("Нужно минимум 2 варианта. Введите через запятую.")
        return

    await create_question_and_ask_more(message, state, options_json=json.dumps(options, ensure_ascii=False))


async def create_question_and_ask_more(message: Message, state: FSMContext, options_json: str | None) -> None:
    data = await state.get_data()
    poll_id = data["poll_id"]
    q_text = data["question_text"]
    q_type = data["question_type"]
    q_order = data.get("question_order", 1)

    question = await api.create_question(
        poll_id=poll_id,
        text=q_text,
        q_type=q_type,
        order=q_order,
        options_json=options_json,
    )

    await state.update_data(question_order=q_order + 1)
    await state.set_state(PollCreation.waiting_for_add_question)

    await message.answer(
        f"Вопрос добавлен (ID: {question['id']}). Добавить ещё вопрос?",
        reply_markup=yes_no_keyboard,
    )


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
    if not message.text.isdigit():
        await message.answer("ID должен быть числом. Попробуйте снова.")
        return

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
        await message.answer("Спасибо! Опрос завершён.", reply_markup=main_keyboard)
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
    await message.answer(
        "Не понял команду. Нажмите /help или используйте кнопки меню.",
        reply_markup=main_keyboard,
    )
