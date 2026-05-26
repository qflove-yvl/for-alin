from enum import Enum


class QuestionType(str, Enum):
    single_choice = "single_choice"
    multi_choice = "multi_choice"
    scale_1_5 = "scale_1_5"
    open_text = "open_text"
