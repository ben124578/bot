
import stoat
import random

client = stoat.Client()

# Saint's Corpse gacha
corpse_parts = [
    ("Left Arm", 30),
    ("Right Arm", 25),
    ("Left Eye", 20),
    ("Right Eye", 15),
    ("Heart", 7),
    ("Torso", 3)
]

@client.on(stoat.MessageCreateEvent)
async def on_message(event, /):
    message = event.message

    # Ignore bot messages
    if message.author.relationship is stoat.RelationshipStatus.user:
        return

    if message.content.lower().strip() == "tusk spin the steel":

        result = random.choices(
            [part[0] for part in corpse_parts],
            weights=[part[1] for part in corpse_parts],
            k=1
        )[0]

        if result == "Torso":
            response = (
                "🌟 **HOLY SHIT!!!** 🌟\n"
                "You obtained the **SAINT'S CORPSE TORSO**!\n"
                "A miracle has occurred..."
            )

        elif result == "Heart":
            response = (
                "❤️ **INCREDIBLE SPIN!** ❤️\n"
                "You obtained the **SAINT'S CORPSE HEART**!"
            )

        else:
            response = (
                "🌀 **TUSK SPIN!** 🌀\n"
                f"You obtained: **Saint's Corpse - {result}**!"
            )

        await message.channel.send(response)

client.run("YOUR_BOT_TOKEN")

