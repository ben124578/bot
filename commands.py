
import os
import random
from openai import OpenAI

api_key = os.getenv("XAI_API_KEY")

print(
    "XAI API KEY CHECK:",
    "FOUND" if api_key else "MISSING",
    flush=True
)

grok = OpenAI(
    api_key=api_key,
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

# Active AI conversations
active_users = set()
conversation_history = {}

# Tusk catchphrases
CATCHPHRASES = ["chumi", "movẽre crüs"]

SYSTEM_PROMPT = """
You are Tusk, a sarcastic, brutally honest and funny AI.
You have a chaotic personality.
You can tease and roast users playfully.
Speak casually and naturally.
Keep responses relatively short.
"""


async def handle_message(client, message):

    # Ignore bot messages
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
    # ACTIVATE AI MODE
    # --------------------------------
    if lower_content == "tusk":

        if user_id not in active_users:
            active_users.add(user_id)

            conversation_history[user_id] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]

            await message.channel.send("chumi")
        else:
            await message.channel.send(
                "I'm already here, dumbass. Say something."
            )

        return

    # --------------------------------
    # DEACTIVATE AI MODE
    # --------------------------------
    if lower_content == "spin ball":

        if user_id in active_users:
            active_users.remove(user_id)
            conversation_history.pop(user_id, None)

            await message.channel.send("chumi")

        return

    # --------------------------------
    # GROK CONVERSATION
    # --------------------------------
    if user_id in active_users:

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
                answer = "My brain just stopped working."

            history.append({
                "role": "assistant",
                "content": answer
            })

            # Keep memory manageable
            if len(history) > 21:
                conversation_history[user_id] = (
                    [history[0]] + history[-20:]
                )

            await message.channel.send(answer)

            # Random catchphrase every 1-2 AI replies
            if random.randint(1, 2) == 1:
                await message.channel.send(
                    random.choice(CATCHPHRASES)
                )

               except Exception as error:
            print("GROK ERROR TYPE:", type(error).__name__, flush=True)
            print("GROK ERROR:", repr(error), flush=True)
            print("GROK STATUS:", getattr(error, "status_code", None), flush=True)

            error_response = getattr(error, "response", None)

            if error_response is not None:
                print("GROK RESPONSE BODY:", error_response.text, flush=True)

            error_body = getattr(error, "body", None)
            if error_body is not None:
                print("GROK ERROR BODY:", repr(error_body), flush=True)

            if history and history[-1]["role"] == "user":
                history.pop()

            await message.channel.send(
                "My brain malfunctioned. Try again."
            )
    print("GROK ERROR TYPE:", type(error).__name__, flush=True)
    print("GROK ERROR:", repr(error), flush=True)
    print("GROK STATUS:", getattr(error, "status_code", None), flush=True)

    error_response = getattr(error, "response", None)

    if error_response is not None:
        print("GROK RESPONSE BODY:", error_response.text, flush=True)

    error_body = getattr(error, "body", None)
    if error_body is not None:
        print("GROK ERROR BODY:", repr(error_body), flush=True)

    if history and history[-1]["role"] == "user":
        history.pop()

    await message.channel.send(
        "My brain malfunctioned. Try again."
    )
