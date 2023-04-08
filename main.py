import os
import ptbot
from dotenv import load_dotenv
from pytimeparse import parse


def render_progressbar(
        total,
        iteration,
        prefix='',
        suffix='',
        length=30,
        fill='█',
        zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, chat_id, message_id, user_text):
    total_bar = int(user_text[:-1])
    bot.update_message(
        chat_id,
        message_id,
        "Осталось {} секунд\n".format(secs_left) + render_progressbar(
                                                        total_bar,
                                                        total_bar-secs_left
                                                    )
    )


def wait(chat_id, user_text):
    if user_text == '/start':
        bot.send_message(chat_id, "Привет) Я умею запускать таймер")
    else:
        message_id = bot.send_message(chat_id, "Зпускаю таймер...")
        bot.create_countdown(
            parse(user_text),
            notify_progress,
            chat_id=chat_id,
            message_id=message_id,
            user_text=user_text
        )
        bot.create_timer(parse(user_text), choose, chat_id=chat_id)


def choose(chat_id):
    bot.send_message(chat_id, 'Время вышло')


def main():
    bot.reply_on_message(wait)
    bot.run_bot()


if __name__ == '__main__':
    load_dotenv('secret.env')
    tg_token = os.environ['TELEGRAM_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    bot = ptbot.Bot(tg_token)
    main()
