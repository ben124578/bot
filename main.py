import os
from threading import Thread
from flask import Flask
import commands

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web, daemon=True).start()

# 2. Stoat Bot Setup
class MyBot(stoat.Client):
    async def on_ready(self, _, /):
        print(f"Logged in as {self.me}")

    async def on_message(self, message, /):
      await commands.handle_message(self, message)
      


token = os.environ.get("BOT_KEY")
client = MyBot(token=token)
client.run()
