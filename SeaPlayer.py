from seaplayer.seaplayer import SeaPlayer
from rich.console import Console

console = Console()

# ! Start
if __name__ == "__main__":
    try:
        app = SeaPlayer()
        app.run()
        app.started = False
        #console.print(app.styles.background)
    except: console.print_exception(word_wrap=True, show_locals=True)