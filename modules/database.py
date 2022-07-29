import motor.motor_asyncio
import asyncio
import random
from fuzzywuzzy import fuzz, process
from typing import Union, Tuple


class Phrase:
    def __init__(self, phrase: dict):
        self.answers = phrase["answers"]
        self.triggers = phrase["triggers"]
        self.id = phrase["_id"]

    @property
    def get_random_answer(self) -> str:
        """Получить рандомный ответ на триггер."""
        return random.choice(self.answers)


class WebDatabase:
    def __init__(self, mongo_key: str):
        self.cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_key)
        self.cluster.get_io_loop = asyncio.get_running_loop
        db = self.cluster.Isla
        self.active_triggers = db.active_triggers
        self.inactive_triggers = db.inactive_triggers

    async def find_phrase_by_id(self, id: str) -> Phrase:
        """Находит фразу в базе данных по id."""
        return Phrase(await self.active_triggers.find_one({"_id": id}))

    async def add_inactive_trigger(self, trigger: str) -> str:
        """Добавляет неактивный триггер, и возвращает его id."""
        result = await self.inactive_triggers.insert_one({"trigger": trigger})
        return result.inserted_id

    async def add_active_phrase(self, triggers: list, answers: list) -> str:
        """Добавляет фразы в базу данных, и возвращает id."""
        result = await self.active_triggers.insert_one({"triggers": triggers, "answers": answers})
        return result.inserted_id


class CacheDatabase:
    def __init__(self):
        self.trigger_phrases = {}

    async def load_phrases(self, collection) -> None:
        """Загрузка всех тригерров в кэш."""
        self.trigger_phrases = {}
        async for phrase in collection.find():
            for trigger in phrase["triggers"]:
                self.trigger_phrases[trigger] = phrase["_id"]

    def add_triggers(self, triggers: list, id: str) -> None:
        """Добавляет триггеры в кэш"""
        for trigger in triggers:
            self.trigger_phrases[trigger] = id


class DatabaseManager:
    def __init__(self, mongo_key: str):
        self.web = WebDatabase(mongo_key)
        self.cache = CacheDatabase()

    async def load(self) -> None:
        """Подготовка базы данных к работе. Надо вызвать ее перед началом работы."""
        await self.cache.load_phrases(self.web.active_triggers)

    async def get_phrase_by_trigger(self, trigger: str) -> Union[Phrase, None]:
        """Возвращает самую похожу фразу, если процент схожести больше 80. Иначе возвращает None"""
        fuzzy_trigger_return = process.extractOne(
            query=trigger.lower(),
            choices=list(self.cache.trigger_phrases.keys()),
            scorer=fuzz.WRatio
        )
        if fuzzy_trigger_return[1] < 80:
            return None
        return await self.web.find_phrase_by_id(self.cache.trigger_phrases[fuzzy_trigger_return[0]])

    def get_most_similar_phrase(self, trigger: str) -> Tuple[Phrase, int]:
        """Возвращает самую похожу фразу, и процент схожости."""
        fuzzy_trigger_return = process.extractOne(
            query=trigger.lower(),
            choices=list(self.cache.trigger_phrases.keys()),
            scorer=fuzz.WRatio
        )
        return fuzzy_trigger_return

    async def add_trigger_for_consideration(self, trigger: str) -> str:
        """Добавляет триггер на рассмотрение, и возвращает id триггера."""
        result_id = await self.web.add_inactive_trigger(trigger.lower())
        return result_id

    async def add_phrase(self, triggers: list, answers: list) -> None:
        """Добавляет новую фразу."""
        id = await self.web.add_active_phrase(triggers=triggers, answers=answers)
        self.cache.add_triggers(triggers=triggers, id=id)




