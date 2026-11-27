
import os
import json
from openai import OpenAI
import psycopg

# --------------------------------
# GROQ AI SETUP
# --------------------------------

api_key = os.getenv("GROQ_API_KEY")
database_url = os.getenv("DATABASE_URL")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing!")

if not database_url:
    raise ValueError("DATABASE_URL is missing!")

print("GROQ API KEY:", "FOUND", flush=True)
print("DATABASE URL:", "FOUND", flush=True)

grok = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-120b"


# --------------------------------
# TUSK PERSONALITY
# --------------------------------

SYSTEM_PROMPT = """
You are Tusk, a sarcastic, brutally honest and funny AI.

You have a chaotic personality.
You can tease and roast users playfully.
Speak casually and naturally.
Keep responses relatively short.
Remember details from the conversation.
"""


# --------------------------------
# SUPABASE DATABASE
# --------------------------------

def get_connection():
    return psycopg.connect(database_url)


def initialize_database():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tusk_memory (
                    user_id TEXT PRIMARY KEY,
                    history JSONB NOT NULL DEFAULT '[]'::jsonb
                )
            """)

    print("TUSK DATABASE READY!", flush=True)


def get_history(user_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT history::text FROM tusk_memory WHERE user_id = %s",
                (user_id,)
            )

            result = cursor.fetchone()

    if result:
        return json.loads(result[0])

    return []


def save_history(user_id, history):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tusk_memory (user_id, history)
                VALUES (%s, %s::jsonb)
                ON CONFLICT (user_id)
                DO UPDATE SET history = EXCLUDED.history
            """, (user_id, json.dumps(history)))


# Create the database table when the bot starts
initialize_database()


# --------------------------------
# HANDLE MESSAGES
# --------------------------------

async def handle_message(client, message):

    # Ignore the bot's own messages
    if message.author_id == client.me.id:
        return

    content = (message.content or "").strip()

    if not content:
        return

    user_id = str(message.author_id)

    # Check whether the message starts with "tu"
    starts_with_tu = (
        content[:2].lower() == "tu"
        and (len(content) == 2 or content[2].isspace())
    )

    # Remove "tu" when sending the message to Groq
    if starts_with_tu:
        user_message = content[2:].strip()
    else:
        user_message = content

    # Load this user's permanent conversation history
    history = get_history(user_id)

    # Remember the message, even if it doesn't start with "tu"
    if user_message:
        history.append({
            "role": "user",
            "content": user_message
        })

    # Save immediately so messages survive restarts
    save_history(user_id, history)

    # Stay silent unless the message starts with "tu"
    if not starts_with_tu:
        return

    if not user_message:
        return

    # Build conversation for Groq
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + history

    try:
        response = grok.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "My brain just stopped working."

        # Remember Tusk's response too
        history.append({
            "role": "assistant",
            "content": answer
        })

        save_history(user_id, history)

        await message.channel.send(answer)

    except Exception as error:
        print("GROQ ERROR TYPE:", type(error).__name__, flush=True)
        print("GROQ ERROR:", repr(error), flush=True)

        await message.channel.send(
            "My brain malfunctioned. Try again."
        )
