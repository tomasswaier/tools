import sys
import webbrowser
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class Window(Gtk.Window):
    # initialize Gtk,Window
    def __init__(self):
        Gtk.Window.__init__(self)
        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press_event)

    # bind x to close the app
    def on_key_press_event(self, widget, event):
        if event.keyval == Gdk.KEY_x:
            Gtk.main_quit()

    def openImage(self, img):

        self.image = Gtk.Image()
        self.image.set_from_file(img)
        self.add(self.image)

        self.show_all()


def main(file):
    # split the input file and match it with correct type
    # I dont belive use of magic library is necesary
    fileType = str(file).split(".")

    match fileType[1]:
        case "html" | "webm":
            # uses user browser to open specified website
            webbrowser.open(file, new=2)
        case "jpg" | "png" | "ani" | "gif" | "icns" | "jpeg" | "svg" | "xpm" | "xbm":
            display = Window()
            display.openImage(file)
            Gtk.main()


main(sys.argv[1])
