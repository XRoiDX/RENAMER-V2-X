# (c) @XRoiDX

from pyrogram import types
from bot.client import Client
from bot.core.db.database import db
from bot.core.file_info import (
    get_media_file_name,
    get_media_file_size,
    get_file_type,
    get_file_attr
)
from bot.core.display import humanbytes
from bot.core.handlers.settings import show_settings


@Client.on_callback_query()
async def cb_handlers(c: Client, cb: "types.CallbackQuery"):
    if cb.data == "showSettings":
        await cb.answer()
        await show_settings(cb.message)
    elif cb.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(cb.from_user.id)
        if not thumbnail:
            await cb.answer("Yᴏᴜ Dɪᴅɴ'ᴛ Sᴇᴛ Aɴʏ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ😐!", show_alert=True)
        else:
            await cb.answer()
            await c.send_photo(cb.message.chat.id, thumbnail, "Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ🖼️",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton("Dᴇʟᴇᴛᴇ Tʜᴜᴍʙɴᴀɪʟ🖼️",
                                                              callback_data="deleteThumbnail")
                               ]]))
    elif cb.data == "deleteThumbnail":
        await db.set_thumbnail(cb.from_user.id, None)
        await cb.answer("Oᴋᴀʏ, I Dᴇʟᴇᴛᴇᴅ Yᴏᴜʀ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ. Nᴏᴡ I Wɪʟʟ Aᴘᴘʟʏ Dᴇꜰᴀᴜʟᴛ Tʜᴜᴍʙɴᴀɪʟ.", show_alert=True)
        await cb.message.delete(True)
    elif cb.data == "setThumbnail":
        await cb.answer()
        await cb.message.edit("Sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴘʜᴏᴛᴏ ᴛᴏ sᴇᴛ ᴛʜᴀᴛ ᴀs ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ.\n\n"
                              "Pʀᴇss /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ ᴘʀᴏᴄᴇss.")
        from_user_thumb: "types.Message" = await c.listen(cb.message.chat.id)
        if not from_user_thumb.photo:
            await cb.message.edit("Pʀᴏᴄᴇss Cᴀɴᴄᴇʟʟᴇᴅ✓")
            return await from_user_thumb.continue_propagation()
        else:
            await db.set_thumbnail(cb.from_user.id, from_user_thumb.photo.file_id)
            await cb.message.edit("Oᴋᴀʏ!\n"
                                  "Nᴏᴡ ɪ ᴡɪʟʟ ᴀᴘᴘʟʏ ᴛʜɪs ᴛʜᴜᴍʙɴᴀɪʟ ᴛᴏ ɴᴇxᴛ ᴜᴘʟᴏᴀᴅs.",
                                  reply_markup=types.InlineKeyboardMarkup(
                                      [[types.InlineKeyboardButton("Oᴘᴇɴ Sᴇᴛᴛɪɴɢs ⚙️",
                                                                   callback_data="showSettings")]]
                                  ))
    elif cb.data == "setCustomCaption":
        await cb.answer()
        await cb.message.edit("ᴏᴋᴀʏ,\n"
                              "sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ.\n\n"
                              "ᴘʀᴇss /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ ᴘʀᴏᴄᴇss.")
        user_input_msg: "types.Message" = await c.listen(cb.message.chat.id)
        if not user_input_msg.text:
            await cb.message.edit("Pʀᴏᴄᴇss Cᴀɴᴄᴇʟʟᴇᴅ✓")
            return await user_input_msg.continue_propagation()
        if user_input_msg.text and user_input_msg.text.startswith("/"):
            await cb.message.edit("Pʀᴏᴄᴇss Cᴀɴᴄᴇʟʟᴇᴅ✓")
            return await user_input_msg.continue_propagation()
        await db.set_caption(cb.from_user.id, user_input_msg.text.markdown)
        await cb.message.edit("Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ Aᴅᴅᴇᴅ Sᴜᴄᴄᴇssꜰᴜʟʟʏ",
                              reply_markup=types.InlineKeyboardMarkup(
                                  [[types.InlineKeyboardButton("Oᴘᴇɴ Sᴇᴛᴛɪɴɢs ⚙️",
                                                               callback_data="showSettings")]]
                              ))
    elif cb.data == "triggerApplyCaption":
        await cb.answer()
        apply_caption = await db.get_apply_caption(cb.from_user.id)
        if not apply_caption:
            await db.set_apply_caption(cb.from_user.id, True)
        else:
            await db.set_apply_caption(cb.from_user.id, False)
        await show_settings(cb.message)
    elif cb.data == "triggerApplyDefaultCaption":
        await db.set_caption(cb.from_user.id, None)
        await cb.answer("Oᴋᴀʏ, Nᴏᴡ I Wɪʟʟ Kᴇᴇᴘ Dᴇꜰᴀᴜʟᴛ Cᴀᴘᴛɪᴏɴ😐", show_alert=True)
        await show_settings(cb.message)
    elif cb.data == "showCaption":
        caption = await db.get_caption(cb.from_user.id)
        if not caption:
            await cb.answer("Yᴏᴜ Dɪᴅɴ'ᴛ Sᴇᴛ Aɴʏ Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ", show_alert=True)
        else:
            await cb.answer()
            await cb.message.edit(
                text=caption,
                parse_mode="Markdown",
                reply_markup=types.InlineKeyboardMarkup([[
                    types.InlineKeyboardButton("Gᴏ ʙᴀᴄᴋ", callback_data="showSettings")
                ]])
            )
    elif cb.data == "triggerUploadMode":
        await cb.answer()
        upload_as_doc = await db.get_upload_as_doc(cb.from_user.id)
        if upload_as_doc:
            await db.set_upload_as_doc(cb.from_user.id, False)
        else:
            await db.set_upload_as_doc(cb.from_user.id, True)
        await show_settings(cb.message)
    elif cb.data == "showFileInfo":
        replied_m = cb.message.reply_to_message
        _file_name = get_media_file_name(replied_m)
        text = f"**File Name:** `{_file_name}`\n\n" \
               f"**File Extension:** `{_file_name.rsplit('.', 1)[-1].upper()}`\n\n" \
               f"**File Type:** `{get_file_type(replied_m).upper()}`\n\n" \
               f"**File Size:** `{humanbytes(get_media_file_size(replied_m))}`\n\n" \
               f"**File MimeType:** `{get_file_attr(replied_m).mime_type}`"
        await cb.message.edit(
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton("Cʟᴏsᴇ Mᴇssᴀɢᴇ", callback_data="closeMessage")]]
            )
        )
    elif cb.data == "closeMessage":
        await cb.message.delete(True)
