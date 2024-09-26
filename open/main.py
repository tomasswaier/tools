import sys
import webbrowser
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

gi.require_version("GdkX11", "3.0")
from gi.repository import GdkX11
import vlc


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

    # if its an image
    def open_image(self, img):
        self.image = Gtk.Image()
        self.image.set_from_file(img)
        self.add(self.image)

        self.show_all()

    # if its a video
    def open_video(self, filename, is_audio=False):
        self.is_player_active = False
        self.playerPaused = False
        self.vbox = Gtk.VBox(spacing=6)
        self.add(self.vbox)
        self.filename = filename

        self.drawArea = Gtk.DrawingArea()
        self.drawArea.set_size_request(800, 800)
        self.drawArea.connect("realize", self._realized)

        self.scrollBar = Gtk.HScale.new()

        self.playButton = Gtk.Button.new_with_label("Start/Stop")
        self.playButton.connect("clicked", self.toggle_video)
        self.vbox.pack_start(self.drawArea, True, True, 0)
        self.vbox.pack_start(self.playButton, False, False, 0)
        self.vbox.pack_start(self.scrollBar, False, False, 0)

        self.show_all()

    def set_time(self, widget, data=None):
        print(self.scrollBar.value())

    def toggle_video(self, widget, data=None):
        if self.is_player_active == False and self.playerPaused == False:
            self.player.play()
            self.is_player_active = True
        if self.is_player_active == True and self.playerPaused == True:
            self.player.play()
            self.playerPaused = False
        if self.is_player_active == True and self.playerPaused == False:
            self.player.pause()
            self.playerPaused = True
        else:
            pass

    def stopPlayer(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)

    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib")
        if self.vlcInstance is None:
            raise Exception("Failed to create VLC instance")
        self.player = self.vlcInstance.media_player_new()
        media = self.vlcInstance.media_new_path(self.filename)
        self.player.set_media(media)

        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        self.player.set_mrl(self.filename)
        self.player.play()
        self.is_player_active = True

        self.scrollBar.set_range(0, self.player.get_position() / 1000)
        self.scrollBar.set_size_request(100, 30)


def main(file):
    # split the input file and match it with correct type
    # I dont belive use of magic library is necesary
    fileType = str(file).split(".")

    match fileType[-1]:
        case "html" | "webm":
            # uses user browser to open specified website
            webbrowser.open(file, new=2)
        case "jpg" | "png" | "ani" | "gif" | "icns" | "jpeg" | "svg" | "xpm" | "xbm":
            display = Window()
            display.open_image(file)
            Gtk.main()
        case "mp4" | "mp3" | "avi" | "mkv" | "m4a":
            display = Window()
            display.open_video(file)
            display.show_all()
            Gtk.main()


main(sys.argv[1])
