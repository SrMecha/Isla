import disnake


class ViewBuilder:
    @classmethod
    def create_trigger_log_view(cls, inactive_trigger_id: str) -> disnake.ui.View:
        """Возвращает кнопки логов тригеров для добавления"""
        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                style=disnake.ButtonStyle.green,
                label="Создать новую фразу из триггера",
                row=0,
                custom_id=f"new_{inactive_trigger_id}"
            )
        )
        view.add_item(
            disnake.ui.Button(
                style=disnake.ButtonStyle.red,
                label="Удалить неактивный триггер",
                row=0,
                custom_id=f"delete_{inactive_trigger_id}"
            )
        )
        return view

    @classmethod
    def create_add_phrase(cls):
        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                style=disnake.ButtonStyle.green,
                label="Создать новую фразу",
                row=0,
                custom_id=f"without_new"
            )
        )
        return view
