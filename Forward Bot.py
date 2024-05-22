import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)

# Load environment variables from a .env file
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Configure logging to output detailed information
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# Dictionaries to store message IDs for tracking
message_id_map = {}


# Main function to process and forward messages
async def process_message(update: Update, context: CallbackContext):
    # Get the incoming message or edited message
    message = update.message or update.edited_message
    if not message:
        return

    # Handle edited messages by replacing the existing ones
    if update.edited_message:
        await _replace_message(context, message)
    # Handle new messages
    elif any(
        [
            message.text,
            message.photo,
            message.document,
            message.video,
            message.voice,
            message.location,
            message.poll,
            message.contact,
            message.audio,
            message.animation,
            message.sticker,
            message.video_note,
        ]
    ):
        if message.reply_to_message:
            # Forward replies to the corresponding forwarded message in the channel
            original_message_id = message.reply_to_message.message_id
            if original_message_id in message_id_map:
                await _forward_reply_message(message, context, original_message_id)
        else:
            # Forward new messages
            await _forward_new_message(message, context)
    else:
        # Inform the user if the message type is not supported
        await message.reply_text("Sorry, I cannot handle this type of message.")

    logging.info("message_id_map: %s", message_id_map)


# Function to replace an existing message with the updated one
async def _replace_message(context, message):
    original_message_id = message.message_id
    # Delete the old message if it exists in the tracking map
    if original_message_id in message_id_map:
        await context.bot.deleteMessage(
            chat_id=CHANNEL_ID, message_id=message_id_map[original_message_id]
        )
        del message_id_map[original_message_id]

    # Copy the new message to the channel
    if message.caption:
        new_message = await message.copy(chat_id=CHANNEL_ID, caption=message.caption)
    elif message.text:
        new_message = await message.copy(chat_id=CHANNEL_ID)

    # Update the message ID maps with the new message IDs
    message_id_map[message.message_id] = new_message.message_id


# Function to forward new messages
async def _forward_new_message(message, context):
    new_message = await message.copy(chat_id=CHANNEL_ID)

    # Update the message ID maps with the new message IDs
    message_id_map[message.message_id] = new_message.message_id


# Function to forward replies to the corresponding forwarded message in the channel
async def _forward_reply_message(message, context, original_message_id):
    new_message = await message.copy(
        chat_id=CHANNEL_ID,
        reply_to_message_id=message_id_map[original_message_id],
    )

    # Update the message ID maps with the new message IDs
    message_id_map[message.message_id] = new_message.message_id


# Handler for the /start command
async def start_command(update: Update, context: CallbackContext):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I will ensure that your messages are privately sent to the channel.\n\nReply to the message you want to delete with /delete to delete your message from the channel.",
    )


# Handler for the /delete command
async def delete_command(update: Update, context: CallbackContext):
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message you want to delete.")
        return

    original_message_id = update.message.reply_to_message.message_id
    if original_message_id in message_id_map:
        await context.bot.deleteMessage(
            chat_id=CHANNEL_ID, message_id=message_id_map[original_message_id]
        )
        del message_id_map[original_message_id]
    else:
        await update.message.reply_text("Sorry, I couldn't find the message to delete.")


if __name__ == "__main__":
    # Initialize the Application with JobQueue
    application = ApplicationBuilder().token(API_TOKEN).build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("delete", delete_command))
    application.add_handler(MessageHandler(filters.ALL, process_message))

    # Start the bot
    application.run_polling()
