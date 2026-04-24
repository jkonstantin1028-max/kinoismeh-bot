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

# тільки перевірені робочі джерела
rss_sources = [
    "https://rozdil.lviv.ua/rss",     # анекдоти
    "https://karabas.live/rss",       # концерти, культура
    "https://musicukraine.com/rss",   # музика
    "https://kinomania.org.ua/rss"    # кіно
]

# стоп-слова для виключення політики
stop_words = ["політика", "президент", "вибори", "парламент", "уряд", "війна", "закон", "рада"]

posted_titles = set()
emojis = ["😂", "🤣", "🎬", "🎵", "🔥", "😎", "🎭", "📺", "🎤"]

def clean_text(text: str) -> str:
    return re.sub(r'http\S+', '', text).strip()

def is_allowed(title: str) -> bool:
    return not any(word.lower() in title.lower() for word in stop_words)

def publish_entry(entry):
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

        # fallback — тільки текст (сайти не дають картинок)
        bot.send_message(chat_id=CHAT_ID, text=text)
        posted_titles.add(title)
        print("Опубліковано пост:", title)
    except Exception as e:
        print("Помилка при публікації:", e)

def publish_first_news():
    source = random.choice(rss_sources)
    feed = feedparser.parse(source)
    if feed.entries:
        publish_entry(feed.entries[0])
    else:
        print("RSS пустий при старті:", source)

def check_rss():
    sources = random.sample(rss_sources, k=len(rss_sources))
    for source in sources:
        feed = feedparser.parse(source)
        if feed.entries:
            entry = random.choice(feed.entries[:5])
            publish_entry(entry)
        else:
            print("RSS пустий:", source)

publish_first_news()

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


