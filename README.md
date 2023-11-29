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
![MainScreen-v0 7 2](https://github.com/romanin-rf/SeaPlayer/assets/60302782/f836ac9e-fb9e-44e4-9bc3-44b2d13fc873)
![ConfigurateScreen-v0 7 2](https://github.com/romanin-rf/SeaPlayer/assets/60302782/7568c059-dea2-4fb5-9333-e02a3a636499)
