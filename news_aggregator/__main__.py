from client import NewsClient


BASE_URL = 'http://localhost:8000'

def main():
    news_client = NewsClient(BASE_URL)

    # Prompt user for commands
    while True:
        command = input("Enter command (login/logout/post/list/delete/exit): ").strip().lower()

        if command == 'login':
            username = input("Enter username: ")
            password = input("Enter password: ")
            response = news_client.login(username, password)
            print(response)

        elif command == 'logout':
            token = input("Enter token: ")
            response = news_client.logout(token)
            print(response)

        elif command == 'post':
            headline = input("Enter headline: ")
            category = input("Enter category: ")
            region = input("Enter region: ")
            details = input("Enter details: ")
            token = input("Enter token: ")
            response = news_client.post_story(token, headline, category, region, details)
            print(response)

        elif command == 'delete':
            story_key = input("Enter story ID: ")
            token = input("Enter token: ")
            response = news_client.delete_story(token, story_key)
            print(response)

        elif command == 'exit':
            print("Exiting program...")
            break

        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
