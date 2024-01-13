import uuid

import flet as ft

from .constants import ENDPOINTS
from .models import Webhook
from .webhook import get_test_webhook_data, send_webhook


class HoyoUpdateNotifierWebApp:
    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._uuid = str(uuid.uuid4())

        # control refs
        self._game_dropdown_ref = ft.Ref[ft.Dropdown]()
        self._webhook_textfield_ref = ft.Ref[ft.TextField]()
        self._save_webhook_filled_button_ref = ft.Ref[ft.FilledButton]()
        self._test_webhook_outlined_button_ref = ft.Ref[ft.OutlinedButton]()

    @property
    def _app_bar(self) -> ft.AppBar:
        return ft.AppBar(
            title=ft.Container(
                ft.Text("Hoyo Update Notifier", size=20), margin=ft.margin.symmetric(vertical=10)
            ),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            icon=ft.icons.HELP_CENTER_OUTLINED,
                            text="Tutorial",
                            data="https://github.com/seriaati/hoyo-update-notifier/blob/main/tutorial.md",
                            on_click=self._popup_menu_item_on_click,
                        ),
                        ft.PopupMenuItem(
                            icon=ft.icons.CHAT_OUTLINED,
                            text="Contact me on Discord",
                            data="https://discord.com/users/410036441129943050",
                            on_click=self._popup_menu_item_on_click,
                        ),
                        ft.PopupMenuItem(
                            icon=ft.icons.CODE_OUTLINED,
                            text="Source code",
                            data="https://github.com/seriaati/hoyo-update-notifier",
                            on_click=self._popup_menu_item_on_click,
                        ),
                    ]
                ),
            ],
            toolbar_height=64,
        )

    @property
    def _game_dropdown(self) -> ft.Dropdown:
        return ft.Dropdown(
            label="Game & region",
            options=[ft.dropdown.Option(text=game) for game in ENDPOINTS],
            value=list(ENDPOINTS.keys())[0],
            ref=self._game_dropdown_ref,
            on_change=self._game_dropdown_on_change,
        )

    @property
    def _webhook_textfield(self) -> ft.TextField:
        return ft.TextField(
            label="Discord webhook URL",
            hint_text="https://discord.com/api/webhooks/...",
            ref=self._webhook_textfield_ref,
        )

    @property
    def _save_webhook_filled_button(self) -> ft.FilledButton:
        return ft.FilledButton(
            text="Save",
            ref=self._save_webhook_filled_button_ref,
            icon=ft.icons.SAVE_OUTLINED,
            on_click=self._save_webhook_filled_button_on_click,
        )

    @property
    def _test_webhook_filled_button(self) -> ft.OutlinedButton:
        return ft.OutlinedButton(
            text="Test",
            ref=self._test_webhook_outlined_button_ref,
            icon=ft.icons.SEND_OUTLINED,
            on_click=self._test_webhook_outlined_button_on_click,
        )

    async def _show_error_snackbar(self, msg: str) -> None:
        await self._page.show_snack_bar_async(
            ft.SnackBar(
                ft.Text(msg, color=ft.colors.ON_ERROR_CONTAINER),
                bgcolor=ft.colors.ERROR_CONTAINER,
                show_close_icon=True,
                close_icon_color=ft.colors.ON_ERROR_CONTAINER,
            )
        )

    async def _show_primary_snackbar(self, msg: str) -> None:
        await self._page.show_snack_bar_async(
            ft.SnackBar(
                ft.Text(msg, color=ft.colors.ON_PRIMARY_CONTAINER),
                bgcolor=ft.colors.PRIMARY_CONTAINER,
                show_close_icon=True,
                close_icon_color=ft.colors.ON_PRIMARY_CONTAINER,
            )
        )

    async def _show_loading_snackbar(self, msg: str) -> None:
        await self._page.show_snack_bar_async(
            ft.SnackBar(
                ft.Row(
                    [
                        ft.ProgressRing(
                            width=16,
                            height=16,
                            stroke_width=2,
                            color=ft.colors.ON_SECONDARY_CONTAINER,
                        ),
                        ft.Text(msg, color=ft.colors.ON_SECONDARY_CONTAINER),
                    ]
                ),
                bgcolor=ft.colors.SECONDARY_CONTAINER,
            )
        )

    async def _popup_menu_item_on_click(self, e: ft.ControlEvent) -> None:
        await self._page.launch_url_async(e.control.data)

    async def _game_dropdown_on_change(self, _: ft.ControlEvent) -> None:
        await self._update_webhook_textfield()

    async def _update_webhook_textfield(self) -> None:
        webhook = await Webhook.get_or_none(
            uuid=self._uuid, game=self._game_dropdown_ref.current.value
        )

        if webhook is None:
            self._webhook_textfield_ref.current.value = ""
        else:
            self._webhook_textfield_ref.current.value = webhook.url

        await self._page.update_async()

    async def _save_webhook_filled_button_on_click(self, _: ft.ControlEvent) -> None:
        webhook_url = self._webhook_textfield_ref.current.value

        game = self._game_dropdown_ref.current.value
        webhook = await Webhook.get_or_none(uuid=self._uuid, game=game)
        if webhook is None:
            webhook = Webhook(uuid=self._uuid, game=game)

        if webhook_url is None:
            await webhook.delete()
        else:
            webhook.url = webhook_url
            await webhook.save()
        await self._show_primary_snackbar("Saved")

    async def _test_webhook_outlined_button_on_click(self, _: ft.ControlEvent) -> None:
        webhook_url = self._webhook_textfield_ref.current.value
        if not webhook_url:
            return await self._show_error_snackbar("Enter a webhook URL first")

        game = self._game_dropdown_ref.current.value
        if game is None:
            msg = "Game is None"
            raise RuntimeError(msg)

        await self._show_loading_snackbar("Sending webhook...")

        success = await send_webhook(webhook_url, get_test_webhook_data())
        if success:
            await self._show_primary_snackbar("Webhook sent successfully")
        else:
            await self._show_error_snackbar("Failed to send webhook, check the URL")

    async def _add_controls(self) -> None:
        self._page.appbar = self._app_bar
        await self._page.add_async(
            ft.Container(
                ft.Column([self._game_dropdown, self._webhook_textfield]),
                margin=ft.margin.symmetric(vertical=10),
            )
        )
        await self._page.add_async(
            ft.Row(
                [
                    ft.Container(self._save_webhook_filled_button, margin=ft.margin.only(right=6)),
                    self._test_webhook_filled_button,
                ]
            )
        )

    async def start(self) -> None:
        await self._add_controls()
        await self._page.update_async()

        if self._page.client_storage is None:
            msg = "Client storage is not available"
            raise RuntimeError(msg)

        client_uuid = await self._page.client_storage.get_async("uuid")
        if client_uuid is None:
            client_uuid = self._uuid
            await self._page.client_storage.set_async("uuid", client_uuid)
        else:
            self._uuid = client_uuid

        await self._update_webhook_textfield()
