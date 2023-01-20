    # tg_shedule_bot.
    # This project for my wife, she is a psychologist.
In project I used Python 3.10, aoigram framework, json, SQLite3
Specification for Bot:
    - Write new "Submitting application for a consultation" in database
    - Have a FAQ section
    - Write new questions from FAQ section
    - Read information from database
    - Read "bio" and "prices" from .txt(Don't ask 😅 it's wife's request)
    - Show biography info
     
Now all requests work.
    - Added new section with events information

For the bot to work, you need:
- Install packages:
    - aiogram (When I wrote, I used the version v2.24)
    - python-dotenv( the same, used v0.21.0)
- Put it in the root directory:
    - .env(this file should contain telegram TOKEN and ID_NUM(Telegram user id the bot owner))
    - The SQL database will be created at the first start
    - bio.txt
    - price.txt
    - cens.txt(a file with obscene words, when bot starts it will be converted in .json)
    - master.json(this file needed for work FAQ section. Contain questions dict(in future i want rename this file))


# In future, i want todo google calendar integration, even though my wife is against it 😅
 
