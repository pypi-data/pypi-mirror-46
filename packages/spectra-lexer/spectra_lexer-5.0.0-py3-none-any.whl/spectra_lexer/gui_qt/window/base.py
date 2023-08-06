from .main_window import MainWindow
from spectra_lexer.gui import Window


class GUIQtWindow(Window):
    """ GUI Qt operations class for the main window. """

    window: MainWindow = None  # Main GUI window. All GUI activity (including dialogs) is coupled to this window.

    @init("gui")
    def start(self, keys:dict) -> None:
        """ Create the window, get everything we need from it, and send it all to the GUI components. """
        self.window = MainWindow()
        elements = self.window.widgets()
        d = {k: elements[k] for k in keys if k in elements}
        self.engine_call("res:gui", d, broadcast_depth=1)

    def show(self) -> None:
        if self.window is not None:
            self.window.show()
            self.window.activateWindow()
            self.window.raise_()

    def close(self) -> None:
        if self.window is not None:
            self.window.close()
