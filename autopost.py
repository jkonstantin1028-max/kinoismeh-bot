import feedparser
import time
import requests

BOT_TOKEN = "ВАШ_ТОКЕН"
CHAT_ID = "@Kinoismeh"

# Украинские развлекательные источники
rss_sources = [
    "https://www.ukrinform.ua/rss",
    "https://tsn.ua/rss",
    "https://espreso.tv/rss",
    "https://detector.media/rss",
    "https://zaxid.net/rss",
    "https://anekdotua.com/rss",
    "https://karabas.live/rss",
    "https://musicukraine.com/rss"
]

# Список для отслеживания уже опубликованных постов
posted_links = set()

# Слова, которые нужно исключить (чтобы убрать политику)
ban_words = ["политика", "війна", "правительство", "влада"]

def is_allowed(text):
    return not any(word in text.lower() for word in ban_words)

def format_post(entry):
    # Берём только заголовок и описание, без ссылки
    return f"{entry.title}\n\n{entry.summary}"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def check_feeds():
    for source in rss_sources:
        feed = feedparser.parse(source)
        # Ограничиваем количество постов за раз (например, 3)
        for entry in feed.entries[:3]:
            if entry.link in posted_links:
                continue
            text = format_post(entry)
            if is_allowed(text):
                send_message(text)
                posted_links.add(entry.link)
                # Ограничиваем память до 500 ссылок
                if len(posted_links) > 500:
                    posted_links.pop()

if __name__ == "__main__":
    while True:
        check_feeds()
        time.sleep(600)  # проверка каждые 10 минут
