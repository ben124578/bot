
import os
import stoat
import commands

from flask import Flask

# Flask keep-alive server
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"


# Stoat Bot Setup
class MyBot(stoat.Client):

    async def on_ready(self, event, /):
        print(f"Logged in as {self.me}")

    async def on_message(self, message, /):
        # Ignore bot messages
        if message.author_id == self.me.id:
            return

        await commands.handle_message(self, message)


# Start the bot
def start_bot():
    token = os.environ.get("BOT_KEY")

    if not token:
        raise ValueError("BOT_KEY environment variable is missing!")

    client = MyBot(token=token)
    print("STARTING STOAT CLIENT...")
    client.run()


if __name__ == "__main__":
    start_bot()

