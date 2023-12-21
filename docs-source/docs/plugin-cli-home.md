# Plugin CLI
## Description
The CLI for managing plugins.

## Using
=== "via `seaplug`"
    ```
    seaplug [--init-config] [load/list/enable/disable/create] [OPTIONS]
    ```
=== "via `python -m`"
    ```bash
    python -m seaplayer.plug [--init-config] [load/list/enable/disable/create] [OPTIONS]
    ```

## Commands
### Load
The command to load plugins.

=== ":material-console: Console"
    ```bash
    seaplug load [--overwrite/-o] ./plugins/ExamplePlugin
    ```
=== "Output"
    ```
    Plugin loaded!
    ```

### Unload
The command to unload plugins.

=== ":material-console: Console"
    ```bash
    seaplug unload seaplayer.plugins.example 
    ```
=== "Output"
    ```
    Plugin unloaded!
    ```

### List
List of all loaded plugins.

=== ":material-console: Console"
    ```bash
    seaplug list
    ```
=== "Output"
    ```
    1. ExamplePlugin (seaplayer.plugins.example) v1.0.0 from Romanin (Disabled)
    ```

### Enable
Enabling the plugin.

=== ":material-console: Console"
    ```bash
    seaplug enable seaplayer.plugins.example
    ```
=== "Output"
    ```
    The 'seaplayer.plugins.example' plug-in is enabled."
    ```

### Disable
Disabling the plugin.

=== ":material-console: Console"
    ```sh
    seaplug disable seaplayer.plugins.example
    ```
=== "Output"
    ```
    The 'seaplayer.plugins.example' plug-in is disabled."
    ```

### Create
Create plugin environment. More information in [Plugin Development](plugin-dev-home.md).

=== ":material-console: Console"
    ```sh
    seaplug create [--name/--name-id/--version/--author/--description/--url/--overwrite] .
    ```
=== "Output"
    ```
    The plugin directory has been created.
    ```
