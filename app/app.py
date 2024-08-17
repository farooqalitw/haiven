# © 2024 Thoughtworks, Inc. | Licensed under the Apache License, Version 2.0  | See LICENSE.md file for permissions.
import gradio as gr
from api.boba_api import BobaApi
from content_manager import ContentManager
from llms.chats import ServerChatSessionMemory
from prompts.prompts_factory import PromptsFactory
from server import Server
from ui.ui_factory import UIFactory
from config_service import ConfigService


class App:
    def __init__(
        self,
        content_manager: ContentManager,
        config_service: ConfigService,
        prompts_factory: PromptsFactory,
        chat_session_memory: ServerChatSessionMemory,
        ui_factory: UIFactory,
    ):
        self.server = Server(
            chat_session_memory,
            config_service,
            BobaApi(
                prompts_factory,
                content_manager,
                chat_session_memory,
                config_service,
            ),
        ).create()
        self.content_manager = content_manager
        self.ui_factory = ui_factory

    def launch_via_fastapi_wrapper(self):
        ui_components = [
            ("create_ui_analysts", "get_analysis_path"),
            ("create_ui_testing", "get_testing_path"),
            ("create_ui_coding", "get_coding_path"),
            ("create_ui_knowledge", "get_knowledge_path"),
            ("create_ui_about", "get_about_path"),
            ("create_plain_chat", "get_chat_path"),
        ]

        for create_ui, get_path in ui_components:
            ui_component = getattr(self.ui_factory, create_ui)()
            path = getattr(self.ui_factory.navigation_manager, get_path)()
            gr.mount_gradio_app(self.server, ui_component, path=path, root_path=path)

        return self.server
