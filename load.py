import json
from models import Author, Quote
import connect

from mongoengine import DoesNotExist


def get_or_create_author(fullname, born_date=None, born_location=None, description=None):
    try:
        author = Author.objects.get(fullname=fullname)
        created = False
    except DoesNotExist:
        author = Author(
            fullname=fullname,
            born_date=born_date,
            born_location=born_location,
            description=description
        )
        author.save()
        created = True
    return author, created


def load_authors():
    with open(r"D:\GOIT_SoftEng\Module8\HW\authors.json", "r", encoding="utf-8") as file:
        authors_data = json.load(file)
    for author_data in authors_data:
        fullname = author_data.get("fullname")
        born_date = author_data.get("born_date")
        born_location = author_data.get("born_location")
        description = author_data.get("description")
        author, created = get_or_create_author(fullname, born_date, born_location, description)
        print(f"{'Created' if created else 'Found'} author: {fullname}")


def load_quotes():
    with open(r"D:\GOIT_SoftEng\Module8\HW\qoutes.json", "r", encoding="utf-8") as file:
        quotes_data = json.load(file)
    for quote_data in quotes_data:
        quote_text = quote_data.get("quote")
        author_name = quote_data.get("author")
        tags = quote_data.get("tags", [])
        
        # Отримуємо автора або створюємо, якщо його немає
        author, _ = get_or_create_author(author_name)
        # Додаємо цитату
        quote = Quote(quote=quote_text, author=author, tags=tags)
        quote.save()
        print(f"Saved quote: {quote_text} by {author_name}")


if __name__ == "__main__":
    load_authors()
    load_quotes()
