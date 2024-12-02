from models import Quote, Author
import connect


def search_by_author(author_name):
    author = Author.objects(fullname=author_name).first()
    if not author:
        return []
    quotes = Quote.objects(author=author.id)
    return [quote.quote for quote in quotes]


def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    return [quote.quote for quote in quotes]


def search_by_tags(tags):
    tags_list = tags.split(",")
    quotes = Quote.objects(tags__in=tags_list)
    return [quote.quote for quote in quotes]

def main():
    while True:
        command = input("Enter your command: ").strip()
        if command.lower() == "exit":
            print("Exiting the program.")
            break
        try:
            cmd, value = command.split(":", 1)
            if cmd == "name":
                results = search_by_author(value.strip())
            elif cmd == "tag":
                results = search_by_tag(value.strip())
            elif cmd == "tags":
                results = search_by_tags(value.strip())
            else:
                print("Invalid command. Try again.")
                continue
            print("\n".join(results) if results else "No quotes found.")
        except ValueError:
            print("Invalid input format. Use command:value.")

if __name__ == "__main__":
    main()
