<div id="header" align="center">
    <img src="https://github.com/romanin-rf/SeaPlayer/assets/60302782/937adcc4-f547-440c-8139-a5f15bffa157" alt="Icon" width="300">
</div>
<div id="header" align="center"><h1>SeaPlayer</h1></div>

## Descriptions
SeaPlayer is a player that works in the terminal. Works with `MP3`, `OGG`, `WAV`, `MIDI` and `FLAC` files.

## Install
1. You can use [Release](https://github.com/romanin-rf/sea-player/releases)
2. ***Download clone repository*** install the dependencies from `requirements.txt` and run via [Python](https://www.python.org).
3.  ```
    pip install --upgrade seaplayer
    ```

### For MIDI playback
In order to play MIDI files you need to install FluidSynth:
- **Windows**: https://github.com/FluidSynth/fluidsynth/releases
- **Linux**:
    - **Ubuntu/Debian**:
        ```shell
        sudo apt-get install fluidsynth
        ```
    - **Arch Linux**:
        ```shell
        sudo pacman -S fluidsynth
        ```
- **MacOS**
    - With [Fink](http://www.finkproject.org/):
        ```shell
        fink install fluidsynth
        ```
    - With [Homebrew](https://brew.sh/):
        ```shell
        brew install fluidsynth
        ```
    - With [MacPorts](http://www.macports.org/):
        ```shell
        sudo port install fluidsynth
        ```

## Using
```shell
python -m seaplayer # Method for `downloaded repository` or `installed via pip`
```
![MainScreen-v0.5.4](https://github.com/romanin-rf/SeaPlayer/assets/60302782/5be6c2cb-5602-4c85-a3be-ae36a90e71e4)
![ConfigurateScreen-v0.5.4](https://github.com/romanin-rf/SeaPlayer/assets/60302782/922c7112-2259-47d1-9619-488855e14c2c)
