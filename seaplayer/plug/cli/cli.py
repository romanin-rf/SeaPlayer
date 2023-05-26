import os
import click
from rich.console import Console
# > Local Import's
from .exceptions import *
from ...units import PLUGINS_CONFIG_PATH
from ..pluginbase import PluginInfo
from ..pluginloader import PluginLoaderConfigManager
from .functions import (
    init_config,
    is_config_inited,
    get_plugins_info,
    raise_exception,
    is_plugin_dirpath
)

# ! Vars
console = Console()
plugin_config = PluginLoaderConfigManager(PLUGINS_CONFIG_PATH)

CREATE_DEFAULT_CODE = """\
from seaplayer.plug import PluginBase

class Plugin(PluginBase):
    pass

plugin_main = Plugin
"""

# ! Commands
@click.command("enable", help="Enabling plugin.")
@click.argument("plugin_name_id")
def enabling(plugin_name_id: str):
    if plugin_config.exists_plugin_by_name_id(plugin_name_id):
        plugin_config.enable_plugin_by_name_id(plugin_name_id)
        console.print(f"[yellow]The {repr(plugin_name_id)} plug-in is [green]enabled[/green].[/yellow]")
    else:
        raise_exception(console, PluginNotExistsError, plugin_name_id)

@click.command("disable", help="Disabling plugin.")
@click.argument("plugin_name_id")
def disabling(plugin_name_id: str):
    if plugin_config.exists_plugin_by_name_id(plugin_name_id):
        plugin_config.disable_plugin_by_name_id(plugin_name_id)
        console.print(f"[yellow]The {repr(plugin_name_id)} plug-in is [red]disabled[/red].[/yellow]")
    else:
        raise_exception(console, PluginNotExistsError, plugin_name_id)

@click.command("list", help="List of plugins.")
def listing():
    if len(plugin_config.config.plugins_enable) > 0:
        for n, info in enumerate(get_plugins_info(), 1):
            status = "[green]Enabled[/green]" if plugin_config.is_enable_plugin(info) else "[red]Disabled[/red]"
            console.print(
                f"[cyan]{n}[/cyan]. [green]{info.name}[/green] ([green]{info.name_id}[/green]) [cyan]v{info.version}[/cyan] from [yellow]{info.author}[/yellow] ({status})"
            )
    else:
        console.print(f"[yellow]The list of plugins is [blue]empty[/blue].[/yellow]")

@click.command("create", help="Create plugin environment.")
@click.argument("dirpath", type=click.Path(True, False))
@click.option(
    "--name", "name",
    help="Name of the plugin.",
    type=str, prompt=True
)
@click.option(
    "--name-id", "name_id",
    help="Name ID of the plugin.",
    type=str, prompt=True
)
@click.option(
    "--version", "-v", "version",
    help="Version of the plugin.",
    type=str, prompt=True
)
@click.option(
    "--author", "-a", "author",
    help="Author of the plugin.",
    type=str, prompt=True
)
@click.option(
    "--description", "-d", "description",
    help="Description of the plugin.",
    type=str, default=None
)
@click.option(
    "--url", "-u", "url",
    help="Link to the plugin source code.",
    type=str, default=None
)
@click.option(
    "--recreate", "recreate",
    help="Ignores if there is already a plugin in the folder and overwrites it.",
    is_flag=True, default=False
)
def creating(
    dirpath: str,
    recreate: bool,
    **kwargs: str
):
    dirpath = os.path.abspath(dirpath)
    try:
        if (not is_plugin_dirpath(dirpath)) or recreate:
            info = PluginInfo(**kwargs)
            
            with open(os.path.join(dirpath, "info.json"), "w", encoding="utf-8") as file:
                file.write(info.json())
            with open(os.path.join(dirpath, "__init__.py"), "w", encoding="utf-8") as file:
                file.write(CREATE_DEFAULT_CODE)
            
            console.print("[yellow]The plugin directory has been [green]created[/green].[/yellow]")
        else:
            raise_exception(console, IsPluginDirectoryError, dirpath)
    except:
        console.print_exception()

# ! Main Group
@click.group
@click.option(
    "--init-config", "initialization_config",
    help="Forced (re)initialisation of the config.",
    is_flag=True, default=False
)
def main(initialization_config: bool):
    if (not is_config_inited()) or initialization_config:
        init_config()

# ! Main Group Bind Commands
main.add_command(enabling)
main.add_command(disabling)
main.add_command(listing)
main.add_command(creating)
