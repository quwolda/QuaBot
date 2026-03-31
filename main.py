import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands

print("1. Импорты прошли успешно")

load_dotenv()
TOKEN = os.getenv('TOKEN')
print(f"2. Токен найден: {'ДА' if TOKEN else 'НЕТ'}")

bot = commands.InteractionBot(intents=disnake.Intents.all())
print("3. Бот инициализирован")

@bot.event
async def on_ready():
    print(f"6. Бот в сети как {bot.user} ✅")

if __name__ == "__main__":
    print("4. Пробуем запустить bot.run()...")
    try:
        # ЗАКОММЕНТИРУЙ ПОКА ЗАГРУЗКУ КОГОВ!
        bot.load_extensions("./cogs")
        print("5. Коги загружены")
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ ОШИБКА ПРИ ЗАПУСКЕ: {e}")
