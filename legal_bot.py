import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

GUILD_ID = 1392743613124968449  # 👈 Your server ID
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Utility: Split long messages
def split_message(text, max_length=1990):
    lines = text.split('\n')
    chunks, current_chunk = [], ""
    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk)
            current_chunk = line + '\n'
        else:
            current_chunk += line + '\n'
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

@bot.event
async def on_ready():
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)  # ✅ Slash command sync to your guild
        print(f"✅ Legal Assistant Bot is online as {bot.user} | Synced {len(synced)} slash commands to {GUILD_ID}")
    except Exception as e:
        print(f"⚠️ Slash command sync failed: {e}")

# 💬 Auto-answer in #⚖️legal-queries
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    allowed_channel = '⚖️legal-queries'
    if message.guild and message.channel.name != allowed_channel:
        return

    question = message.content.strip()
    if len(question) < 10:
        return

    try:
        async with message.channel.typing():
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a helpful legal assistant. Answer legal questions clearly and simply."},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 1000,
                "temperature": 0.3
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            response_json = response.json()

            if "choices" in response_json:
                full_answer = response_json["choices"][0]["message"]["content"]
                chunks = split_message(full_answer)

                for i, chunk in enumerate(chunks):
                    prefix = "📘 **LegalBot says:**\n" if i == 0 else "📎 Continued:\n"
                    await message.channel.send(prefix + chunk.strip())
            else:
                await message.channel.send("⚠️ Error: No response from model.")
                print("API error response:", response_json)

    except Exception as e:
        await message.channel.send("❌ Sorry, I couldn't process your request.")
        print(f"Error: {e}")

    await bot.process_commands(message)

# ✅ Slash command /ask
@bot.tree.command(name="ask", description="Ask a legal question to LegalBot")
@app_commands.describe(question="Your legal question")
async def ask(interaction: discord.Interaction, question: str):
    if interaction.guild and (not hasattr(interaction.channel, "name") or interaction.channel.name != "🤖bot-commands"):
        await interaction.response.send_message(
            "❌ Please use this command in `#🤖bot-commands` or DM me directly.",
            ephemeral=True
        )
        return

    await interaction.response.defer(thinking=True)

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful legal assistant. Answer legal questions clearly and simply."},
                {"role": "user", "content": question}
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response_json = response.json()

        if "choices" in response_json:
            full_answer = response_json["choices"][0]["message"]["content"]
            chunks = split_message(full_answer)

            for i, chunk in enumerate(chunks):
                prefix = "📘 **LegalBot says:**\n" if i == 0 else "📎 Continued:\n"
                await interaction.followup.send(prefix + chunk.strip())
        else:
            await interaction.followup.send("⚠️ Error: No response from model.")
            print("API error response:", response_json)

    except Exception as e:
        await interaction.followup.send("❌ Sorry, I couldn't process your request.")
        print(f"Error: {e}")

# ✅ Slash command /help
@bot.tree.command(name="help", description="How to use the LegalBot")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(	#🤖🤖bot-commands
        "**👩‍⚖️ LegalBot Help**\n"
        "- Ask directly in `#⚖️legal-queries` (no slash needed).\n"
        "- Or use `/ask` in `#🤖bot-commands` or DMs.\n"
        "- Example: `/ask What is the punishment for cybercrime in India?`\n",
        ephemeral=True
    )

# Start bot
bot.run(DISCORD_TOKEN)
