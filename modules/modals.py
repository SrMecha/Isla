import disnake
from modules.database import DatabaseManager


class NewPhraseModal(disnake.ui.Modal):
    def __init__(self, database: DatabaseManager):
        components = [
            disnake.ui.TextInput(
                label="Введите тригеры через \" | \"",
                placeholder="Просто | Введите | Все | Тригеры",
                custom_id="triggers",
                style=disnake.TextInputStyle.paragraph
            ),
            disnake.ui.TextInput(
                label="Введите ответы через \" | \"",
                placeholder="Вот пример. | Надо вводить вот так вот. | Иначе это не будет работать.",
                custom_id="answers",
                style=disnake.TextInputStyle.paragraph,
            ),
        ]
        super().__init__(
            title="Создание новой фразы",
            custom_id="CreateNewPhrase",
            components=components,
            timeout=600
        )
        self.database = database

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        triggers = []
        for trigger in inter.text_values["triggers"].split(" | "):
            triggers.append(trigger.lower())
        await self.database.add_phrase(triggers=triggers, answers=inter.text_values["answers"].split(" | "))
        await inter.response.send_message("Я поняла...")

    async def on_error(self, error: Exception, interaction: disnake.ModalInteraction):
        pass
