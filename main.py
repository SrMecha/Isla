import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
from modules.database import DatabaseManager
from modules.embeds import EmbedBuilder
from modules.views import ViewBuilder
from modules.modals import NewPhraseModal

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
MONGO_KEY = os.environ.get("MONGO_KEY")
owners_ids = [652472617667788801]

intent = disnake.Intents.all()
client = commands.Bot(command_prefix="isla ", intents=intent)

log_channel_id = 1002314007157407915
client.log_channel = None

database = DatabaseManager(MONGO_KEY)


@client.event
async def on_ready():
    await database.load()
    print("База данных загружена")
    client.log_channel = await client.fetch_channel(log_channel_id)
    print("Компоненты загружены")
    await client.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.listening,
            name="тебя"
        )
    )
    print('Бот запущен как {0.user}'.format(client))
    print('='*15)


@client.event
async def on_message(message: disnake.Message):
    await client.process_commands(message)
    if message.author.bot or client.log_channel is None:
        return
    name_in_message = bool("<@1000150001537798155>" in message.content.lower() or "айла" in message.content.lower())
    referenced = False
    if message.reference:
        reference_message = await message.channel.fetch_message(message.reference.message_id)
        if reference_message.author.id == client.user.id:
            referenced = True
        else:
            await client.log_channel.send(
                embed=EmbedBuilder.create_other_trigger_log_embed(
                    trigger=reference_message.content,
                    most_like=database.get_most_similar_phrase(reference_message.content),
                    guild=reference_message.guild,
                    author=reference_message.author
                )
            )

    if name_in_message or referenced:
        message_content = message.content.lower()
        message_content.replace("<@1000150001537798155>", "")
        message_content.replace("айла", "")
        phrase = await database.get_phrase_by_trigger(message_content)
        if phrase is None:
            await client.log_channel.send(
                embed=EmbedBuilder.create_self_trigger_log_embed(
                    trigger=message_content,
                    most_like=database.get_most_similar_phrase(message_content),
                    guild=message.guild,
                    author=message.author
                )
            )
            return
        await message.reply(phrase.get_random_answer)


@client.event
async def on_button_click(interaction: disnake.MessageInteraction):
    if interaction.author.id not in owners_ids:
        interaction.response.send_message(
            "Погоди, эта кнопка предназначена не для тебя. Не трогай её, как бы сильно тебе не хотелось бы.",
            ephemeral=True
        )
    button: disnake.Button = interaction.component
    custom_id = button.custom_id.split("_")
    if button.custom_id == "without_new":
        await interaction.response.send_modal(
            modal=NewPhraseModal(database)
        )
        return

    await interaction.response.defer()


@client.command(name="add")
async def add_phrase(ctx):
    await ctx.send(
        view=ViewBuilder.create_add_phrase()
    )


client.run(TOKEN)
