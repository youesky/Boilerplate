from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import random 

#user random module to select items randomly

api_id = "API_ID"
api_hash = "API_HASH"
bot_token = "BOT_TOKEN"

app = Client("neural_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

#ReplyKeyboardMarkup
keyboard = ReplyKeyboardMarkup([
[KeyboardButton(text="Send Photo"), KeyboardButton(text="Send Poll")],
[KeyboardButton(text="Random Emoji"), KeyboardButton(text="Change Keyboard")]
], resize_keyboard=False)
#pass resize_keyboard = True if you wanna make it smaller

#InlineKeyboardMarkup
inline_keyboard = InlineKeyboardMarkup([
[InlineKeyboardButton(text="Send Photo", callback_data="send_photo"), InlineKeyboardButton(text="Send Poll", callback_data="send_poll")],
[InlineKeyboardButton(text="Random Emoji", callback_data="random_emoji"), InlineKeyboardButton(text="Change Keyboard", callback_data="change_keyboard")]
])
#Here you would probably notice that we have passed callback_data parameter, this is because we use this callback_data to handle when specific button is clicked

#bear in mind you can make Keyboards dynamically.

@app.on_message(filters.command("start"))
async def start(_, message):
    #sending keyboard with reply_markup parameter
    await message.reply("Welcome to My Telegram bot.\nChoose Keyboard:", reply_markup=keyboard)
    
"""once we've keyboard to user, now we have to respond when user clicks one of the buttons, so to do this we use on_message() handler"""

"""To receive only text use, we user filters.text parameter, feel free to use other parameters: filters.photo, filters.document etc."""

emoji = ["😁", "😎", "😉", "🤗","😊"]

@app.on_message(filters.text)
async def handle_all_msg(_, message):
 """from message object we can extract text as: message.text, Great, Lets continue."""
 if message.text == "Send Photo":
  photo_id = random.randint(300, 800)
  photo_url = f"https://picsum.photos/{photo_id}"
  #we are sending photo from a website, once we have photo, we can send it to user
  await app.send_photo(message.chat.id, photo_url, caption="This is my caption!")
 elif message.text == "Random Emoji":
  emoji_to_be_sent = random.choice(emoji)
  await app.send_message(message.chat.id, emoji_to_be_sent)
 elif message.text == "Send Poll":
  await app.send_poll(message.chat.id, question="What do you like?", options=["Mango","Apple","Both"]) 
 elif message.text == "Change Keyboard":
  #Now lets remove ReplyKeyboardMarkup and send InlineKeyboardMarkup 
  await message.reply("Keyboard has been changed!", reply_markup=ReplyKeyboardRemove())
  await message.reply("Choose options:", reply_markup=inline_keyboard)

""""
So far, we have handled all our buttons events, Now lets handle InlineKeyboardButtons using on_callback_query() handler
"""
@app.on_callback_query()
async def answer_callback(_, callback):
 print(callback)
 await app.answer_callback_query(callback.id, "You have clicked InlineKeyboardButton!", show_alert=True)
 if callback.data == "change_keyboard":
  await app.delete_messages(callback.from_user.id, callback.message.id)
  await app.send_message(callback.from_user.id, "Choose Keyboard", reply_markup=keyboard)
 #see what callback contains, we will show you how to handle this in the next tutorial

print("Bot has been started!")
app.run()
