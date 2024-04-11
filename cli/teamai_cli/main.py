# © 2024 Thoughtworks, Inc. | Thoughtworks Pre-Existing Intellectual Property | See License file for permissions.
import typer

from teamai_cli.app.app import App
from teamai_cli.services.client import Client
from teamai_cli.services.config_service import ConfigService
from teamai_cli.services.file_service import FileService
from teamai_cli.services.knowledge_service import KnowledgeService
from teamai_cli.services.page_helper import PageHelper
from teamai_cli.services.token_service import TokenService
from teamai_cli.services.web_page_service import WebPageService

CONFIG_FILE_PATH = "../app/config.yaml"
ENCODING = "cl100k_base"

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def index_file(
    source_path: str,
    destination_dir="new_knowledge_base.kb",
    embedding_model="openai",
    config_path: str = CONFIG_FILE_PATH,
):
    """Index single pdf or text file to a given destination directory."""
    tiktoken_service = TokenService(ENCODING)
    knowledge_service = KnowledgeService(destination_dir, tiktoken_service)
    config_service = ConfigService()
    file_service = FileService()
    client = Client()
    page_helper = PageHelper()
    web_page_service = WebPageService(client, page_helper)
    app = App(config_service, file_service, knowledge_service, web_page_service)
    app.index_individual_file(source_path, embedding_model, config_path)


@cli.command()
def index_all_files(
    source_dir: str,
    destination_dir="new_knowledge_base.kb",
    embedding_model="openai",
    config_path: str = CONFIG_FILE_PATH,
):
    """Index all pdf or text files in a directory to a given destination directory."""
    token_service = TokenService(ENCODING)
    knowledge_service = KnowledgeService(destination_dir, token_service)
    config_service = ConfigService()
    file_service = FileService()
    client = Client()
    page_helper = PageHelper()
    web_page_service = WebPageService(client, page_helper)
    app = App(config_service, file_service, knowledge_service, web_page_service)
    print("Indexing all files")
    app.index_all_files(source_dir, embedding_model, config_path)


@cli.command()
def pickle_web_page(
    url: str,
    destination_path="web_page.pickle",
    html_filter="p",
):
    """Index a web page to a given destination path."""
    token_service = TokenService(ENCODING)
    knowledge_service = KnowledgeService(destination_path, token_service)
    config_service = ConfigService()
    file_service = FileService()
    client = Client()
    page_helper = PageHelper()
    web_page_service = WebPageService(client, page_helper)
    app = App(config_service, file_service, knowledge_service, web_page_service)
    app.index_web_page(
        url=url, html_filter=html_filter, destination_path=destination_path
    )


if __name__ == "__main__":
    cli()
