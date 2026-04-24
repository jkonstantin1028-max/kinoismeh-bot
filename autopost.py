import os
import time
import schedule
import feedparser
import telebot
import random
import re

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8745612357:AAFQOPh0-WY0yr1VeVhYmUHCeNcPDsDgviA"
CHAT_ID = os.getenv("CHAT_ID") or "-1003912998089"

bot = telebot.TeleBot(BOT_TOKEN)

# тільки розважальні джерела
rss_sources = [
    "https://rsshub.app/telegram/channel/ukr_memes",
    "https://rsshub.app/telegram/channel/anekdoty_ua",
    "https://rsshub.app/telegram/channel/kino_fan_ua",
    "https://rsshub.app/telegram/channel/ukrainian_music",
    "https://rsshub.app/telegram/channel/muzika_ua",
    "https://rsshub.app/telegram/channel/xydessa",
    "https://rsshub.app/telegram/channel/fmupl",
    "https://rsshub.app/telegram/channel/kinoman_ua",
    "https://karabas.live/rss",
    "https://musicukraine.com/rss",
    "https://anekdoty.com.ua/rss",
    "https://rozdil.lviv.ua/rss"
]

# стоп-слова для виключення політики
stop_words = ["політика", "президент", "вибори", "парламент", "уряд", "війна", "закон", "рада"]

# пам'ять для унікальних постів
posted_titles = set()

# емодзі для різноманітності
emojis = ["😂", "🤣", "🎬", "🎵", "🔥", "😎", "🎭", "📺", "🎤"]

def clean_text(text: str) -> str:
    """Прибирає лінки та залишає тільки чистий текст"""
    return re.sub(r'http\S+', '', text).strip()

def is_allowed(title: str) -> bool:
    """Перевіряє чи новина не політична"""
    return not any(word.lower() in title.lower() for word in stop_words)

def publish_entry(entry):
    """Публікує новину з картинкою якщо є"""
    try:
        title = clean_text(entry.title)
        if not is_allowed(title):
            print("Пропущено політичну новину:", title)
            return
        if title in posted_titles:
            print("Новина вже була:", title)
            return

        emoji = random.choice(emojis)
        text = f"{emoji} {title}"

        # якщо є картинка
        if hasattr(entry, "media_content") and entry.media_content:
            img_url = entry.media_content[0].get("url")
            if img_url:
                bot.send_photo(chat_id=CHAT_ID, photo=img_url, caption=text)
                print("Опубліковано пост з картинкою:", title)
        else:
            bot.send_message(chat_id=CHAT_ID, text=text)
            print("Опубліковано пост:", title)

        posted_titles.add(title)
    except Exception as e:
        print("Помилка при публікації:", e)

def publish_first_news():
    """При запуску одразу бере першу новину"""
    source = random.choice(rss_sources)
    feed = feedparser.parse(source)
    if feed.entries:
        publish_entry(feed.entries[0])

def check_rss():
    """Кожні 10–20 хвилин публікує 2–3 різні новини"""
    sources = random.sample(rss_sources, k=3)
    for source in sources:
        feed = feedparser.parse(source)
        if feed.entries:
            entry = random.choice(feed.entries[:5])
            publish_entry(entry)

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

