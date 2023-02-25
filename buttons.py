from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Define main menu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="General Information"),
            KeyboardButton(text="Questionnaire")
        ],
    ],
    resize_keyboard=True
)

# Define lab menu
lab_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3")
        ],
    ],
    resize_keyboard=True
)

# Define subject menu
subject_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Informatics"),
            KeyboardButton(text="Mathematics"),
        ],
    ],
    resize_keyboard=True
)
