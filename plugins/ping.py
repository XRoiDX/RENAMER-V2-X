# (c) @XRoiDX

from bot.client import Client
from pyrogram import filters
from pyrogram import types
from bot.core.db.add import add_user_to_database


@Client.on_message(filters.command(["start", "ping"]) & filters.private & ~filters.edited)
async def ping_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await m.reply_text("Hɪ, ɪ ᴀᴍ ʀᴇɴᴀᴍᴇ ʙᴏᴛ🙂!\n\n"
                       "I Cᴀɴ Rᴇɴᴀᴍᴇ Mᴇᴅɪᴀ Wɪᴛʜᴏᴜᴛ Dᴏᴡɴʟᴏᴀᴅɪɴɢ ɪᴛ😍!\n"
                       "Sᴘᴇᴇᴅ Dᴇᴘᴇɴᴅs Oɴ Yᴏᴜʀ Mᴇᴅɪᴀ Dᴄ🚀.\n\n"
                       "Jᴜsᴛ Sᴇɴᴅ Mᴇ Mᴇᴅɪᴀ Aɴᴅ Rᴇᴘʟʏ Tᴏ Iᴛ Wɪᴛʜ  /rename Cᴏᴍᴍᴀɴᴅ.",
                       reply_markup=types.InlineKeyboardMarkup([[
                           types.InlineKeyboardButton("Oᴘᴇɴ Sᴇᴛᴛɪɴɢs ⚙️",
                                                      callback_data="showSettings")
                       ]]))


@Client.on_message(filters.command("help") & filters.private & ~filters.edited)
async def help_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await m.reply_text("I Cᴀɴ Rᴇɴᴀᴍᴇ Mᴇᴅɪᴀ Wɪᴛʜᴏᴜᴛ Dᴏᴡɴʟᴏᴀᴅɪɴɢ ɪᴛ!\n"
                       "Sᴘᴇᴇᴅ Dᴇᴘᴇɴᴅs Oɴ Yᴏᴜʀ Mᴇᴅɪᴀ Dᴄ🚀.\n\n"
                       "Jᴜsᴛ Sᴇɴᴅ Mᴇ Mᴇᴅɪᴀ Aɴᴅ Rᴇᴘʟʏ Tᴏ Iᴛ Wɪᴛʜ  /rename Cᴏᴍᴍᴀɴᴅ.\n\n"
                       "Tᴏ Sᴇᴛ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ 🖼️ Rᴇᴘʟʏ Tᴏ Aɴʏ Iᴍᴀɢᴇ Wɪᴛʜ/set_thumbnail\n\n"
                       "Tᴏ Sᴇᴇ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ 🖼️ Pʀᴇss /show_thumbnail",
                       reply_markup=types.InlineKeyboardMarkup([[
                           types.InlineKeyboardButton("Oᴘᴇɴ Sᴇᴛᴛɪɴɢs ⚙️",
                                                      callback_data="showSettings")
                       ]]))
