import os
import time
import schedule
import feedparser
import telebot
import random

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8745612357:AAFQOPh0-WY0yr1VeVhYmUHCeNcPDsDgviA"
CHAT_ID = os.getenv("CHAT_ID") or "-1003912998089"

bot = telebot.TeleBot(BOT_TOKEN)

# список джерел
rss_sources = [
    "https://www.ukrinform.ua/rss",
    "https://tsn.ua/rss",
    "https://espreso.tv/rss",
    "https://detector.media/rss",
    "https://zaxid.net/rss",
    "https://karabas.live/rss",
    "https://musicukraine.com/rss",
    "https://rsshub.app/telegram/channel/ukr_memes",
    "https://rsshub.app/telegram/channel/anekdoty_ua",
    "https://rsshub.app/telegram/channel/kino_fan_ua",
    "https://rsshub.app/telegram/channel/ukrainian_music",
    "https://rsshub.app/telegram/channel/muzika_ua",
    "https://rsshub.app/telegram/channel/xydessa",
    "https://rsshub.app/telegram/channel/fmupl",
    "https://rsshub.app/telegram/channel/kinoman_ua"
]

# пам'ять для унікальних постів
posted_titles = set()

def clean_text(text: str) -> str:
    """Прибирає лінки та залишає тільки чистий текст"""
    import re
    return re.sub(r'http\S+', '', text).strip()

def publish_first_news():
    """При запуску одразу бере першу новину з випадкового джерела"""
    try:
        source = random.choice(rss_sources)
        feed = feedparser.parse(source)
        if feed.entries:
            entry = feed.entries[0]
            title = clean_text(entry.title)
            if title not in posted_titles:
                bot.send_message(chat_id=CHAT_ID, text=f"🎬 {title}")
                posted_titles.add(title)
                print("Опублікована перша новина:", title, "з", source)
            else:
                print("Перша новина вже була:", title)
        else:
            print("RSS пустий:", source)
    except Exception as e:
        print("Помилка при публікації першої новини:", e)

def check_rss():
    """Кожні 10–20 хвилин публікує 2–3 різні новини"""
    try:
        sources = random.sample(rss_sources, k=3)
        for source in sources:
            feed = feedparser.parse(source)
            if feed.entries:
                entry = random.choice(feed.entries[:5])
                title = clean_text(entry.title)
                if title not in posted_titles:
                    bot.send_message(chat_id=CHAT_ID, text=f"📰 {title}")
                    posted_titles.add(title)
                    print("Опубліковано пост:", title, "з", source)
                else:
                    print("Новина вже була:", title)
            else:
                print("RSS пустий:", source)
    except Exception as e:
        print("Помилка при публікації RSS:", e)

# одразу при запуску
publish_first_news()

# випадковий інтервал між 10 і 20 хвилинами
def schedule_random():
    schedule.clear('rss')
    minutes = random.randint(10, 20)
    schedule.every(minutes).minutes.do(check_rss).tag('rss')
    print(f"Новий інтервал: {minutes} хвилин")

schedule_random()
schedule.every().hour.do(schedule_random)

while True:
    schedule.run_pending()
    time.sleep(1)

