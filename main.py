from BuoyScanner import BuoyScanner
from dotenv import load_dotenv
from Telegram import Telegram

def main():
    try:
        scanner = BuoyScanner("51205")
        telegram = Telegram()

        telegram.send_message(scanner.getLatestData())
    except ValueError as e:
        print(e)
    except RuntimeError as e:
        print(e)
    finally:
        print("Program finished")

if __name__ == "__main__":
    main()