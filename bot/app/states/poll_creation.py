from aiogram.fsm.state import State, StatesGroup


class PollCreation(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()


class PollPassing(StatesGroup):
    waiting_for_poll_id = State()
    answering_questions = State()
