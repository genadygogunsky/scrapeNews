import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def parse_news(url):
    """
    Функция для парсинга новостей с указанного сайта
    
    :param url: URL новостного сайта
    :return: список словарей с новостями
    """
    try:
        # Отправляем GET-запрос
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()  # Проверка успешности запроса

        # Создаем объект BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим блоки новостей (примерный селектор, нужно адаптировать под конкретный сайт)
        news_items = soup.find_all('div', class_='news-item')

        parsed_news = []
        for item in news_items:
            # Извлечение данных о новости
            title = item.find('h2').text.strip()
            link = item.find('a')['href']
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            parsed_news.append({
                'title': title,
                'link': link,
                'date': date
            })

        return parsed_news

    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return []

def save_to_csv(news_list, filename='news.csv'):
    """
    Сохранение спарсенных новостей в CSV-файл
    
    :param news_list: список новостей
    :param filename: имя файла для сохранения
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'link', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for news in news_list:
                writer.writerow(news)
        
        print(f"Новости сохранены в {filename}")

    except IOError as e:
        print(f"Ошибка при сохранении файла: {e}")

def main():
    # URL новостного сайта (замените на реальный)
    NEWS_URL = 'https://example-news-site.com'
    
    # Парсинг новостей
    parsed_news = parse_news(NEWS_URL)
    
    # Сохранение в CSV
    if parsed_news:
        save_to_csv(parsed_news)

if __name__ == "__main__":
    main()
