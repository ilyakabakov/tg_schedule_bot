# Bot for recording clients to a specialist.

- The Bot may to do:
    - Write new application for a consultation in database
    - Have a FAQ section 
    - Write new question in db from client in FAQ section
    - Rewrite info about upcoming event from bot's admin
    - Show information from database to admin
    - Read text content from json
    - Show events info from db
    - Form to sign up for an event
    - Delete messages with obscene words in chat, where bot is admin and in private messages.
   
#
In project I used: 
- Python 3.10;
- Aoigram framework ver. 2.25.1;
- json;
- Redis;
- SQL Alchemy;
- aioSQLite;
- SQLite3 db.

In this bot uses Redis like a temporary storage.
Bot's token and Redis password are contained in the .env file.
And all text content reading from json file, except for the poster of the upcoming event.
# 
The project is deployed and running in the Telegram App:
@kabakova_psy_bot


 
