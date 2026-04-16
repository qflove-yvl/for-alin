from aiogram.fsm.state import State, StatesGroup


class PollCreation(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_add_question = State()
    waiting_for_question_text = State()
    waiting_for_question_type = State()
    waiting_for_question_options = State()


class PollPassing(StatesGroup):
    waiting_for_poll_id = State()
    answering_questions = State()
