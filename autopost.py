import requests
import feedparser
import schedule
import time
from datetime import datetime
from collections import deque

BOT_TOKEN = "8745612357:AAFQOPh0-WY0yr1VeVhYmUHCeNcPDsDgviA"
CHAT_ID = "@Kinoismeh"

posted_links = deque(maxlen=500)

def log_message(message):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n")

def send_post(text, link=None):
    try:
        if link and link in posted_links:
            log_message(f"Пропущено (дубликат): {link}")
            return
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
        if r.status_code == 200:
            log_message(f"Опубликовано: {text[:50]}... | {link}")
            if link:
                posted_links.append(link)
        else:
            log_message(f"Ошибка публикации: {r.text}")
    except Exception as e:
        log_message(f"Ошибка отправки поста: {e}")

def get_rss_posts(url, prefix="📰 Новина", limit=5):
    try:
        feed = feedparser.parse(url)
        posts = []
        for entry in feed.entries[:limit]:
            posts.append((f"{prefix}: {entry.title}\n{entry.link}", entry.link))
        return posts
    except Exception as e:
        log_message(f"Ошибка RSS {url}: {e}")
        return []

def auto_post():
    sources = [
        {"url": "https://www.pravda.com.ua/rss/", "prefix": "📰 Українська правда"},
        {"url": "https://www.ukrinform.ua/rss", "prefix": "🎭 Укрінформ"},
        {"url": "https://tsn.ua/rss", "prefix": "📺 ТСН"},
        {"url": "https://espreso.tv/rss", "prefix": "📰 Espreso"},
        {"url": "https://detector.media/rss", "prefix": "🎬 Detector Media"},
        {"url": "https://zaxid.net/rss", "prefix": "📰 Zaxid.net"},
        {"url": "https://rsshub.app/telegram/channel/ukrmemes", "prefix": "😂 Мем-канал"},
        {"url": "https://rsshub.app/telegram/channel/kinonews_ua", "prefix": "🎥 Кіноновини"},
        {"url": "https://rsshub.app/telegram/channel/culture_ua", "prefix": "🎭 Культура UA"},
        {"url": "https://rsshub.app/telegram/channel/lifestyle_ua", "prefix": "✨ Лайфстайл UA"},
        {"url": "https://rsshub.app/telegram/channel/humor_ua", "prefix": "🤣 Гумор UA"}
    ]

    now = datetime.now()
    hour = now.hour
    if 0 <= hour < 8:
        log_message("Ночной режим: публикация каждые 30 минут")
    else:
        log_message("Дневной режим: публикация каждые 10 минут")

    for source in sources:
        posts = get_rss_posts(source["url"], source["prefix"], limit=5)
        for text, link in posts:
            send_post(text, link)

# --- Приветственный пост при запуске ---
send_post("🚀 Бот запущен, джерела оновлено!")

# --- Настройка расписания ---
schedule.every(10).minutes.do(auto_post)
schedule.every(30).minutes.do(auto_post)

while True:
    try:
        schedule.run_pending()
        time.sleep(60)
    except Exception as e:
        log_message(f"Критическая ошибка цикла: {e}")
        time.sleep(10)  # пауза и повтор





