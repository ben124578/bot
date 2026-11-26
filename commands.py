
import os
import random
from openai import OpenAI

# Grok API connection
grok = OpenAI(
    api_key=os.environ.get("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# Saint's Corpse gacha
corpse_parts = [
    ("Left Arm", 30),
    ("Right Arm", 25),
    ("Left Eye", 20),
    ("Right Eye", 15),
    ("Heart", 7),
    ("Torso", 3)
]

# Active Tusk conversations
waiting_for_message = set()
conversation_history = {}
catchphrase_countdown = {}

CATCHPHRASES = ["chumi", "movẽre crüs"]

SYSTEM_PROMPT = """
You are Tusk, a sarcastic, brutally honest and funny AI chatbot.
You have a chaotic personality and enjoy joking around.
You can tease the user, use casual language and occasionally roast them.
Do not be overly formal. Respond naturally and stay conversational.
Do not pretend to be a human.
Keep most responses reasonably short.
"""

async def handle_message(client, message):
    if message.author_id == client.me.id:
        return

    user_id = message.author_id
    content = message.content.strip()
    lower_content = content.lower()

    # --------------------------------
    # SAINT'S CORPSE GACHA
    # --------------------------------
    if lower_content == "tusk spin the steel":

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
        return

    # --------------------------------
    # STOP TUSK MODE
    # --------------------------------
    if lower_content == "tusk stop":
        waiting_for_message.discard(user_id)
        conversation_history.pop(user_id, None)
        catchphrase_countdown.pop(user_id, None)

        await message.channel.send("Tusk mode deactivated.")
        return

    # --------------------------------
    # ACTIVATE TUSK MODE
    # --------------------------------
    if lower_content == "tusk":
        waiting_for_message.add(user_id)

        conversation_history[user_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        catchphrase_countdown[user_id] = random.randint(1, 2)

        await message.channel.send("chumi")
        return

    # --------------------------------
    # GROK AI CONVERSATION
    # --------------------------------
    if user_id in waiting_for_message:

        history = conversation_history[user_id]

        history.append({
            "role": "user",
            "content": content
        })

        try:
            response = grok.responses.create(
                model="grok-4.7",
                input=history,
                store=False
            )

            answer = response.output_text

            if not answer:
                answer = "I have absolutely no idea what to say."

            history.append({
                "role": "assistant",
                "content": answer
            })

            # Keep conversation history manageable
            if len(history) > 21:
                conversation_history[user_id] = [
                    history[0]
                ] + history[-20:]

            await message.channel.send(answer)

            # Random catchphrase every 1-2 AI replies
            catchphrase_countdown[user_id] -= 1

            if catchphrase_countdown[user_id] <= 0:
                phrase = random.choice(CATCHPHRASES)
                await message.channel.send(phrase)

                catchphrase_countdown[user_id] = random.randint(1, 2)

        except Exception as error:
            print(f"Grok API error: {error}")

            # Remove the failed message from history
            if history and history[-1]["role"] == "user":
                history.pop()

            await message.channel.send(
                "My brain just malfunctioned. Try again."
            )

        return

