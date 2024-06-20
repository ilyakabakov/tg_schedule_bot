from aiogram import types, Router, Bot
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter

""" Censoring filter """
user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    """ This function is the first part of the two-factor authentication analog,
    catches the Admin command in the admin chat and identifies the rank of the user
    in this chat, keeping the ID in the list that is used in the custom IsAdmin filter. """
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == 'creator' or member.status == 'administrator'
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
