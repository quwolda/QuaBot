import disnake
from disnake.ext import commands

# Класс для управления кнопкой
class AvatarControl(disnake.ui.View):
    def __init__(self, user: disnake.User, author: disnake.User):
        super().__init__(timeout=60)
        self.user = user
        self.author = author
        # Глобальный аватар
        self.global_url = user.avatar.url if user.avatar else user.default_avatar.url
        # Безопасно пытаемся достать серверный аватар
        guild_av = getattr(user, "guild_avatar", None)
        self.server_url = guild_av.url if guild_av else self.global_url
        self.is_global = True


    @disnake.ui.button(label="Сменить (Общий/Серверный)", style=disnake.ButtonStyle.gray)
    async def switch_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        # Необязательно, но полезно: чтобы только автор команды мог тыкать
        if inter.author.id != self.author.id:
            return await inter.send("Это не ваша кнопка!", ephemeral=True)

        self.is_global = not self.is_global
        
        # Редактируем текущий эмбед
        embed = inter.message.embeds[0]
        embed.set_image(url=self.global_url if self.is_global else self.server_url)
        embed.set_thumbnail(url=self.server_url if self.is_global else self.global_url)
        
        await inter.response.edit_message(embed=embed, view=self)

class General(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    # Настройки для работы везде (User Install + Guild)
    EVERYWHERE = {
        "install_types": disnake.ApplicationInstallTypes.all(),
        "contexts": disnake.InteractionContextTypes.all()
    }

    # /ping
    @commands.slash_command(
        name="ping",
        description="Пинг",
        name_localizations={"ru": "пинг"},
        **EVERYWHERE
    )
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send(f"🏓 Понг! Задержка: `{round(self.bot.latency * 1000)}ms`")

    # /info
    @commands.slash_command(
        name="info",
        description="Инфа о боте",
        name_localizations={"ru": "Инфа"},
        **EVERYWHERE
    )
    async def info(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send("Я долбаёб 🐧")

    # /avatar
    @commands.slash_command(
        name="avatar", 
        description="Посмотреть аватар пользователя",
        name_localizations={"ru": "аватар"},
        **EVERYWHERE
    )
    async def avatar(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        user = user or inter.author
        view = AvatarControl(user, inter.author)
        
        embed = disnake.Embed(
            title=f"@{user.display_name}",
            color=0x76028d,
            timestamp=disnake.utils.utcnow()
        )

        embed.set_author(name="Аватар пользователя")
        embed.set_image(url=view.global_url)
        embed.set_thumbnail(url=view.server_url)
        embed.set_footer(text="QuaBot")
        
        await inter.send(embed=embed, view=view)

def setup(bot: commands.InteractionBot):
    bot.add_cog(General(bot))
