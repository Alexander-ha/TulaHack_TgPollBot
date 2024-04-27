# -*- coding: utf-8 -*-
import telebot
from django.conf import settings
from telegram import Bot
from bananadmin.questions import QUESTIONS
from .models import Respondent
import regex as re

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, num_threads=5)
my_dict = {key: value for key, value in QUESTIONS}
QUESTIONSS = my_dict["Стартовый Простой Опрос"]
number_of_questions = len(QUESTIONSS)
global start_from_the_latest
start = "/start"
restart = "Попытаться еще раз"

def change_start(checker):
    global start_from_the_latest
    start_from_the_latest = checker
    


@bot.message_handler(commands = ['start'])
def start(message):
  bot.send_message(message.chat.id,
   'Приветствую! Я - универсальный Telegram-бот для создания и прохождения опросов\n\n Список комманд:\n\n -/help - помощь в прохождении опросов\n\n  -/make_choice - выбрать опрос')

@bot.message_handler(commands = ['help'])
def help(message):
  bot.send_message(message.chat.id, 'Список комманд:\n\n -/help - помощь в прохождении опросов\n\n  -/make_choice - выбрать опрос')


@bot.message_handler(commands = ['make_choice'])
def make_choice(message):
  id=message.from_user.id
  names = [QUESTIONS [i][0] for i in range(0, len(QUESTIONS))]
  names = "\n\n".join(names)
  bot.send_message(message.chat.id, 'Можете выбрать следующие опросы:\n'+names)

  def process_choice(message):
    user_choice = message.text
    QUESTIONSS = my_dict[user_choice]
    bot.send_message(message.chat.id, 'Отличный выбор! Желаете приступить к прохождению нового опроса или закончить прохождение предыдущих?')
    bot.register_next_step_handler(message, process_poll)

  def process_poll(message):
    msg = message.text
    regex_new = re.compile(r'\bнов[аыои]?[йем]?\b', re.IGNORECASE)
    regex_previous = re.compile(r'\bпредыдущ[ийаяое]?\b', re.IGNORECASE)
    if re.match(regex_new, msg):
        checker = False
        change_start(checker)
        print('Пользователь выбрал новый опрос')
        handler(message)
    if re.match(regex_previous, msg):
        checker = True
        change_start(checker)
        print('Пользователь выбрал старый опрос')
        handler(message)
    if re.match(regex_previous, msg) == False:
        bot.send_message(message.chat.id, 'Не могу вас понять, попробуйте еще раз!')
  
  bot.register_next_step_handler(message, process_choice)



def markup_choices(choices):
    if not choices:
        return telebot.types.ReplyKeyboardRemove(selective=False)

    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    for choice in choices:
        markup.add(telebot.types.KeyboardButton(choice))

    return markup


@bot.message_handler()
def handler(message):
    registrant, _ = Respondent.objects.get_or_create(        
        id=message.from_user.id,
        defaults={
            "first_name": message.from_user.first_name or "",
            "last_name": message.from_user.last_name or "",
            "username": message.from_user.username or "",
        }
    )

    if start_from_the_latest is True:       
        response = registrant.responses.filter(completed=False).last()
    if start_from_the_latest is False:
        response = registrant.responses.create()
    if not response or message.text in [start, restart]:
        response = registrant.responses.create()
    if number_of_questions >= response.step >= 1:
        prev_question = QUESTIONSS[response.step - 1]["text"]
        response.parts[prev_question] = message.text
        response.save(update_fields=["parts"])
    if response.step >= number_of_questions:
        response.completed = True
        response.save(update_fields=["completed"])
        bot.send_message(
            registrant.id,
            "Готово! Спасибо за прохождение опроса",
            reply_markup=markup_choices([restart])
        )
        return

    question = QUESTIONSS[response.step]
    text = question["text"]
    choices = question.get("choices") or []

    bot.send_message(registrant.id, text, reply_markup=markup_choices(choices))

    response.step += 1
    response.save(update_fields=["step"])
