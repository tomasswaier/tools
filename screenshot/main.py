#!/usr/bin/env python3
import gi
import datetime

gi.require_version('Gtk', '3.0')
import os
from gi.repository import Gtk, Gdk, GdkPixbuf


class Application(Gtk.Window):
    sc_frame = None
    left_x = 0
    left_y = 0
    right_x = 0
    right_y = 0
    #this variable represents the amount of pixels you will be jumping by
    jump_value = 50
    right_x = 400
    right_y = 400
    screenshot = None

    def __init__(self):
        super().__init__(title="GoodBye World")

        overlay = Gtk.Overlay()
        self.add(overlay)

        screen = Gdk.Display.get_default()
        monitor = screen.get_primary_monitor()
        sizes = monitor.get_geometry()

        self.set_default_size(sizes.width, sizes.height)
        root_monitor = screen.get_default_screen().get_root_window()
        self.screenshot = Gdk.pixbuf_get_from_window(root_monitor, sizes.x,
                                                     sizes.y, sizes.width,
                                                     sizes.height)
        self.pixbuf = self.screenshot.scale_simple(
            sizes.width, sizes.height, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image()
        image.set_from_pixbuf(self.pixbuf)
        overlay.add(image)

        self.canvas = Gtk.DrawingArea()
        self.canvas.set_size_request(sizes.height, sizes.width)
        self.canvas.connect("draw", self.draw)
        overlay.add_overlay(self.canvas)
        self.keys_pressed = set()

        self.connect("key-press-event", self.on_key_press)
        self.connect("key-release-event", self.on_key_release)

    def draw(self, widget, cr):
        self.sc_frame = cr
        self.sc_frame.set_source_rgb(0.3, 1, 0.3)
        self.sc_frame.rectangle(self.left_x, self.left_y,
                                self.right_x - self.left_x,
                                self.right_y - self.left_y)
        self.sc_frame.stroke()

    def copy_image_to_clipboard(self, pixbuf):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_image(pixbuf)
        clipboard.store()

    def on_key_press(self, widget, event):
        self.keys_pressed.add(event.keyval)
        if Gdk.KEY_s in self.keys_pressed and Gdk.KEY_k in self.keys_pressed:
            self.right_y -= self.jump_value

        elif Gdk.KEY_s in self.keys_pressed and Gdk.KEY_j in self.keys_pressed:
            self.right_y += self.jump_value

        elif Gdk.KEY_d in self.keys_pressed and Gdk.KEY_l in self.keys_pressed:
            self.right_x += self.jump_value

        elif Gdk.KEY_d in self.keys_pressed and Gdk.KEY_h in self.keys_pressed:
            self.right_x -= self.jump_value

        elif Gdk.KEY_w in self.keys_pressed and Gdk.KEY_k in self.keys_pressed:
            self.left_y -= self.jump_value

        elif Gdk.KEY_w in self.keys_pressed and Gdk.KEY_j in self.keys_pressed:
            self.left_y += self.jump_value

        elif Gdk.KEY_a in self.keys_pressed and Gdk.KEY_l in self.keys_pressed:
            self.left_x += self.jump_value

        elif Gdk.KEY_a in self.keys_pressed and Gdk.KEY_h in self.keys_pressed:
            self.left_x -= self.jump_value
        elif Gdk.KEY_p in self.keys_pressed:
            new_pixbuf = self.pixbuf.new_subpixbuf(self.left_x, self.left_y,
                                                   self.right_x - self.left_x,
                                                   self.right_y - self.left_y)
            home_directory = os.path.expanduser("~")
            screenshots_directory = os.path.join(home_directory, "Pictures",
                                                 "Screenshots")
            os.chdir(screenshots_directory)
            new_pixbuf.savev(str(datetime.datetime.now()) + ".png", "png", ())

            self.copy_image_to_clipboard(new_pixbuf)
            Gtk.main_quit()
        self.canvas.queue_draw()

    def on_key_release(self, widget, event):
        if event.keyval in self.keys_pressed:
            self.keys_pressed.remove(event.keyval)


win = Application()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
