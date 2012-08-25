import sys

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    print("GTK Not Availible")


class Ravlyk:
    wTree = None
    window_main=None
    window_load_images = None

    def __init__( self ):
        filename = "main_window.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)

        self.window_main = builder.get_object('window_main')
        self.window_main.set_title('Ravlyk')
        self.window_main.set_size_request(1000, 500)
        self.window_main.show_all()

        gtk.main()

    def load_images(self, data):
        img_load_dialog = gtk.FileChooserDialog (title="Load images",
                              parent=self.window_main,
                              action=gtk.FILE_CHOOSER_ACTION_OPEN,
                              buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        img_load_dialog.set_select_multiple(True)

        response = img_load_dialog.run()

        if response == gtk.RESPONSE_OK:
            filenames = img_load_dialog.get_filenames()
            for file in filenames:
                print ('%s selected' % (file,))
        elif response == gtk.RESPONSE_CANCEL:
            print ('Closed, no files selected')
        img_load_dialog.destroy()

    def quit(self, widget):
        sys.exit(0)


if __name__ == "__main__":
    Ravlyk()
