# tg_shedule_bot.
# This project for my wife, she is a psychologist.
In project I used Python 3.10, aoigram framework, json, SQLite3

Project in Telegram App:
@kabakova_psy_bot

- Specifications for Bot:
    - Write new "Submitting application for a consultation" in database
    - Have a FAQ section 
    - Write new questions from FAQ section
    - Read information from database
    - Show information from database to admin
    - Read "bio", "prices" and FAQ part from .json
    - Show biography info to client
    - Delete messages with obscene words in chat, where bot is admin and in private messages.  
     
Now all requests work.
    - Added new section with events information

How to install:
- You needed Installed packages:
    - python 3.10
    - aiogram (version v2.24)
    - python-dotenv(v0.21.0)
- Put it in the root directory:
    - .env(this file should contain telegram TOKEN and ID_NUM(Telegram user id the bot owner))
- The SQL database will be created at the first bot started
- Put it in the database folder:
    - cens.txt(a file with obscene words, when bot starts it will be converted in .json)
    - master.json(Contain questions dict, bio and prices)
- Json file structure: {"key": {"queries": [value]},...}


# In future, i want todo google calendar integration, even though my wife is against it 😅
 
