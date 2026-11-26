import os
import stoat
import commands

class MyBot(stoat.Client):

    async def on_ready(self, event, /):
        print(f"Logged in as {self.me}")

    async def on_message(self, message, /):
        if message.author_id == self.me.id:
            return

        await commands.handle_message(self, message)


token = os.environ.get("BOT_KEY")

if not token:
    raise ValueError("BOT_KEY environment variable is missing!")

client = MyBot(token=token)
print("STARTING STOAT CLIENT...")
client.run()
