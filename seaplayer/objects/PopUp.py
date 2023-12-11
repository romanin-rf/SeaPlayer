from textual.containers import Container

# ! Main Class
class PopUp(Container):
    DEFAULT_CSS = """
    PopUp {
        layer: popup;
        background: $background;
        align-vertical: middle;
        align-horizontal: center;
        content-align: center middle;
        width: auto;
        height: auto;
        padding: 1 2 1 2;
    }
    """
    
    pass
