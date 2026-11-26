
import os
import stoat
from threading import Thread
from flask import Flask
import commands

# Flask keep-alive server
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web, daemon=True).start()


# Stoat Bot Setup
class MyBot(stoat.Client):

    async def on_ready(self, event, /):
        print(f"Logged in as {self.me}")

    async def on_message(self, message, /):
        # Ignore bot messages
        if message.author_id == self.me.id:
            return

        await commands.handle_message(self, message)


# Load token
token = os.environ.get("BOT_KEY")

if not token:
    raise ValueError("BOT_KEY environment variable is missing!")

client = MyBot(token=token)
client.run()
