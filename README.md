# Message Forwarder Bot

This bot forwards messages from a source chat to a designated channel on Telegram. It ensures that messages are privately sent to the channel without revealing the original sender.

## Features

- Forwards various types of messages: text, photo, document, video, voice, location, poll, contact, audio, animation, sticker, video note.
- Supports replying to messages in the source chat, which will be forwarded to the corresponding forwarded message in the channel.
- Allows users to delete their messages from the channel by replying to them with the `/delete` command.

## Requirements

- Python
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library
- [python-dotenv](https://github.com/theskumar/python-dotenv) library
- A Telegram Bot [Token](https://core.telegram.org/bots/tutorial)
- A Telegram Channel ID

## Setup

1.  Clone this repository to your local machine.

    `git clone https://github.com/B14cs/Forward-Bot`

2.  Install the required dependencies. 

    `pip install -r requirements.txt`

3.  Add the following lines to the .env file, replacing the placeholders with your
    actual values:

    ```plaintext
    API_TOKEN=your_api_token
    CHANNEL_ID=your_channel_id
    ```

    Note:  For security reasons, it's not recommended to store the API token directly in the script. The python-dotenv library is used to load these environment variables from the .env file.

4.  Run the bot script

    `python bot.py`

## Commands

- `/start`: Start the bot and receive instructions.
- `/delete`: Delete your message from the channel by replying to it with this command.

## Usage

1. Add the bot to your Telegram channel as an administrator.
2. Start the bot.
3. Send messages to the bot, and it will automatically forward the message to the specified channel.

- You can edit your messages in the private chat, and they will be automatically edited in the channel.
- Reply to messages with the `/delete` command to remove them from the channel.

## Contributions

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or create a pull request.

