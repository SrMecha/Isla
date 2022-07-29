import disnake
from typing import Tuple


class EmbedBuilder:
    @classmethod
    def create_other_trigger_log_embed(
            cls,
            trigger: str,
            most_like: Tuple[str, int],
            guild: disnake.Guild,
            author: disnake.User
    ) -> disnake.Embed:
        """Возвращает ембед логов тригеров для добавления, при переписке других пользователей."""
        embed = disnake.Embed(
            title="Переписка других людей",
            description=f"Сервер: {guild.name} | {guild.id}\n"
                        f"Пользователь: {author.name} | {author.id}\n"
                        f"Фраза:\n```{trigger}```\n"
                        f"Больше всего похоже на: ```{most_like[0]}```\n"
                        f"Процент схожести: {most_like[1]}%",
            color=disnake.Color(0x4e4c57)
        )
        embed.set_image(url="https://getwallpapers.com/wallpaper/full/7/9/f/722830-best-plastic-memories-wallpapers-1920x1080.jpg")
        return embed

    @classmethod
    def create_self_trigger_log_embed(
            cls,
            trigger: str,
            most_like: Tuple[str, int],
            guild: disnake.Guild,
            author: disnake.User
    ) -> disnake.Embed:
        """Возвращает ембед логов тригеров для добавления, при переписке с ботом."""
        embed = disnake.Embed(
            title="Ответ на сообщение бота",
            description=f"Сервер: {guild.name} | {guild.id}\n"
                        f"Пользователь: {author.name} | {author.id}\n"
                        f"Фраза:\n```{trigger}```\n"
                        f"Больше всего похоже на: ```{most_like[0]}```\n"
                        f"Процент схожести: {most_like[1]}%",
            color=disnake.Color(0x7a7edc)
        )
        embed.set_image(url="https://2.bp.blogspot.com/-tsWzBWI1g5Q/VY4w8pNO3WI/AAAAAAAAOTg/X85s-bCRHpk/w1200-h630-p-k-no-nu/Plastic%2BMemories%2BOriginal%2BSoundtrack%2BVol.1.jpg")
        return embed
