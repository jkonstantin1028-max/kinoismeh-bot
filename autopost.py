import os
import time
import requests
import schedule
import feedparser
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8745612357:AAFQOPh0-WY0yr1VeVhYmUHCeNcPDsDgviA"
CHAT_ID = os.getenv("CHAT_ID") or "-1003912998089"

bot = telebot.TeleBot(BOT_TOKEN)

def publish_test():
    try:
        text = "🚀 Проверка публикации: бот работает!"
        bot.send_message(chat_id=CHAT_ID, text=text)
        print("Опубликован тестовый пост:", text)
    except Exception as e:
        print("Ошибка при публикации:", e)

def check_rss():
    try:
        feed = feedparser.parse("https://www.film.ru/rss_news")
        if feed.entries:
            entry = feed.entries[0]
            post_text = f"{entry.title}\n{entry.link}"
            bot.send_message(chat_id=CHAT_ID, text=post_text)
            print("Опубликован пост:", entry.title)
    except Exception as e:
        print("Ошибка при публикации RSS:", e)

# сразу публикуем тестовый пост при старте
publish_test()

# каждые 15 минут проверка RSS
schedule.every(15).minutes.do(check_rss)

while True:
    schedule.run_pending()
    time.sleep(1)

